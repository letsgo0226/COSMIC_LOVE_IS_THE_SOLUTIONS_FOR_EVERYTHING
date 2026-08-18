#!/usr/bin/env python3
"""Riemann Machine Zero-Entropy Equivalence Verifier.

Executable formalization of the logical framework in
"The Riemann Machine Zero-Entropy Equivalence Theorem".

IMPORTANT: RM is an explicit marking-rule axiom. This program therefore
verifies the internal equivalence structure of the formal Riemann Machine;
it does not constitute an analytic proof of the classical Riemann Hypothesis.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    return all(x % d for d in range(3, math.isqrt(x) + 1, 2))


def nth_prime(n: int) -> int:
    if n < 1:
        raise ValueError("n must be >= 1")
    count, x = 0, 1
    while count < n:
        x += 1
        if is_prime(x):
            count += 1
    return x


def E(n: int, x: int) -> float:
    """E(n,x) = 1 - log(n+1)/log(x), defined for n>=1 and x>1."""
    if n < 1 or x <= 1:
        raise ValueError("E requires n >= 1 and x > 1")
    return 1.0 - math.log(n + 1) / math.log(x)


@dataclass(frozen=True)
class State:
    n: int
    P_n: int
    C_n: int
    beta_n: float
    A_n: float
    O_n: int
    delta_E_n: float
    analytic_zero: bool
    offset_zero: bool
    exponential_zero: bool
    marker_zero: bool
    RM_holds: bool
    equivalence_holds: bool


def verify(n: int, C_n: int | None = None, beta_n: float = 0.5,
           tol: float = 1e-12) -> State:
    """Evaluate one formal Riemann-Machine marker.

    A_n = |beta_n - 1/2|
    O_n = |C_n - P_n|
    DeltaE_n = |E(n,C_n) - E(n,P_n)|

    RM: A_n = 0 iff O_n = 0.
    """
    P_n = nth_prime(n)
    if C_n is None:
        C_n = P_n
    if C_n <= 1:
        raise ValueError("C_n must be > 1")

    A_n = abs(beta_n - 0.5)
    O_n = abs(C_n - P_n)
    delta_E_n = abs(E(n, C_n) - E(n, P_n))

    analytic_zero = A_n <= tol
    offset_zero = O_n == 0
    exponential_zero = delta_E_n <= tol
    marker_zero = C_n == P_n

    # Formal marking rule RM from the paper.
    RM_holds = analytic_zero == offset_zero
    equivalence_holds = (
        RM_holds
        and analytic_zero == offset_zero
        and offset_zero == exponential_zero
        and exponential_zero == marker_zero
    )

    return State(
        n=n,
        P_n=P_n,
        C_n=C_n,
        beta_n=beta_n,
        A_n=A_n,
        O_n=O_n,
        delta_E_n=delta_E_n,
        analytic_zero=analytic_zero,
        offset_zero=offset_zero,
        exponential_zero=exponential_zero,
        marker_zero=marker_zero,
        RM_holds=RM_holds,
        equivalence_holds=equivalence_holds,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the formal Riemann Machine zero-entropy equivalence."
    )
    parser.add_argument("-n", type=int, default=1, help="ordinal index (>=1)")
    parser.add_argument("-c", "--marker", type=int, default=None,
                        help="C_n; defaults to P_n")
    parser.add_argument("--beta", type=float, default=0.5,
                        help="formal Re(rho_n); default 0.5")
    parser.add_argument("--tol", type=float, default=1e-12)
    args = parser.parse_args()

    state = verify(args.n, args.marker, args.beta, args.tol)
    payload = {
        "protocol": "CLZeroPack/RiemannMachine-ZeroEntropy-Equivalence/1",
        "theorem": "A_n=0 <=> O_n=0 <=> DeltaE_n=0 <=> C_n=P_n",
        "RM": "A_n=0 <=> O_n=0 (formal marking-rule axiom)",
        "state": asdict(state),
        "scope": "logical/formal equivalence; not a proof of classical RH",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
