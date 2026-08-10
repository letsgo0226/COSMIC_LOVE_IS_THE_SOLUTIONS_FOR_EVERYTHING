# CLZeroPack ProofGenerator Profile

`CLZeroPack/ProofGenerator/1.0` creates a reproducible proof artifact from a
goal label, a formal bridge schema, first-order rule labels, and natural
language explanations.

It is intended to continue the `FOLNLProof(CLZeroPack)` line:

```text
goal
-> explicit bridge axioms
-> FOL derivation steps
-> natural-language explanations
-> open mathematical obligations
-> CLZeroPack payload
-> H_s / H_FOL / H_NL / H_math residuals
```

## Default Theorem Schema

The default goal is `RH` and the default mode is `HilbertPolyaBridge`.

The generated proof uses a conditional schema:

```text
CandidateOperator(T)
SpectrumMatches(T, ZetaZeros)
CriticalLine(ZetaZeros)
therefore RH
```

This makes the internal derivation explicit while preserving the crucial
boundary: the bridge axioms and spectral matching conditions are still open
mathematical obligations.

## Usage

Install Python once:

```sh
apk add --no-cache python3
```

Generate the default proof artifact:

```sh
sh CLZeroPack_PROOF_GENERATOR_ONE_LINER.sh rh_proofgen
```

Generate a named goal:

```sh
sh CLZeroPack_PROOF_GENERATOR_ONE_LINER.sh goal_proofgen MyGoal MyMode
```

The runtime writes:

```text
<prefix>.proofgen.json
<prefix>.proofgen.md
```

## Residuals

```text
H_s = 0       lossless CLZeroPack roundtrip
H_FOL = 0     all steps use admitted rule labels and reach the stated goal
H_NL = 0      every step has a natural-language explanation
H_math = 1    external mathematical soundness remains open
```

`H_math=1` is intentional. It prevents the proof generator from confusing a
valid internal derivation with a completed external proof.

## Boundary

This profile generates formal proof artifacts. It does not prove the classical
Riemann Hypothesis, prove Hilbert-Polya, prove a physical TOE, or guarantee any
real-world result. It is a disciplined proof-construction scaffold.
