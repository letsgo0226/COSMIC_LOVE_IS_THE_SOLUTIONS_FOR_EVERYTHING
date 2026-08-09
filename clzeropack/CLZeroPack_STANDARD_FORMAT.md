# CLZeroPack Standard Format

`CLZeroPack` is an iSH-friendly lossless packaging format for finite programs,
proof artifacts, question-answer mappings, manifests, and text/data payloads.

It is designed to be:

```text
lossless
UTF-8 stable
No-SHA
iSH-friendly
profile-extensible
critical-line annotated
```

## Canonical Envelope

```json
{
  "Protocol": "CLZeroPack/<ProfileName>/1.0",
  "Payload": "<base64(zlib(subject_bytes))>",
  "G_alg": 0,
  "rho_CL": "1/2+i*log(1+G_alg)",
  "H_s": 0,
  "Manifest": {},
  "UTC": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## Canonical Pipeline

```text
Subject bytes
-> zlib compression
-> base64 encoding
-> Payload
-> finite algebraic code G_alg
-> rho_CL = 1/2+i*log(1+G_alg)
-> H_s roundtrip check
```

`subject_bytes` may be raw file bytes, stdin bytes, or compact UTF-8 JSON bytes
for profiles such as QA, ProofArtifact, FOLProof, and FOLNLProof.

`Manifest` remains the human-readable metadata and may either describe the
subject or be the subject itself, depending on the profile.

## Standard No-SHA Algebraic Code

The compact iSH reference implementation uses:

```python
G_alg = sum((i+1)*x for i,x in enumerate(zlib_bytes)) % 1000000007
```

This is not a cryptographic digest. It is a small deterministic algebraic
coordinate for CLZeroPack certificates.

## Standard Residuals

| Field | Meaning |
|---|---|
| `H_s` | lossless payload roundtrip |
| `H_iSH` | official one-liner satisfies iSH line and byte limits |
| `H_complete` | profile-required fields exist |
| `H_FOL` | first-order predicate logic structure closes |
| `H_NL` | natural-language explanations exist |
| `H_math` | external mathematical proof obligations close |

Only `H_s` belongs to every CLZeroPack envelope. Other residuals are
profile-specific.

## iSH Length Constraint

Official CLZeroPack one-liner profiles must be lossless first and iSH-bounded
second.

A one-liner is CLZeroPack-iSH compliant only if:

```text
1. it is one physical shell line
2. its source bytes fit an accepted iSH tier
3. it performs an H_s lossless roundtrip check
4. it writes text output with UTF-8 explicitly
5. it avoids SHA/hashlib unless a digest profile is explicitly declared
6. it never truncates source code to fit the terminal
```

The standard iSH tiers are:

| Tier | Source Bytes | Meaning |
|---|---:|---|
| `A` | `<= 1500` | best for direct iSH paste/store/run |
| `B` | `<= 3500` | acceptable official iSH one-liner |
| `C` | `<= 8000` | usable, but loader/stdin mode is recommended |
| `LoaderRequired` | `> 8000` | not a standard direct iSH one-liner |

The official iSH residual is:

```text
H_iSH = 0 iff
  one_physical_line
  and source_bytes <= 8000
  and H_s-capable by design
```

If losslessness and shortness conflict, CLZeroPack must preserve losslessness
by switching to one of:

```text
stdin payload mode
file input mode
GitHub raw fetch mode
zlib/base64 loader mode
```

It must not solve the conflict by cutting or truncating source code.

## Standard Profiles

```text
CLZeroPack/Tiny/1.0
CLZeroPack/Standard/1.0
CLZeroPack/CoordinateRuntime/1.0
CLZeroPack/QA-RH-Style/1.0
CLZeroPack/ProofArtifact/1.0
CLZeroPack/FOLProof/1.0
CLZeroPack/FOLNLProof/1.0
CLZeroPack/RH-Proof-Reduction/1.0
```

Use `CLZeroPack/Tiny/1.0` when iSH paste or command-buffer limits are strict.
Tiny omits automatic dependency installation and keeps only the canonical
lossless envelope fields.

Use `CLZeroPack/CoordinateRuntime/1.0` when a short zero-spectrum coordinate
must locate and decode a payload at runtime.

## Boundary

`CLZeroPack` proves lossless packaging when `H_s=0`.

It does not by itself prove:

```text
external mathematical truth
the classical Riemann Hypothesis
physical TOE claims
medical claims
real-world policy outcomes
```

Profiles may add formal logic layers, proof artifacts, natural-language
commentary, and domain-specific constraints, but those layers must state their
own residuals and boundaries explicitly.
