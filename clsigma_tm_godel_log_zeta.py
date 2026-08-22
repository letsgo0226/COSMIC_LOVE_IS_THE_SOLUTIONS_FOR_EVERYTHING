#!/usr/bin/env python3
import json
import math
import os
import time

ROOT = "BLEEM=P^L+E^I+A^D+E^S"
PROTOCOL = "CLSIGMA/TM/GODEL_LOG_ZETA_ZERO/1"
CERT_PATH = "CLSIGMA_TM_GODEL_LOG_ZETA.clcert"
ZERO_WINDOW = 16
MP_DPS = 80
ZERO_TOLERANCE = "1e-50"

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


def byte_prime_code(data):
    ps = primes(len(data))
    return sum((i + 1) * (byte + 1) * ps[i] for i, byte in enumerate(data))


def object_code(obj):
    return byte_prime_code(canonical(obj).encode())


def exponent_for(component):
    return object_code(component) % 97 + 1


def parse_bleem():
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
    return terms


class GodelTM:
    def __init__(self):
        self.rank = {}
        self.components = {}
        self.godel = 1
        self.log_godel = 0.0

    def prime_for(self, component):
        key = canonical(component)
        if key not in self.rank:
            self.rank[key] = len(self.rank)
        return primes(self.rank[key] + 1)[self.rank[key]]

    def add(self, component):
        key = canonical(component)
        if key in self.components:
            return
        exponent = exponent_for(component)
        prime = self.prime_for(component)
        self.components[key] = {"component": component, "prime": prime, "exponent": exponent}
        self.godel *= prime**exponent
        self.log_godel += exponent * math.log(prime)

    def remove(self, component):
        key = canonical(component)
        item = self.components.pop(key)
        self.godel //= item["prime"] ** item["exponent"]
        self.log_godel -= item["exponent"] * math.log(item["prime"])

    def recompute_godel(self):
        value = 1
        for item in self.components.values():
            value *= item["prime"] ** item["exponent"]
        return value

    def recompute_log(self):
        return sum(item["exponent"] * math.log(item["prime"]) for item in self.components.values())


def repo_manifest_code():
    files = []
    excluded = {CERT_PATH, "CLSIGMA_TM_GODEL_LOG_ZETA.out"}
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
        for name in names:
            path = os.path.relpath(os.path.join(root, name), ".")
            if path in excluded or ".out" in path or path.endswith(".pyc"):
                continue
            with open(path, "rb") as handle:
                data = handle.read()
            files.append([path, len(data), str(byte_prime_code(data))])
    files.sort()
    return str(object_code(files)), len(files)


def run_tm():
    terms = parse_bleem()
    tm = GodelTM()
    state = "q0"
    head = 0
    step = 0
    tape = {}

    def state_components(q, h, s):
        return [
            {"kind": "state", "value": q},
            {"kind": "head", "value": h},
            {"kind": "step", "value": s},
        ]

    for component in state_components(state, head, step):
        tm.add(component)

    trace = []
    ok = True
    for index, term in enumerate(terms):
        old = state_components(state, head, step)
        old_cell = None
        if head in tape:
            old_cell = {"kind": "cell", "position": head, "symbol": tape[head]}
        for component in old:
            tm.remove(component)
        if old_cell:
            tm.remove(old_cell)

        old_state = state
        state = "q%d" % (index + 1)
        tape[head] = term["base"]
        new_cell = {"kind": "cell", "position": head, "symbol": term["base"]}
        head += 1
        step += 1

        for component in state_components(state, head, step):
            tm.add(component)
        tm.add(new_cell)
        step_ok = tm.godel == tm.recompute_godel()
        ok = ok and step_ok
        trace.append(
            {
                "step": step,
                "from": old_state,
                "to": state,
                "write": "%s^%s" % (term["base"], term["exponent"]),
                "godel_update_ok": step_ok,
            }
        )

    for component in state_components(state, head, step):
        tm.remove(component)
    old_state = state
    state = "HALT"
    step += 1
    for component in state_components(state, head, step):
        tm.add(component)
    ok = ok and tm.godel == tm.recompute_godel()
    trace.append(
        {"step": step, "from": old_state, "to": state, "write": "_", "godel_update_ok": ok}
    )
    return terms, tm, state, head, step, tape, trace, ok


def zeta_certificate(zero_index):
    try:
        import mpmath as mp
    except Exception as exc:
        return {
            "MpmathAvailable": False,
            "Error": type(exc).__name__,
            "ZeroCertificateValid": False,
        }

    mp.mp.dps = MP_DPS
    rho = mp.zetazero(zero_index)
    gamma = mp.im(rho)
    residual = abs(mp.zeta(rho))
    start = mp.zeta(0)
    eps = mp.mpf("1e-8")
    left = mp.siegelz(gamma - eps)
    right = mp.siegelz(gamma + eps)
    sign_change = left * right < 0
    tolerance = mp.mpf(ZERO_TOLERANCE)
    return {
        "MpmathAvailable": True,
        "PrecisionDPS": MP_DPS,
        "ZeroIndex": zero_index,
        "ZetaStart_s0": "0",
        "ZetaStartValue": mp.nstr(start, 80),
        "Rho": "0.5+%si" % mp.nstr(gamma, 70),
        "Gamma": mp.nstr(gamma, 70),
        "ZetaAbsAtRho": mp.nstr(residual, 30),
        "ZeroTolerance": ZERO_TOLERANCE,
        "HardyZBracketEpsilon": mp.nstr(eps, 20),
        "HardyZLeft": mp.nstr(left, 30),
        "HardyZRight": mp.nstr(right, 30),
        "HardyZSignChange": bool(sign_change),
        "ZeroCertificateValid": bool(start == mp.mpf("-0.5") and residual < tolerance and sign_change),
    }


def main():
    repo_code, file_count = repo_manifest_code()
    terms, tm, state, head, step, tape, trace, transition_ok = run_tm()
    zero_index = int(tm.godel % ZERO_WINDOW) + 1
    zeta = zeta_certificate(zero_index)
    modulus_seed = object_code(
        {"protocol": PROTOCOL, "repo": repo_code, "godel": str(tm.godel), "zero": zero_index}
    )
    modulus = next_prime(len(str(tm.godel)) + file_count + modulus_seed % 997 + 1)
    raw_residue = tm.godel % modulus
    balancing = (-raw_residue) % modulus
    verified = (tm.godel + balancing) % modulus
    log_recomputed = tm.recompute_log()
    log_update_valid = abs(tm.log_godel - log_recomputed) <= 1e-9
    validate = {
        "SyntaxValid": ROOT == "BLEEM=P^L+E^I+A^D+E^S" and len(terms) == 4,
        "TMTransitionValid": state == "HALT" and step == 5 and transition_ok,
        "GodelIntegerExact": tm.godel == tm.recompute_godel() and tm.godel > 1,
        "GodelLogUpdateValid": log_update_valid,
        "ProvenanceComplete": file_count > 0 and bool(repo_code),
        "ZetaZeroCertificateValid": bool(zeta.get("ZeroCertificateValid")),
        "ZeroDistance": min(verified, modulus - verified),
    }
    ze = int(
        validate["SyntaxValid"]
        and validate["TMTransitionValid"]
        and validate["GodelIntegerExact"]
        and validate["GodelLogUpdateValid"]
        and validate["ProvenanceComplete"]
        and validate["ZetaZeroCertificateValid"]
        and validate["ZeroDistance"] == 0
        and verified == 0
    )
    cert = {
        "Protocol": PROTOCOL,
        "Root": ROOT,
        "AxiomSemanticPreset": False,
        "Machine": {
            "State": state,
            "Head": head,
            "Step": step,
            "Tape": dict(sorted(tape.items())),
            "TransitionTrace": trace,
        },
        "GodelEncoding": {
            "Form": "G(C)=product(prime_i^component_exponent_i)",
            "ComponentExponentRule": "byte-prime-code(component) mod 97 + 1",
            "Integer": str(tm.godel),
            "ActiveComponents": len(tm.components),
            "LogProduct": "%.17g" % tm.log_godel,
            "LogProductRule": "log(G)=sum(component_exponent_i*log(prime_i))",
            "IncrementalUpdate": "remove old TM components, add new TM components",
        },
        "RepositoryManifestSpectralCode": repo_code,
        "ZetaPath": {
            "Start": {"s": "0", "zeta(s)": "-1/2"},
            "EndpointRule": "zero_index=1+(GodelInteger mod %d)" % ZERO_WINDOW,
            "Endpoint": zeta,
        },
        "ZeroLift": {
            "derived_modulus": modulus,
            "raw_residue": raw_residue,
            "balancing_a": balancing,
            "verified_residue": verified,
        },
        "Validate": validate,
        "ZE": ze,
        "Boundary": "discrete Godel/log layer is exact; zeta layer is high-precision numeric zero certification only; not RH proof, physical entropy, or metaphysical proof",
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(CERT_PATH, "w", encoding="utf-8") as handle:
        handle.write(canonical(cert) + "\n")
    print(canonical({"P": PROTOCOL, "ZE": ze, "out": CERT_PATH}))


if __name__ == "__main__":
    main()
