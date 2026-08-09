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
| `H_complete` | profile-required fields exist |
| `H_FOL` | first-order predicate logic structure closes |
| `H_NL` | natural-language explanations exist |
| `H_math` | external mathematical proof obligations close |

Only `H_s` belongs to every CLZeroPack envelope. Other residuals are
profile-specific.

## Standard Profiles

```text
CLZeroPack/Standard/1.0
CLZeroPack/QA-RH-Style/1.0
CLZeroPack/ProofArtifact/1.0
CLZeroPack/FOLProof/1.0
CLZeroPack/FOLNLProof/1.0
CLZeroPack/RH-Proof-Reduction/1.0
```

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
