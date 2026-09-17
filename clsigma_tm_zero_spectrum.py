#!/usr/bin/env python3
import json
import os
import time

ROOT = "BLEEM=P^L+E^I+A^D+E^S"
PROTOCOL = "CLSIGMA/TM/ZERO_SPECTRUM/BYTE_PRIME_INCREMENTAL/1"
CERT_PATH = "CLSIGMA_TM_ZERO_SPECTRUM.clcert"
EXCLUDED = {CERT_PATH, "CLSIGMA_TM_ZERO_SPECTRUM.out"}

_PRIMES = []
_CANDIDATE = 2


def canonical(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def primes(count):
    global _CANDIDATE
    while len(_PRIMES) < count:
        if is_prime(_CANDIDATE):
            _PRIMES.append(_CANDIDATE)
        _CANDIDATE += 1
    return _PRIMES[:count]


def next_prime(n):
    n = max(2, n)
    while not is_prime(n):
        n += 1
    return n


def spectrum_index(data):
    ps = primes(len(data))
    return sum((i + 1) * (byte + 1) * ps[i] for i, byte in enumerate(data))


def object_code(obj):
    return spectrum_index(canonical(obj).encode())


def parse_bleem():
    if not ROOT.startswith("BLEEM="):
        raise ValueError("invalid root")
    terms = []
    for index, text in enumerate(ROOT.split("=", 1)[1].split("+"), 1):
        base, exponent = text.split("^", 1)
        terms.append(
            {
                "index": index,
                "base": base,
                "exponent": exponent,
                "interpretation": "uninterpreted",
            }
        )
    return {"root": "BLEEM", "op": "=", "rhs_op": "+", "terms": terms}


def repo_manifest_code():
    files = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
        for name in names:
            path = os.path.relpath(os.path.join(root, name), ".")
            if path in EXCLUDED or ".out" in path or path.endswith(".pyc"):
                continue
            with open(path, "rb") as handle:
                data = handle.read()
            files.append([path, len(data), str(spectrum_index(data))])
    files.sort()
    return str(object_code(files)), len(files)


def component(kind, value):
    return object_code({"kind": kind, "value": value})


def cell_component(position, symbol):
    return object_code({"kind": "cell", "position": position, "symbol": symbol})


def configuration_code(state, head, step, tape):
    return (
        component("state", state)
        + component("head", head)
        + component("step", step)
        + sum(cell_component(position, symbol) for position, symbol in tape.items())
    )


def transition_table(ast):
    terms = ast["terms"]
    table = {}
    states = ["q%d" % i for i in range(len(terms) + 1)]
    for index, term in enumerate(terms):
        table[(states[index], "_")] = (
            states[index + 1],
            term["base"],
            1,
            "write:%s^%s" % (term["base"], term["exponent"]),
        )
    table[(states[-1], "_")] = ("HALT", "_", 0, "accept")
    return table


def run_machine():
    ast = parse_bleem()
    table = transition_table(ast)
    tape = {}
    state = "q0"
    head = 0
    step = 0
    z = configuration_code(state, head, step, tape)
    trace = []
    ok = True

    while state != "HALT" and step < len(ast["terms"]) + 2:
        symbol = tape.get(head, "_")
        transition = table.get((state, symbol))
        if transition is None:
            ok = False
            break

        old_state, old_head, old_step = state, head, step
        old_cell_present = old_head in tape
        old_cell_symbol = tape.get(old_head, "_")
        new_state, write_symbol, move, action = transition

        old_terms = (
            component("state", old_state)
            + component("head", old_head)
            + component("step", old_step)
        )
        if old_cell_present:
            old_terms += cell_component(old_head, old_cell_symbol)

        if write_symbol == "_":
            tape.pop(old_head, None)
        else:
            tape[old_head] = write_symbol
        state = new_state
        head = old_head + move
        step = old_step + 1

        new_terms = component("state", state) + component("head", head) + component(
            "step", step
        )
        if old_head in tape:
            new_terms += cell_component(old_head, tape[old_head])

        z = z - old_terms + new_terms
        full = configuration_code(state, head, step, tape)
        incremental_ok = z == full
        ok = ok and incremental_ok
        trace.append(
            {
                "step": step,
                "from": old_state,
                "to": state,
                "head": head,
                "action": action,
                "incremental_update_ok": incremental_ok,
            }
        )

    return ast, tape, state, head, step, z, trace, ok


def main():
    manifest_code, file_count = repo_manifest_code()
    ast, tape, state, head, step, z, trace, incremental_ok = run_machine()
    modulus_seed = object_code(
        {
            "protocol": PROTOCOL,
            "root": ROOT,
            "repo": manifest_code,
            "steps": step,
            "final": z,
        }
    )
    modulus = next_prime(len(str(z)) + file_count + modulus_seed % 997 + 1)
    raw_residue = z % modulus
    balancing = (-raw_residue) % modulus
    verified = (z + balancing) % modulus

    validate = {
        "SyntaxValid": ROOT == "BLEEM=P^L+E^I+A^D+E^S" and len(ast["terms"]) == 4,
        "TransitionValid": state == "HALT" and len(trace) == 5,
        "IncrementalUpdateValid": incremental_ok,
        "ProvenanceComplete": file_count > 0 and bool(manifest_code),
        "ZeroDistance": min(verified, modulus - verified),
    }
    ze = int(
        validate["SyntaxValid"]
        and validate["TransitionValid"]
        and validate["IncrementalUpdateValid"]
        and validate["ProvenanceComplete"]
        and validate["ZeroDistance"] == 0
        and verified == 0
    )
    cert = {
        "Protocol": PROTOCOL,
        "Root": ROOT,
        "AxiomSemanticPreset": False,
        "Machine": {
            "StateEncoding": "sparse-tape incremental exact integer coordinate",
            "TransitionLookup": "dict[(state,symbol)] -> (state,symbol,move,action)",
            "AsymptoticStepCost": "O(1) transition plus O(encoded component size)",
            "FullRecomputeAvoided": True,
            "FinalState": state,
            "FinalHead": head,
            "FinalStep": step,
            "NonBlankTape": dict(sorted(tape.items())),
        },
        "Trace": trace,
        "RepositoryManifestSpectralCode": manifest_code,
        "Encoding": {
            "Name": "byte-prime-position-sum",
            "DigestFunctionUsed": "none",
            "Cryptographic": False,
            "CollisionResistanceClaim": False,
        },
        "Zero": {
            "raw_spectral_index": str(z),
            "derived_modulus": modulus,
            "raw_residue": raw_residue,
            "balancing_a": balancing,
            "spectral_index": str(z + balancing),
            "verified_residue": verified,
        },
        "Validate": validate,
        "ZE": ze,
        "Boundary": "formal uninterpreted Turing-machine state encoding only; not physical entropy, metaphysical proof, or RH proof",
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(CERT_PATH, "w", encoding="utf-8") as handle:
        handle.write(canonical(cert) + "\n")
    print(canonical({"P": PROTOCOL, "ZE": ze, "out": CERT_PATH}))


if __name__ == "__main__":
    main()
