# CLZeroRH Proof Reduction Protocol

`CLZeroRHProof` converts a CLZeroPack-style construction into a formal proof
reduction for the Riemann Hypothesis while suspending the validity of the
program output itself.

The program is used only as a source of structure. The final mathematical
target must be readable without trusting the program.

## Principle

The CLZeroPack coordinate

```text
rho_X = 1/2 + i * log(1 + G_alg(X))
```

is not a proof of the Riemann Hypothesis. It is a hint that a proof should be
reduced to a spectral statement:

```text
nontrivial zeta zeros <-> spectrum of a self-adjoint operator
```

## Formal Reduction

Let `xi(s)` be the completed zeta function. The proof target is:

```text
For every nontrivial zero rho of zeta(s), Re(rho)=1/2.
```

The Hilbert-Polya style reduction is:

1. Construct a Hilbert space `H`.
2. Define a densely defined operator `T` on `H`.
3. Prove `T` is self-adjoint.
4. Prove the spectral determinant of `T` equals `xi(s)` up to accepted
   normalization.
5. Prove a bijection between the spectrum of `T` and the imaginary parts of all
   nontrivial zeros of `zeta(s)`.
6. Since self-adjoint spectra are real, each zero is of the form
   `rho = 1/2 + i*gamma`, with `gamma` real.

Then:

```text
Re(rho)=1/2
```

## Status

This protocol produces a conditional formal theorem:

```text
If such a self-adjoint operator T and exact spectral bridge exist,
then the Riemann Hypothesis follows.
```

It does not claim the open bridge theorem has been completed.

## iSH Usage

```sh
apk add --no-cache python3
sh CLZeroRH_PROOF_REDUCTION_ONE_LINER.sh rh_proof
```

This creates:

```text
rh_proof.clzerorh.json
rh_proof.clzerorh.md
```

`H_s=0` means the certificate payload roundtrips losslessly. `H_math=0` would
mean all proof obligations are closed; this runtime leaves the bridge
obligations explicit unless a future proof supplies them.
