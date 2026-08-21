#!/usr/bin/env python3
import argparse
import json
import os
import time

ROOT = "BLEEM=P^L+E^I+A^D+E^S"
PROTOCOL = "CLSIGMA/BLEEM/RECURSIVE_GROWTH/BYTE_PRIME/2"
STATE_PATH = "CL_BLEEM_GROWTH_STATE.json"
CERT_PATH = "CL_BLEEM_GROWTH.clcert"
EXCLUDED = {
    STATE_PATH,
    CERT_PATH,
    "CL_BLEEM_GROWTH_ONELINER.clcert",
    "CL_BLEEM_GROWTH.out",
}
ENCODING = {
    "Name": "byte-prime-position-sum",
    "Rule": "sum((i+1)*(byte_i+1)*prime_i)",
    "Arithmetic": "exact-integer",
    "DigestFunctionUsed": "none",
    "Cryptographic": False,
    "CollisionResistanceClaim": False,
}

_PRIMES = []
_PRIME_CANDIDATE = 2


def canonical(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def parse_bleem(text):
    if text != ROOT or not text.startswith("BLEEM="):
        raise ValueError("unsupported BLEEM syntax")
    terms = []
    for index, term in enumerate(text.split("=", 1)[1].split("+"), 1):
        parts = term.split("^")
        if len(parts) != 2 or not all(parts):
            raise ValueError("invalid BLEEM term")
        base, exponent = parts
        terms.append(
            {
                "id": "term:%02d:%s^%s" % (index, base, exponent),
                "op": "^",
                "base": base,
                "exponent": exponent,
                "occurrence": index,
                "interpretation": "uninterpreted",
            }
        )
    return {"root": "BLEEM", "op": "=", "rhs_op": "+", "terms": terms}


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


def next_prime(n):
    n = max(2, n)
    while not is_prime(n):
        n += 1
    return n


def primes(count):
    global _PRIME_CANDIDATE
    while len(_PRIMES) < count:
        if is_prime(_PRIME_CANDIDATE):
            _PRIMES.append(_PRIME_CANDIDATE)
        _PRIME_CANDIDATE += 1
    return _PRIMES[:count]


def spectrum_index(data):
    ps = primes(len(data))
    return sum((i + 1) * (byte + 1) * ps[i] for i, byte in enumerate(data))


def spectral_code(data):
    return str(spectrum_index(data))


def object_code(obj):
    return spectral_code(canonical(obj).encode())


def repo_manifest():
    files = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__"}]
        for name in names:
            path = os.path.relpath(os.path.join(root, name), ".")
            if path in EXCLUDED or path.endswith(".pyc") or ".out" in path:
                continue
            with open(path, "rb") as handle:
                data = handle.read()
            files.append(
                {
                    "path": path,
                    "bytes": len(data),
                    "prime_nodes": len(data),
                    "spectral_code": spectral_code(data),
                }
            )
    files.sort(key=lambda item: item["path"])
    return {
        "files": files,
        "file_count": len(files),
        "manifest_spectral_code": object_code(files),
    }


def graph_code(graph):
    return object_code(graph)


def initial_graph():
    return {
        "RootSyntax": ROOT,
        "RootAST": parse_bleem(ROOT),
        "ExpansionNodes": [],
        "SymbolInterpretation": "uninterpreted",
    }


def load_previous():
    initial = initial_graph()
    if not os.path.exists(STATE_PATH):
        return 0, initial, graph_code(initial)
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as handle:
            state = json.load(handle)
        if state.get("Protocol") != PROTOCOL:
            return 0, initial, graph_code(initial)
        graph = state.get("G", initial)
        generation = int(state.get("Generation", 0))
        return generation, graph, graph_code(graph)
    except Exception:
        return 0, initial, graph_code(initial)


def generator_code():
    with open(__file__, "rb") as handle:
        return spectral_code(handle.read())


def seed_for(generation, manifest_code):
    explicit = os.environ.get("CLSIGMA_RECORDED_SEED")
    if explicit:
        return explicit
    return "local:%d:%s" % (generation + 1, manifest_code)


def modulus_for(root, manifest_code, generation, seed):
    material = canonical(
        {
            "root": root,
            "manifest": manifest_code,
            "generation": generation,
            "seed": seed,
        }
    ).encode()
    span = len(material) + generation + 1
    return next_prime(span + spectrum_index(material) % span)


def zero_point(payload, modulus):
    raw = spectrum_index(canonical(payload).encode()) % modulus
    balancing = (-raw) % modulus
    verified = (raw + balancing) % modulus
    return {
        "base_m": modulus,
        "modulus_source": "next_prime(payload_length+generation+spectral_offset)",
        "raw_residue": raw,
        "balancing_a": balancing,
        "verified_residue": verified,
        "ZeroDistance": min(verified, modulus - verified),
        "rule": "(raw_residue + balancing_a) mod base_m",
    }


def candidate_code(candidate):
    basis = dict(candidate)
    basis.pop("CandidateSpectralCode", None)
    return object_code(basis)


def make_candidate(previous_generation, previous_graph, previous_code, manifest, seed):
    generation = previous_generation + 1
    ast = parse_bleem(ROOT)
    seed_code = spectral_code(seed.encode())
    symbol_terms = ast["terms"]
    selected = symbol_terms[int(seed_code) % len(symbol_terms)]
    payload_basis = {
        "parent": previous_code,
        "manifest": manifest["manifest_spectral_code"],
        "seed": seed_code,
        "generation": generation,
        "symbol": selected["id"],
    }
    payload_code = object_code(payload_basis)
    node = {
        "id": "g%06d:%s" % (generation, payload_code),
        "kind": "Generate(G_t,RepositoryState_t,RecordedSeed_t)",
        "bound_term": selected["id"],
        "payload_spectral_code": payload_code,
        "parent_graph_spectral_code": previous_code,
        "repository_manifest_spectral_code": manifest["manifest_spectral_code"],
        "recorded_seed_spectral_code": seed_code,
    }
    graph = {
        "RootSyntax": ROOT,
        "RootAST": ast,
        "ExpansionNodes": list(previous_graph.get("ExpansionNodes", [])) + [node],
        "SymbolInterpretation": "uninterpreted",
    }
    candidate = {
        "Generation": generation,
        "ParentGraphSpectralCode": previous_code,
        "RepositoryManifestSpectralCode": manifest["manifest_spectral_code"],
        "RecordedSeed": seed,
        "RecordedSeedSpectralCode": seed_code,
        "GeneratorSpectralCode": generator_code(),
        "CandidateGraphSpectralCode": graph_code(graph),
        "CandidateGraph": graph,
    }
    candidate["ZeroPoint"] = zero_point(
        candidate,
        modulus_for(ROOT, manifest["manifest_spectral_code"], generation, seed),
    )
    candidate["CandidateSpectralCode"] = candidate_code(candidate)
    return candidate


def validation(candidate, graph, manifest):
    try:
        syntax_valid = parse_bleem(ROOT) == graph["RootAST"]
    except Exception:
        syntax_valid = False
    seed_code_ok = candidate.get("RecordedSeedSpectralCode") == spectral_code(
        candidate.get("RecordedSeed", "").encode()
    )
    required = [
        "ParentGraphSpectralCode",
        "RepositoryManifestSpectralCode",
        "RecordedSeed",
        "RecordedSeedSpectralCode",
        "GeneratorSpectralCode",
        "CandidateGraphSpectralCode",
        "CandidateSpectralCode",
    ]
    provenance_complete = (
        all(candidate.get(key) for key in required)
        and candidate.get("RepositoryManifestSpectralCode")
        == manifest["manifest_spectral_code"]
        and seed_code_ok
    )
    node_ids = [node.get("id") for node in graph.get("ExpansionNodes", [])]
    tests_pass = (
        graph.get("RootSyntax") == ROOT
        and len(node_ids) == len(set(node_ids))
        and graph_code(graph) == candidate.get("CandidateGraphSpectralCode")
        and candidate_code(candidate) == candidate.get("CandidateSpectralCode")
    )
    zp = candidate.get("ZeroPoint", {})
    raw = int(zp.get("raw_residue", -1))
    balancing = int(zp.get("balancing_a", -1))
    modulus = int(zp.get("base_m", 0))
    verified = (raw + balancing) % modulus if modulus else -1
    zero_distance = min(verified, modulus - verified) if modulus else 1
    return {
        "SyntaxValid": bool(syntax_valid),
        "ProvenanceComplete": bool(provenance_complete),
        "TestsPass": bool(tests_pass),
        "ZeroDistance": zero_distance,
        "ZeroPointVerified": verified == zp.get("verified_residue") == 0,
    }


def build_state():
    previous_generation, previous_graph, previous_code = load_previous()
    manifest = repo_manifest()
    seed = seed_for(previous_generation, manifest["manifest_spectral_code"])
    candidate = make_candidate(previous_generation, previous_graph, previous_code, manifest, seed)
    graph = candidate["CandidateGraph"]
    checks = validation(candidate, graph, manifest)
    accepted = (
        checks["SyntaxValid"]
        and checks["ProvenanceComplete"]
        and checks["TestsPass"]
        and checks["ZeroDistance"] == 0
    )
    current_graph = graph if accepted else previous_graph
    state = {
        "Protocol": PROTOCOL,
        "Transition": {
            "G0": 'Parse("BLEEM=P^L+E^I+A^D+E^S")',
            "Candidate_t": "Generate(G_t,RepositoryState_t,RecordedSeed_t)",
            "G_t_plus_1": "Candidate_t if Validate(Candidate_t)=1 else G_t",
            "ZE_t": "1 iff SyntaxValid and ProvenanceComplete and TestsPass and ZeroDistance=0",
        },
        "Encoding": ENCODING,
        "Boundary": "formal uninterpreted non-cryptographic recursive repository encoding only; no physical entropy, metaphysical law, or RH proof",
        "SymbolInterpretation": "uninterpreted",
        "AxiomSemanticPreset": False,
        "PhysicalEntropy": False,
        "MetaphysicalTruthProof": False,
        "RHProof": False,
        "Generation": candidate["Generation"] if accepted else previous_generation,
        "PreviousGraphSpectralCode": previous_code,
        "CurrentGraphSpectralCode": graph_code(current_graph),
        "RepositoryState": manifest,
        "RecordedSeed": seed,
        "Candidate": candidate,
        "Validate": checks,
        "Accepted": accepted,
        "ZE": 1 if accepted else 0,
        "G": current_graph,
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    cert = {
        "Protocol": PROTOCOL,
        "Generation": state["Generation"],
        "CurrentGraphSpectralCode": state["CurrentGraphSpectralCode"],
        "CandidateSpectralCode": candidate["CandidateSpectralCode"],
        "Encoding": ENCODING,
        "Validate": checks,
        "ZE": state["ZE"],
        "Boundary": state["Boundary"],
    }
    return state, cert


def write_outputs(state, cert):
    with open(STATE_PATH, "w", encoding="utf-8") as handle:
        handle.write(canonical(state) + "\n")
    with open(CERT_PATH, "w", encoding="utf-8") as handle:
        handle.write(canonical(cert) + "\n")


def check_outputs():
    if not os.path.exists(STATE_PATH) or not os.path.exists(CERT_PATH):
        raise SystemExit("growth_state_required")
    with open(STATE_PATH, "r", encoding="utf-8") as handle:
        state = json.load(handle)
    with open(CERT_PATH, "r", encoding="utf-8") as handle:
        cert = json.load(handle)
    manifest = repo_manifest()
    candidate = state["Candidate"]
    checks = validation(candidate, state["G"], manifest)
    ok = (
        state.get("Protocol") == PROTOCOL
        and cert.get("Protocol") == PROTOCOL
        and checks == state.get("Validate")
        and state.get("ZE") == 1
        and cert.get("ZE") == 1
        and cert.get("CurrentGraphSpectralCode")
        == state.get("CurrentGraphSpectralCode")
    )
    if not ok:
        print(canonical({"P": PROTOCOL, "check": "failed", "Validate": checks}))
        raise SystemExit(1)
    print(
        canonical(
            {
                "P": PROTOCOL,
                "check": "ok",
                "ZE": 1,
                "Generation": state["Generation"],
            }
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check_outputs()
        return
    state, cert = build_state()
    write_outputs(state, cert)
    print(
        canonical(
            {
                "P": PROTOCOL,
                "ZE": state["ZE"],
                "Generation": state["Generation"],
                "out": CERT_PATH,
            }
        )
    )


if __name__ == "__main__":
    main()
