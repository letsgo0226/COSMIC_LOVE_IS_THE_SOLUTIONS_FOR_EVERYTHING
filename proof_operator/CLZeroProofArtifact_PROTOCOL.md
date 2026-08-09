# CLZeroProofArtifact Protocol

`CLZeroProofArtifact` is a CLZeroPack profile for generating a complete proof
artifact from a problem, answer, and proof text while suspending external
validity.

It separates four layers:

| Layer | Meaning |
|---|---|
| `completeness` | the proof artifact is present, structured, and losslessly recoverable |
| `validity` | each inference step follows an accepted proof rule |
| `soundness` | the proof rules preserve truth in the intended model |
| `truth` | the target theorem is true in standard mathematical semantics |

This profile closes only the first layer unless an external verifier is added.

## Formal Shape

Given:

```text
Q = problem
A = answer
P = proof artifact
```

the system forms:

```text
CLZeroProof(Q,A,P)
  = Seal(base64(zlib(JSON(Q,A,P,status))))
```

and assigns a formal critical-line coordinate:

```text
rho_P = 1/2 + i * log(1 + G_alg(Payload))
```

## Completion

```text
H_s = 0
H_complete = 0
```

means the proof artifact is complete as an encoded object:

```text
Q exists
A exists
P exists
payload roundtrips losslessly
```

It does not mean:

```text
P is a verified proof
P is sound in standard mathematics
RH has been externally proven
```

## Default RH Artifact

When no custom proof is supplied, the one-liner emits a complete proof artifact
for the internal claim:

```text
If a self-adjoint operator T has spectrum exactly matching the imaginary parts
of all nontrivial zeta zeros, then RH follows.
```

This is a complete conditional proof artifact, not a completed proof of the
open Hilbert-Polya bridge theorem.

## iSH Usage

```sh
apk add --no-cache python3
sh CLZeroProofArtifact_ONE_LINER.sh rh_artifact
```

With a custom problem and answer:

```sh
sh CLZeroProofArtifact_ONE_LINER.sh out "question" "answer" "proof text"
```

This creates:

```text
out.clzeroproof.json
out.clzeroproof.md
```
