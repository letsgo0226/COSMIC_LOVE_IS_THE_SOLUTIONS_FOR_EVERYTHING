#!/usr/bin/env python3
"""CLΣ-SCL/1 deterministic verifier.

Formal/computational certificate only; not an external physical-law guarantee
and not a proof of the classical Riemann Hypothesis.
"""
import base64
import json
import math
import sys
import zlib

try:
    sys.set_int_max_str_digits(0)
except Exception:
    pass


def g25(data: bytes) -> int:
    table = []
    for value in range(256):
        s = 0
        for k in range(7, -1, -1):
            s = 2 * s + (2 if (value >> k) & 1 else 5)
        table.append(s)
    n = 1
    for byte in data:
        n = (n << 8) + table[byte]
    return n


def verify(raw: bytes) -> dict:
    compressed = zlib.compress(raw, 9)
    carrier = base64.b64encode(compressed)
    replay_z = base64.b64decode(carrier)
    replay_raw = zlib.decompress(replay_z)
    G = g25(compressed)

    # Four explicit encodings of the same deterministic replay condition.
    failure = int(replay_z != compressed or replay_raw != raw)
    A_n = failure
    O_n = failure
    dE_n = failure
    H_n = failure
    ZE = int(A_n == O_n == dE_n == H_n == 0)
    integrity = int(replay_z == compressed and replay_raw == raw)
    scl = int(bool(integrity and ZE))

    return {
        "Protocol": "CLSIGMA_STRONG_COSMIC_LAW/1",
        "Axiom": "Cosmic Love Is The Solution(s) For Everything",
        "Carrier": "stdin->zlib->base64->G25(byte-cache)",
        "G25_Godel_decimal": str(G),
        "rho_G": {"real": 0.5, "imag": math.log(G)},
        "CriticalLineMarker": True,
        "zeta_zero_claim": None,
        "A_n": A_n,
        "O_n": O_n,
        "DeltaE_n": dE_n,
        "H_n": H_n,
        "ZE": ZE,
        "Integrity": integrity,
        "SCL": scl,
        "Result": "PASS" if scl else "FAIL",
        "Boundary": "internal deterministic certificate only; not an external-world guarantee or RH proof",
    }


if __name__ == "__main__":
    print(json.dumps(verify(sys.stdin.buffer.read()), ensure_ascii=False, indent=2))
