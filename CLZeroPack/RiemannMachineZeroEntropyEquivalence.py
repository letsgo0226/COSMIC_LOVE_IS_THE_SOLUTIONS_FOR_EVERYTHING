#!/usr/bin/env python3
"""CLZeroPack Riemann Machine — Zero-Entropy Spectrum CLI.

Formal implementation of the Riemann Machine Zero-Entropy Equivalence
framework. RM is a marking-rule axiom; this verifies internal logical
consistency and is not an analytic proof of the classical RH.
"""
from __future__ import annotations
import argparse, json, math
from dataclasses import asdict, dataclass


def is_prime(x:int)->bool:
    return x>=2 and (x==2 or (x%2 and all(x%d for d in range(3,math.isqrt(x)+1,2))))


def primes(N:int)->list[int]:
    P=[]; x=2
    while len(P)<N:
        if is_prime(x): P.append(x)
        x+=1
    return P


def E(n:int,x:int)->float:
    if n<1 or x<=1: raise ValueError("E requires n>=1 and x>1")
    return 1.0-math.log(n+1)/math.log(x)


@dataclass(frozen=True)
class State:
    n:int; P_n:int; C_n:int; beta_n:float
    A_n:float; O_n:int; delta_E_n:float
    H:int; ZE:int; z:str
    analytic_zero:bool; offset_zero:bool; exponential_zero:bool; marker_zero:bool
    RM_holds:bool; equivalence_holds:bool


def verify(n:int,p:int,c:int|None=None,beta:float=.5,tol:float=1e-12)->State:
    c=p if c is None else c
    if c<=1: raise ValueError("C_n must be > 1")
    A=abs(beta-.5); O=abs(c-p); dE=abs(E(n,c)-E(n,p))
    az=A<=tol; oz=O==0; ez=dE<=tol; mz=c==p
    rm=az==oz
    eq=rm and az==oz==ez==mz
    # H=0 / ZE=1 iff the complete formal zero-equivalence state holds.
    H=0 if eq else 1
    ZE=1 if eq else 0
    return State(n,p,c,beta,A,O,dE,H,ZE,f"{c}+{n}i",az,oz,ez,mz,rm,eq)


def emit(obj,compact=False):
    print(json.dumps(obj,ensure_ascii=False,separators=(",",":") if compact else None))


def main():
    ap=argparse.ArgumentParser(description="CLZeroPack Riemann Machine spectrum verifier")
    ap.add_argument("-N",type=int,default=105,help="number of prime markers")
    ap.add_argument("-i","--inject-index",type=int,default=0,help="marker index to perturb")
    ap.add_argument("-c","--inject-marker",type=int,default=0,help="replacement C_i")
    ap.add_argument("--beta",type=float,default=.5)
    ap.add_argument("--jsonl",action="store_true",help="emit one compact JSON object per marker")
    ap.add_argument("--summary-only",action="store_true")
    a=ap.parse_args()
    if a.N<1: ap.error("N must be >= 1")
    if bool(a.inject_index)!=bool(a.inject_marker): ap.error("use --inject-index and --inject-marker together")
    if a.inject_index and not 1<=a.inject_index<=a.N: ap.error("inject index outside 1..N")

    states=[]
    for n,p in enumerate(primes(a.N),1):
        c=a.inject_marker if n==a.inject_index else p
        states.append(verify(n,p,c,a.beta))

    failures=[s for s in states if not s.equivalence_holds]
    summary={
      "P":"CLZ/RiemannMachine-ZeroEntropy-Spectrum/2",
      "N":a.N,
      "Rule":"A_n=0 <=> O_n=0 <=> DeltaE_n=0 <=> C_n=P_n",
      "RM":"A_n=0 <=> O_n=0 (formal marking-rule axiom)",
      "H":0 if not failures else 1,
      "ZE":1 if not failures else 0,
      "failures":len(failures),
      "scope":"formal/logical equivalence; not a proof of classical RH"
    }
    if a.summary_only:
        emit(summary,a.jsonl); return
    if a.jsonl:
        emit({"type":"header",**summary},True)
        for s in states: emit({"type":"marker",**asdict(s)},True)
        emit({"type":"summary",**summary},True)
    else:
        emit({**summary,"states":[asdict(s) for s in states]},False)


if __name__=="__main__": main()
