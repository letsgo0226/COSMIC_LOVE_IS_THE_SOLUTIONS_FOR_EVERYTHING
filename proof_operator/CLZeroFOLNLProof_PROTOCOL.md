# CLZeroFOLNLProof Protocol

`CLZeroFOLNLProof` extends `CLZeroFOLProof` by requiring every formal proof
step to include a natural-language explanation.

The result is a two-layer proof artifact:

```text
Formal Layer:
  first-order predicate logic language, axioms, rules, steps, conclusion

Natural Language Layer:
  human-readable explanation attached to each formal step

CLZeroPack Layer:
  zlib + base64 lossless payload, G_alg, critical-line coordinate
```

## Required Fields

Each proof step has:

```text
n        step number
rule     first-order predicate logic rule label
formula  formal formula
NL       natural-language explanation
```

## Residuals

```text
H_s = 0
```

means the payload roundtrips losslessly.

```text
H_complete = 0
```

means the artifact contains question, language, axioms, rules, steps,
conclusion, and proof text.

```text
H_FOL = 0
```

means every step uses an allowed first-order predicate logic rule label and the
final formula matches the stated conclusion.

```text
H_NL = 0
```

means every formal step has a non-empty natural-language explanation.

## Boundary

Natural language improves readability. It does not by itself prove soundness,
truth, or the external Riemann Hypothesis. The bridge axioms still require
external mathematical justification.

## iSH Usage

```sh
apk add --no-cache python3
sh CLZeroFOLNLProof_ONE_LINER.sh rh_folnl
```

This creates:

```text
rh_folnl.clzerofolnl.json
rh_folnl.clzerofolnl.md
```
