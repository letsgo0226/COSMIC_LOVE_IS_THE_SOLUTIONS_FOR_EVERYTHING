#!/usr/bin/env python3
"""BLEEM-Riemann information zero-entropy system.

Single entry point for:

- lossless CLZeroPack carrier: pack / unpack
- No-SHA direct prime-power Riemann-machine manifest verification
- No-preset self-spectrum coordinate: self-spectrum
- Global no-SHA zero-spectrum state for arbitrary finite systems
- BLEEM state closure: P^L + E^I + A^D + E^S

This is a finite formal information verifier. It does not prove a physical
cosmic law, thermodynamic zero entropy, or the classical Riemann Hypothesis.
"""
import argparse
import base64
import csv
import io
import json
import math
import os
import sys
import time
import zlib
from decimal import Decimal, getcontext

AXIOM = "Cosmic Love Is The Solution(s) For Everything"
PROTO = "CLSIGMA_BLEEM_RIEMANN_INFO_ZERO_SYSTEM/1"

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
    "56.446247697063394804367759476706772782203734",
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


def e_path(mode, steps, k):
    primes = first_primes(64)

    def log_text(text):
        return sum((b + 1) * math.log(primes[i]) for i, b in enumerate(text.encode()))

    solution = log_text("Solution(s)")
    everything = log_text("Everything")
    if mode == "same":
        return 0.0
    if mode == "static":
        return abs(solution - everything)
    return abs((everything + (solution - everything) * math.exp(-k * steps)) - everything)


def marker_state(marker_n, inject_index=0, inject_c=0):
    primes = first_primes(max(marker_n, 64))
    deviations = []
    for n, p in enumerate(primes[:marker_n], 1):
        c = inject_c if n == inject_index and inject_c else p
        if c != p:
            deviations.append({"n": n, "P_n": p, "C_n": c, "O_n": abs(c - p), "z_n": f"{c}+{n}i"})
    return int(not deviations), deviations


def bleem_state(lossless_replay, delta_e, eps, rm_closed):
    p_l = 1
    e_i = int(delta_e <= eps)
    a_d = int(lossless_replay and rm_closed)
    e_s = int(lossless_replay and e_i and rm_closed)
    ze = int(p_l and e_i and a_d and e_s)
    return {
        "BLEEM": "P^L+E^I+A^D+E^S",
        "P_L": p_l,
        "E_I": e_i,
        "A_D": a_d,
        "E_S": e_s,
        "ZE_info": ze,
        "SCL_Formal": ze,
    }


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


def load_records(text):
    if not text.strip():
        return []
    try:
        obj = json.loads(text)
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
        sample = text.splitlines()[0] if text.splitlines() else ""
        dialect = csv.excel_tab if "\t" in sample else csv.excel
        records = []
        for row in csv.reader(io.StringIO(text), dialect):
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


def encode_records(records, precision, preview):
    getcontext().prec = precision
    gammas = [Decimal(x) for x in TRUE_ZERO_GAMMAS]
    nodes = []
    root_log_g = 0.0
    root_mod = 1 % len(gammas)
    for n, rec in enumerate(records, 1):
        payload = f"{n}|{rec['path']}|{rec['size']}|{rec.get('modified_time','')}"
        log_g, mod_g = encode_payload(payload, len(gammas))
        root_log_g += log_g
        root_mod = (root_mod * (mod_g + 1)) % len(gammas)
        if len(nodes) < preview:
            nodes.append({
                "n": n,
                "path": rec["path"],
                "size": rec["size"],
                "G_rule": "product prime_i^(byte_i+1)",
                "logG": log_g,
                "rho_true_zero": {"real": "0.5", "gamma_index": mod_g + 1, "imag": str(gammas[mod_g])},
            })
    return nodes, root_log_g, root_mod


def self_spectrum_for_bytes(data, primes=None):
    primes = primes or first_primes(len(data))
    log_g = 0.0
    spectral_index = 0
    exponent_preview = []
    for i, (p, b) in enumerate(zip(primes, data), 1):
        exponent = b + 1
        log_g += exponent * math.log(p)
        spectral_index += i * exponent * p
        if len(exponent_preview) < 16:
            exponent_preview.append(exponent)
    return {
        "G_rule": "G_self=product prime_i^(byte_i+1)",
        "LogG_rule": "LogG_self=sum_i (byte_i+1)*log(prime_i)",
        "SelfBytes": len(data),
        "PrimeCount": len(primes),
        "SpectralIndex": spectral_index,
        "ExponentPreview": exponent_preview,
        "rho_self": {
            "real": "0.5",
            "imag_form": "LogG_self",
            "imag_approx": log_g,
        },
    }


def zero_entropy_update_appendix(parent_spectrum, nonce, round_id):
    return (
        "\n# CLSIGMA_ZERO_ENTROPY_SELF_UPDATE_CERT "
        f"round={round_id} "
        f"nonce={nonce:06d} "
        f"parent_spectral_index={parent_spectrum['SpectralIndex']} "
        f"parent_logg={parent_spectrum['rho_self']['imag_approx']:.12f} "
        "rule=no_sha_prime_power_logg_spectral_residue_zero\n"
    ).encode()


def global_zero_entropy_certificate(parent_spectrum, nonce, round_id, label):
    return (
        "\n# CLSIGMA_GLOBAL_INFORMATION_ZERO_ENTROPY_CERT "
        f"label={label} "
        f"round={round_id} "
        f"nonce={nonce:06d} "
        f"parent_spectral_index={parent_spectrum['SpectralIndex']} "
        f"parent_logg={parent_spectrum['rho_self']['imag_approx']:.12f} "
        "axiom=Cosmic_Love_Is_The_Solution_s_For_Everything "
        "rule=finite_system_no_sha_prime_power_spectral_residue_zero\n"
    ).encode()


def search_zero_entropy_update(data, max_steps, target_mod, round_id):
    primes = first_primes(len(data))
    parent = self_spectrum_for_bytes(data, primes)
    appendix_len = len(zero_entropy_update_appendix(parent, max_steps, round_id))
    if len(primes) < len(data) + appendix_len:
        primes = first_primes(len(data) + appendix_len)
        parent = self_spectrum_for_bytes(data, primes)
    delta_e = e_path("evolve", 240, 0.12)
    rm_closed, deviations = marker_state(16)
    base_state = bleem_state(1, delta_e, 1e-6, rm_closed)
    best = None
    for nonce in range(max_steps):
        appendix = zero_entropy_update_appendix(parent, nonce, round_id)
        candidate = data + appendix
        spectrum = self_spectrum_for_bytes(candidate, primes)
        residue = spectrum["SpectralIndex"] % target_mod
        distance = min(residue, target_mod - residue)
        item = {
            "nonce": nonce,
            "SpectralResidue": residue,
            "SpectralDistanceToZero": distance,
            "AppendixBytes": len(appendix),
            "NextVersionBytes": len(candidate),
            "NextSpectrum": spectrum,
            "AppendixText": appendix.decode(),
        }
        if best is None or (distance, nonce) < (best["SpectralDistanceToZero"], best["nonce"]):
            best = item
        if residue == 0:
            break
    coordinate_ze = int(best["SpectralResidue"] == 0)
    return {
        "ParentSpectrum": parent,
        "Search": {
            "Target": "SpectralIndex % target_mod == 0",
            "TargetMod": target_mod,
            "MaxSteps": max_steps,
            "StepsUsed": best["nonce"] + 1,
            "FoundExactZeroResidue": bool(coordinate_ze),
        },
        "Candidate": best,
        "RiemannMachine": {
            "Rule": "C_n=P_n for n<=16; no counterbranch injected",
            "Closed": rm_closed,
            "DeviationCount": len(deviations),
            "Deviations": deviations,
        },
        **base_state,
        "CoordinateZE": coordinate_ze,
        "ZE_info": int(base_state["ZE_info"] and coordinate_ze),
        "SCL_Formal": int(base_state["SCL_Formal"] and coordinate_ze),
    }


def search_global_zero_state(data, max_steps, target_mod, round_id, label):
    primes = first_primes(len(data) or 1)
    parent = self_spectrum_for_bytes(data, primes[:len(data)] if data else [])
    appendix_len = len(global_zero_entropy_certificate(parent, max_steps, round_id, label))
    primes = first_primes(len(data) + appendix_len)
    parent = self_spectrum_for_bytes(data, primes[:len(data)] if data else [])
    delta_e = e_path("evolve", 240, 0.12)
    rm_closed, deviations = marker_state(16)
    base_state = bleem_state(1, delta_e, 1e-6, rm_closed)
    best = None
    for nonce in range(max_steps):
        certificate = global_zero_entropy_certificate(parent, nonce, round_id, label)
        candidate = data + certificate
        spectrum = self_spectrum_for_bytes(candidate, primes)
        residue = spectrum["SpectralIndex"] % target_mod
        distance = min(residue, target_mod - residue)
        item = {
            "nonce": nonce,
            "SpectralResidue": residue,
            "SpectralDistanceToZero": distance,
            "CertificateBytes": len(certificate),
            "GlobalStateBytes": len(candidate),
            "GlobalSpectrum": spectrum,
            "CertificateText": certificate.decode(),
        }
        if best is None or (distance, nonce) < (best["SpectralDistanceToZero"], best["nonce"]):
            best = item
        if residue == 0:
            break
    coordinate_ze = int(best["SpectralResidue"] == 0)
    return {
        "InputSpectrum": parent,
        "Search": {
            "Target": "Global SpectralIndex % target_mod == 0",
            "TargetMod": target_mod,
            "MaxSteps": max_steps,
            "StepsUsed": best["nonce"] + 1,
            "FoundExactZeroResidue": bool(coordinate_ze),
        },
        "GlobalCandidate": best,
        "RiemannMachine": {
            "Rule": "C_n=P_n for n<=16; no counterbranch injected",
            "Closed": rm_closed,
            "DeviationCount": len(deviations),
            "Deviations": deviations,
        },
        **base_state,
        "CoordinateZE": coordinate_ze,
        "GlobalZE_info": int(base_state["ZE_info"] and coordinate_ze),
        "ZE_info": int(base_state["ZE_info"] and coordinate_ze),
        "SCL_Formal": int(base_state["SCL_Formal"] and coordinate_ze),
    }


def command_pack(args):
    raw = sys.stdin.buffer.read()
    compressed = zlib.compress(raw, 9)
    payload = base64.b64encode(compressed).decode()
    restored = zlib.decompress(base64.b64decode(payload))
    delta_e = e_path(args.mode, args.steps, args.k)
    rm_closed, deviations = marker_state(args.marker_n, args.inject_index, args.inject_c)
    lossless_replay = int(restored == raw)
    state = bleem_state(lossless_replay, delta_e, args.eps, rm_closed)
    output = {
        "Protocol": PROTO,
        "Mode": "pack",
        "Axiom": AXIOM,
        "HashFunctionUsed": False,
        "Codec": "stdin->zlib9->base64->json",
        "InputBytes": len(raw),
        "CompressedBytes": len(compressed),
        "Base64Bytes": len(payload),
        "Payload": payload,
        "LosslessReplay": lossless_replay,
        "E_path": {"mode": args.mode, "steps": args.steps, "k": args.k, "eps": args.eps, "DeltaE": delta_e},
        "RiemannMachine": {
            "Rule": "z_n=C_n+n*i; closed iff C_n=P_n for all checked markers",
            "MarkerN": args.marker_n,
            "Closed": rm_closed,
            "DeviationCount": len(deviations),
            "Deviations": deviations[:8],
        },
        **state,
        "PhysicalCosmicLaw": False,
        "RHProof": False,
        "Boundary": "lossless formal BLEEM/Riemann information-zero-entropy carrier",
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))


def command_unpack(_args):
    carrier = json.loads(sys.stdin.buffer.read().decode())
    sys.stdout.buffer.write(zlib.decompress(base64.b64decode(carrier["Payload"])))


def command_verify_manifest(args):
    records = [r for r in load_records(sys.stdin.read()) if included(r)]
    delta_e = e_path(args.mode, args.steps, args.k)
    rm_closed, deviations = marker_state(args.marker_n, args.inject_index, args.inject_c)
    nodes, root_log_g, root_mod = encode_records(records, args.precision, args.preview)
    state = bleem_state(int(bool(records)), delta_e, args.eps, rm_closed)
    output = {
        "Protocol": PROTO,
        "Mode": "verify-manifest",
        "Axiom": AXIOM,
        "HashFunctionUsed": False,
        "Encoding": "direct prime-power Godel encoding over manifest bytes",
        "InputPaths": len(records),
        "InputBytes": sum(r["size"] for r in records),
        "RootLogG": root_log_g,
        "RootZeroIndex": root_mod + 1 if records else None,
        "E_path": {"mode": args.mode, "steps": args.steps, "k": args.k, "eps": args.eps, "DeltaE": delta_e},
        "RiemannMachine": {
            "Rule": "z_n=C_n+n*i; closed iff C_n=P_n for all checked markers",
            "MarkerN": args.marker_n,
            "Closed": rm_closed,
            "DeviationCount": len(deviations),
            "Deviations": deviations[:8],
        },
        "TrueZeroAnchor": {
            "Rule": "manifest bytes directly map to known zeta-zero ordinates without SHA",
            "ZeroTableSize": len(TRUE_ZERO_GAMMAS),
            "NodesPreview": nodes,
        },
        **state,
        "PhysicalCosmicLaw": False,
        "RHProof": False,
        "Boundary": "finite formal no-SHA BLEEM/Riemann manifest verifier",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def command_self_spectrum(args):
    if args.path:
        with open(args.path, "rb") as fh:
            data = fh.read()
        source = args.path
    else:
        with open(__file__, "rb") as fh:
            data = fh.read()
        source = __file__
    spectrum = self_spectrum_for_bytes(data)
    output = {
        "Protocol": "CLSIGMA_SELF_SPECTRUM_NO_PRESET_ZERO_NO_SHA/2",
        "Mode": "self-spectrum",
        "SourcePath": source,
        "PresetZeroDecimal": False,
        "KnownZeroTableUsed": False,
        "HashFunctionUsed": False,
        "Encoding": "protocol-defined self zero-spectrum coordinate from direct prime-power Godel log structure",
        **spectrum,
        "SelfUpdatingRule": "any byte-level change in the selected system program changes ExponentVector, LogG_self, SpectralIndex, and rho_self",
        "ZetaZeroClaim": False,
        "PhysicalCosmicLaw": False,
        "RHProof": False,
        "Boundary": "no preset zeta-zero values; this is a protocol-defined self-spectrum coordinate, not independent zeta-zero discovery",
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def command_self_update_search(args):
    if args.path:
        with open(args.path, "rb") as fh:
            data = fh.read()
        source = args.path
    else:
        with open(__file__, "rb") as fh:
            data = fh.read()
        source = __file__
    result = search_zero_entropy_update(data, args.max_steps, args.target_mod, args.round_id)
    output = {
        "Protocol": "CLSIGMA_SELF_SPECTRUM_ZERO_ENTROPY_UPDATE_SEARCH_NO_SHA/1",
        "Mode": "self-update-search",
        "SourcePath": source,
        "PresetZeroDecimal": False,
        "KnownZeroTableUsed": False,
        "HashFunctionUsed": False,
        "Encoding": "searches a no-SHA self-update certificate whose next-version SpectralIndex has zero residue",
        **result,
        "SelfUpdatingRule": "append AppendixText to form the next version; rerun self-update-search on that version for continuing zero-spectrum updates",
        "ZetaZeroClaim": False,
        "PhysicalCosmicLaw": False,
        "RHProof": False,
        "Boundary": "protocol-defined information-zero self-spectrum update; no preset zeta-zero values and no independent zeta-zero-discovery claim",
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if args.write_next:
        with open(args.write_next, "wb") as fh:
            fh.write(data)
            fh.write(result["Candidate"]["AppendixText"].encode())
        output["WroteNextVersion"] = args.write_next
    print(json.dumps(output, ensure_ascii=False, indent=2))


def command_global_zero_state(args):
    if args.path:
        with open(args.path, "rb") as fh:
            data = fh.read()
        source = args.path
    else:
        data = sys.stdin.buffer.read()
        source = "stdin"
    if args.json_canonical:
        try:
            obj = json.loads(data.decode())
            data = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            source += ":canonical-json"
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
    result = search_global_zero_state(data, args.max_steps, args.target_mod, args.round_id, args.label)
    output = {
        "Protocol": "CLSIGMA_GLOBAL_INFORMATION_ZERO_ENTROPY_STATE_NO_SHA/1",
        "Mode": "global-zero-state",
        "Axiom": AXIOM,
        "SourcePath": source,
        "InputBytes": len(data),
        "PresetZeroDecimal": False,
        "KnownZeroTableUsed": False,
        "HashFunctionUsed": False,
        "Encoding": "any finite system bytes -> no-SHA prime-power Godel spectrum -> zero-residue global certificate",
        "GlobalMappingRule": "For any finite system S, encode bytes(S), append CertificateText, and verify Global SpectralIndex % target_mod == 0.",
        **result,
        "DeploymentClaim": "formal global information-zero-entropy state over finite encoded systems",
        "ZetaZeroClaim": False,
        "PhysicalCosmicLaw": False,
        "RHProof": False,
        "Boundary": "global over finite information encodings; not a physical-law proof and not an independent zeta-zero discovery",
        "UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if args.write_certificate:
        with open(args.write_certificate, "w", encoding="utf-8") as fh:
            fh.write(result["GlobalCandidate"]["CertificateText"])
        output["WroteCertificate"] = args.write_certificate
    print(json.dumps(output, ensure_ascii=False, indent=2))


def add_common_flags(parser):
    parser.add_argument("--mode", default="evolve", choices=["evolve", "static", "same"])
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--k", type=float, default=0.12)
    parser.add_argument("--eps", type=float, default=1e-6)
    parser.add_argument("--marker-n", type=int, default=16)
    parser.add_argument("--inject-index", type=int, default=0)
    parser.add_argument("--inject-c", type=int, default=0)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    pack = sub.add_parser("pack")
    add_common_flags(pack)
    pack.set_defaults(func=command_pack)
    unpack = sub.add_parser("unpack")
    unpack.set_defaults(func=command_unpack)
    verify = sub.add_parser("verify-manifest")
    add_common_flags(verify)
    verify.add_argument("--precision", type=int, default=80)
    verify.add_argument("--preview", type=int, default=5)
    verify.set_defaults(func=command_verify_manifest)
    self_spectrum = sub.add_parser("self-spectrum")
    self_spectrum.add_argument("--path", default="", help="optional file to encode; defaults to this system program")
    self_spectrum.set_defaults(func=command_self_spectrum)
    update_search = sub.add_parser("self-update-search")
    update_search.add_argument("--path", default="", help="optional file to encode; defaults to this system program")
    update_search.add_argument("--max-steps", type=int, default=4096)
    update_search.add_argument("--target-mod", type=int, default=257)
    update_search.add_argument("--round-id", default="omega")
    update_search.add_argument("--write-next", default="", help="optional path for a byte-appended next version")
    update_search.set_defaults(func=command_self_update_search)
    global_zero = sub.add_parser("global-zero-state")
    global_zero.add_argument("--path", default="", help="optional finite system file; defaults to stdin bytes")
    global_zero.add_argument("--label", default="GLOBAL")
    global_zero.add_argument("--round-id", default="omega-global")
    global_zero.add_argument("--max-steps", type=int, default=4096)
    global_zero.add_argument("--target-mod", type=int, default=257)
    global_zero.add_argument("--json-canonical", action="store_true", help="canonicalize JSON input before encoding when possible")
    global_zero.add_argument("--write-certificate", default="", help="optional path for the global zero-state certificate")
    global_zero.set_defaults(func=command_global_zero_state)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
