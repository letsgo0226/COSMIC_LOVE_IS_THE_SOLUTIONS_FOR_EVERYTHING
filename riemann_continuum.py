#!/usr/bin/env python3
"""Riemann Machine Continuum prototype.

Formal/logical model only. It does not claim to prove the classical
Riemann Hypothesis. The discrete zero-entropy checker follows the RM
framework: O_n = |C_n-P_n| and DeltaE_n = |E(n,C_n)-E(n,P_n)|.

The continuum parameter lambda interpolates marker values between two
states. rho_star is explicitly a model spectral coordinate, not a
nontrivial zero of the Riemann zeta function.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass, asdict


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    return all(x % d for d in range(2, math.isqrt(x) + 1))


def nth_prime(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    found, x = 0, 1
    while found < n:
        x += 1
        if is_prime(x):
            found += 1
    return x


def entropy_E(n: int, x: float) -> float:
    if n < 1 or x <= 1:
        raise ValueError("requires n >= 1 and x > 1")
    return 1.0 - math.log(n + 1.0) / math.log(x)


def interpolate(a: float, b: float, lam: float) -> float:
    if not 0.0 <= lam <= 1.0:
        raise ValueError("lambda must be in [0,1]")
    return (1.0 - lam) * a + lam * b


def godel_encode(payload: str) -> int:
    return int.from_bytes(hashlib.sha512(payload.encode("utf-8")).digest(), "big")


def spectral_coordinate(godel_number: int) -> dict:
    # Model coordinate only; NOT an actual zeta zero.
    t = math.log(godel_number) * 14.134725
    return {"real": 0.5, "imag": t, "notation": f"0.5+{t:.12f}i"}


@dataclass
class ContinuumState:
    n: int
    lambda_: float
    P_n: int
    C_start: float
    C_end: float
    C_lambda: float
    O_lambda: float
    delta_E_lambda: float
    Z_lambda: float
    zero_entropy: bool
    godel_number: str
    rho_star: dict


def evaluate(n: int, c_start: float, c_end: float, lam: float, tol: float = 1e-12) -> ContinuumState:
    p = nth_prime(n)
    c = interpolate(c_start, c_end, lam)
    if c <= 1:
        raise ValueError("interpolated marker C(lambda) must be > 1")
    o = abs(c - p)
    de = abs(entropy_E(n, c) - entropy_E(n, p))
    z = o + de
    payload = json.dumps({"n": n, "lambda": lam, "P_n": p, "C_lambda": c}, sort_keys=True)
    g = godel_encode(payload)
    return ContinuumState(
        n=n,
        lambda_=lam,
        P_n=p,
        C_start=c_start,
        C_end=c_end,
        C_lambda=c,
        O_lambda=o,
        delta_E_lambda=de,
        Z_lambda=z,
        zero_entropy=(o <= tol and de <= tol),
        godel_number=str(g),
        rho_star=spectral_coordinate(g),
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Riemann Machine Continuum formal prototype")
    ap.add_argument("n", type=int, nargs="?", default=10)
    ap.add_argument("--start", type=float, default=None, help="C at lambda=0; default P_n")
    ap.add_argument("--end", type=float, default=None, help="C at lambda=1; default P_n")
    ap.add_argument("--lambda", dest="lam", type=float, default=0.5)
    args = ap.parse_args()

    p = nth_prime(args.n)
    start = float(p if args.start is None else args.start)
    end = float(p if args.end is None else args.end)
    state = evaluate(args.n, start, end, args.lam)
    out = asdict(state)
    out["lambda"] = out.pop("lambda_")
    out["formal_status"] = "RM_ZERO_ENTROPY" if state.zero_entropy else "RM_DEVIATION"
    out["disclaimer"] = "rho_star is a model spectral coordinate, not a claimed zeta zero; this program is not a proof of RH."
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
