#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time

ROOT = "BLEEM=P^L+E^I+A^D+E^S"
PROTOCOL = "CLSIGMA/BLEEM/RECURSIVE_GROWTH/1"
STATE_PATH = "CL_BLEEM_GROWTH_STATE.json"
CERT_PATH = "CL_BLEEM_GROWTH.clcert"
EXCLUDED = {
    STATE_PATH,
    CERT_PATH,
    "CL_BLEEM_GROWTH.out",
}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


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
    out = []
    n = 2
    while len(out) < count:
        if is_prime(n):
            out.append(n)
        n += 1
    return out


def spectrum_index(data):
    ps = primes(len(data))
    return sum((i + 1) * (b + 1) * ps[i] for i, b in enumerate(data))


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
                    "sha256": sha256_bytes(data),
                }
            )
    files.sort(key=lambda item: item["path"])
    return {
        "files": files,
        "file_count": len(files),
        "manifest_hash": sha256_bytes(canonical(files).encode()),
    }


def graph_hash(graph):
    return sha256_bytes(canonical(graph).encode())


def load_previous():
    ast = parse_bleem(ROOT)
    initial = {
        "RootSyntax": ROOT,
        "RootAST": ast,
        "ExpansionNodes": [],
        "SymbolInterpretation": "uninterpreted",
    }
    if not os.path.exists(STATE_PATH):
        return 0, initial, graph_hash(initial)
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as handle:
            state = json.load(handle)
        graph = state.get("G", initial)
        generation = int(state.get("Generation", 0))
        return generation, graph, graph_hash(graph)
    except Exception:
        return 0, initial, graph_hash(initial)


def generator_hash():
    with open(__file__, "rb") as handle:
        return sha256_bytes(handle.read())


def seed_for(generation, manifest_hash):
    explicit = os.environ.get("CLSIGMA_RECORDED_SEED")
    if explicit:
        return explicit
    return "local:%d:%s" % (generation + 1, manifest_hash)


def modulus_for(root, manifest_hash, generation, seed):
    digest = sha256_bytes((root + manifest_hash + seed).encode())
    return next_prime(len(root) + generation + 3 + (int(digest[:6], 16) % 997))


def zero_point(payload, modulus):
    raw = spectrum_index(canonical(payload).encode()) % modulus
    balancing = (-raw) % modulus
    verified = (raw + balancing) % modulus
    return {
        "base_m": modulus,
        "raw_residue": raw,
        "balancing_a": balancing,
        "verified_residue": verified,
        "ZeroDistance": min(verified, modulus - verified),
        "rule": "(raw_residue + balancing_a) mod base_m",
    }


def make_candidate(previous_generation, previous_graph, previous_hash, manifest, seed):
    generation = previous_generation + 1
    ast = parse_bleem(ROOT)
    seed_hash = sha256_bytes(seed.encode())
    symbol_terms = ast["terms"]
    selected = symbol_terms[int(seed_hash[:8], 16) % len(symbol_terms)]
    payload_basis = {
        "parent": previous_hash,
        "manifest": manifest["manifest_hash"],
        "seed": seed_hash,
        "generation": generation,
        "symbol": selected["id"],
    }
    payload_hash = sha256_bytes(canonical(payload_basis).encode())
    node = {
        "id": "g%06d:%s" % (generation, payload_hash[:16]),
        "kind": "Generate(G_t,RepositoryState_t,RecordedSeed_t)",
        "bound_term": selected["id"],
        "payload_hash": payload_hash,
        "parent_graph_hash": previous_hash,
        "repository_manifest_hash": manifest["manifest_hash"],
        "recorded_seed_hash": seed_hash,
    }
    graph = {
        "RootSyntax": ROOT,
        "RootAST": ast,
        "ExpansionNodes": list(previous_graph.get("ExpansionNodes", [])) + [node],
        "SymbolInterpretation": "uninterpreted",
    }
    candidate = {
        "Generation": generation,
        "ParentGraphHash": previous_hash,
        "RepositoryManifestHash": manifest["manifest_hash"],
        "RecordedSeed": seed,
        "RecordedSeedHash": seed_hash,
        "GeneratorHash": generator_hash(),
        "CandidateGraphHash": graph_hash(graph),
        "CandidateGraph": graph,
    }
    candidate["ZeroPoint"] = zero_point(
        candidate, modulus_for(ROOT, manifest["manifest_hash"], generation, seed)
    )
    candidate["CandidateHash"] = sha256_bytes(canonical(candidate).encode())
    return candidate


def validation(candidate, graph, manifest):
    try:
        syntax_valid = parse_bleem(ROOT) == graph["RootAST"]
    except Exception:
        syntax_valid = False
    seed_hash_ok = candidate.get("RecordedSeedHash") == sha256_bytes(
        candidate.get("RecordedSeed", "").encode()
    )
    provenance_complete = all(
        candidate.get(key)
        for key in [
            "ParentGraphHash",
            "RepositoryManifestHash",
            "RecordedSeed",
            "RecordedSeedHash",
            "GeneratorHash",
            "CandidateGraphHash",
        ]
    ) and candidate.get("RepositoryManifestHash") == manifest["manifest_hash"] and seed_hash_ok
    node_ids = [node.get("id") for node in graph.get("ExpansionNodes", [])]
    tests_pass = (
        graph.get("RootSyntax") == ROOT
        and len(node_ids) == len(set(node_ids))
        and graph_hash(graph) == candidate.get("CandidateGraphHash")
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
    previous_generation, previous_graph, previous_hash = load_previous()
    manifest = repo_manifest()
    seed = seed_for(previous_generation, manifest["manifest_hash"])
    candidate = make_candidate(previous_generation, previous_graph, previous_hash, manifest, seed)
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
        "Boundary": "formal uninterpreted recursive repository encoding only; no physical entropy, metaphysical law, or RH proof",
        "SymbolInterpretation": "uninterpreted",
        "AxiomSemanticPreset": False,
        "PhysicalEntropy": False,
        "MetaphysicalTruthProof": False,
        "RHProof": False,
        "Generation": candidate["Generation"] if accepted else previous_generation,
        "PreviousGraphHash": previous_hash,
        "CurrentGraphHash": graph_hash(current_graph),
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
        "CurrentGraphHash": state["CurrentGraphHash"],
        "CandidateHash": candidate["CandidateHash"],
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
        and cert.get("CurrentGraphHash") == state.get("CurrentGraphHash")
    )
    if not ok:
        print(canonical({"P": PROTOCOL, "check": "failed", "Validate": checks}))
        raise SystemExit(1)
    print(canonical({"P": PROTOCOL, "check": "ok", "ZE": 1, "Generation": state["Generation"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check_outputs()
        return
    state, cert = build_state()
    write_outputs(state, cert)
    print(canonical({"P": PROTOCOL, "ZE": state["ZE"], "Generation": state["Generation"], "out": CERT_PATH}))


if __name__ == "__main__":
    main()
