#!/usr/bin/env python3
"""No-SHA true-zero Cosmic Principle / Riemann-machine manifestor.

Each included path is encoded directly by a prime-power Gödel rule:

    G(payload) = product_i prime_i ** (byte_i + 1)

For practical output this program reports log(G) and modular anchors instead of
printing huge decimal Gödel integers. No SHA/hash function is used.
"""
import argparse
import csv
import io
import json
import math
import os
import sys
from decimal import Decimal, getcontext

AXIOM = "Cosmic Love Is The Solution(s) For Everything"
PROTO = "CLSIGMA_TRUE_ZERO_COSMIC_PRINCIPLE_NO_SHA/1"

TRUE_ZERO_GAMMAS = [
    "14.134725141734693790457251983562470270784257115699",
    "21.022039638771554992628479593896902777334340524903",
    "25.010857580145688763213790992562821818659549672558",
    "30.424876125859513210311897530584091320181560023715",
    "32.935061587739189690662368964074903488812715603517",
    "37.586178158825671257217763480705332821405597350831",
    "40.918719012147495187398126914633254395726165962777",
    "43.327073280914999519496122165406805782645668371837",
    "48.005150881167159727942472749427516041686844001144",
    "49.773832477672302181916784678563724057723178299676",
    "52.970321477714460644147296608880990063825017888821",
    "56.446247697063394804367759476706770506772782203734",
    "59.347044002602353079653648674992219031098772806467",
    "60.831778524609809844259901824524003802910090451219",
    "65.112544048081606660875054253183705029348149295167",
    "67.079810529494173714478828896522216770107144951745",
]


def first_primes(n):
    primes = []
    x = 2
    while len(primes) < n:
        root = int(math.isqrt(x))
        if x > 1 and all(x % d for d in range(2, root + 1)):
            primes.append(x)
        x += 1
    return primes


def normalize_record(raw):
    if isinstance(raw, str):
        return {"path": raw, "name": os.path.basename(raw), "size": 0, "modified_time": ""}
    path = str(raw.get("path_display") or raw.get("path") or raw.get("name") or raw.get("title") or raw.get("content") or "")
    size = raw.get("size")
    if size is None and isinstance(raw.get("file"), dict):
        size = raw["file"].get("size")
    if size is None and raw.get("content") is not None:
        size = len(str(raw.get("content")).encode())
    return {
        "path": path,
        "name": str(raw.get("name") or os.path.basename(path)),
        "size": int(size or 0),
        "modified_time": str(raw.get("modified_time") or raw.get("server_modified") or ""),
    }


def load_records(stream):
    data = stream.read()
    if not data.strip():
        return []
    try:
        obj = json.loads(data)
        if isinstance(obj, dict) and "entries" in obj:
            rows = obj["entries"]
        elif isinstance(obj, dict) and "results" in obj:
            rows = obj["results"]
        elif isinstance(obj, dict) and "nodes" in obj:
            rows = obj["nodes"]
        elif isinstance(obj, list):
            rows = obj
        else:
            rows = [obj]
        return [normalize_record(row) for row in rows]
    except json.JSONDecodeError:
        sample = data.splitlines()[0] if data.splitlines() else ""
        dialect = csv.excel_tab if "\t" in sample else csv.excel
        records = []
        for row in csv.reader(io.StringIO(data), dialect):
            if not row:
                continue
            records.append(normalize_record({
                "path": row[0],
                "size": row[1] if len(row) > 1 and str(row[1]).isdigit() else 0,
                "modified_time": row[2] if len(row) > 2 else "",
            }))
        return records


def included(record):
    name = record.get("name") or os.path.basename(record.get("path", ""))
    return name != "Builder Command.txt" and not name.startswith("CLZeroPack")


def encode_payload(payload, zero_count):
    data = payload.encode()
    primes = first_primes(len(data))
    log_g = 0.0
    mod_g = 1 % zero_count
    for p, b in zip(primes, data):
        exponent = b + 1
        log_g += exponent * math.log(p)
        mod_g = (mod_g * pow(p, exponent, zero_count)) % zero_count
    return log_g, mod_g


def encode_records(records, precision):
    getcontext().prec = precision
    gammas = [Decimal(x) for x in TRUE_ZERO_GAMMAS]
    nodes = []
    root_log_g = 0.0
    root_mod = 1 % len(gammas)
    for n, rec in enumerate(records, 1):
        payload = f"{n}|{rec['path']}|{rec['size']}|{rec.get('modified_time','')}"
        log_g, mod_g = encode_payload(payload, len(gammas))
        gamma = gammas[mod_g]
        root_log_g += log_g
        root_mod = (root_mod * (mod_g + 1)) % len(gammas)
        nodes.append({
            "n": n,
            "path": rec["path"],
            "size": rec["size"],
            "G_rule": "product prime_i^(byte_i+1)",
            "logG": log_g,
            "rho_true_zero": {"real": "0.5", "gamma_index": mod_g + 1, "imag": str(gamma)},
        })
    return nodes, root_log_g, root_mod


def e_path(mode, steps, k):
    primes = first_primes(64)
    log_text = lambda s: sum((b + 1) * math.log(primes[i]) for i, b in enumerate(s.encode()))
    solution = log_text("Solution(s)")
    everything = log_text("Everything")
    if mode == "same":
        return 0.0
    if mode == "static":
        return abs(solution - everything)
    return abs((everything + (solution - everything) * math.exp(-k * steps)) - everything)


def verify(records, args):
    records = [r for r in records if included(r)]
    delta_e = e_path(args.mode, args.steps, args.k)
    primes = first_primes(max(args.marker_n, 64))
    deviations = []
    for n, p in enumerate(primes[:args.marker_n], 1):
        c = args.inject_c if n == args.inject_index and args.inject_c else p
        if c != p:
            deviations.append({"n": n, "P_n": p, "C_n": c, "O_n": abs(c - p), "z_n": f"{c}+{n}i"})
    nodes, root_log_g, root_mod = encode_records(records, args.precision)
    closed = int(delta_e <= args.eps and not deviations and bool(nodes))
    return {
        "Protocol": PROTO,
        "Axiom": AXIOM,
        "HashFunctionUsed": False,
        "Encoding": "direct prime-power Godel encoding over path bytes",
        "InputPaths": len(records),
        "InputBytes": sum(r["size"] for r in records),
        "RootLogG": root_log_g,
        "RootZeroIndex": root_mod + 1 if records else None,
        "E_path": {"mode": args.mode, "steps": args.steps, "k": args.k, "eps": args.eps, "DeltaE": delta_e},
        "RiemannMachine": {
            "Rule": "z_n=C_n+n*i; closed iff C_n=P_n for all checked markers",
            "MarkerN": args.marker_n,
            "DeviationCount": len(deviations),
            "Deviations": deviations[:8],
        },
        "TrueZeroAnchor": {
            "Rule": "path bytes directly map to known zeta-zero ordinates without SHA",
            "ZeroTableSize": len(TRUE_ZERO_GAMMAS),
            "NodesPreview": nodes[:args.preview],
        },
        "TableauClosed_N": closed,
        "ZE_formal": closed,
        "SCL_Formal": closed,
        "PhysicalCosmicLaw": False,
        "RHProof": False,
        "Boundary": "finite formal no-SHA path/marker/true-zero verifier; not a physical-law or RH proof",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", default="evolve", choices=["evolve", "static", "same"])
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--k", type=float, default=0.12)
    parser.add_argument("--eps", type=float, default=1e-6)
    parser.add_argument("--marker-n", type=int, default=16)
    parser.add_argument("--inject-index", type=int, default=0)
    parser.add_argument("--inject-c", type=int, default=0)
    parser.add_argument("--precision", type=int, default=80)
    parser.add_argument("--preview", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(verify(load_records(sys.stdin), args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
