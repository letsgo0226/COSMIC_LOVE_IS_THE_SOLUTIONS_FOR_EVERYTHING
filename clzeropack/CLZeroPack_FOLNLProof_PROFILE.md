# FOLNLProof(CLZeroPack) Profile

`FOLNLProof(CLZeroPack)` is the standard CLZeroPack profile for proof artifacts
that combine first-order predicate logic with natural-language explanations.

It follows the canonical CLZeroPack envelope:

```json
{
  "Protocol": "CLZeroPack/FOLNLProof/1.0",
  "Payload": "<base64(zlib(manifest_json_bytes))>",
  "G_alg": 0,
  "rho_CL": "1/2+i*log(1+G_alg)",
  "H_s": 0,
  "Manifest": {},
  "UTC": "YYYY-MM-DDTHH:MM:SSZ"
}
```

and adds profile-specific residuals:

```text
H_complete
H_FOL
H_NL
```

## Manifest Shape

```text
Manifest.Protocol = CLZeroFOLNLProof/1.0
Manifest.Language = predicates, constants
Manifest.AllowedRules = FOL rule labels
Manifest.Axioms = explicit axioms
Manifest.Steps = formula + rule + natural-language explanation
Manifest.Conclusion = final formula
```

## Meaning

```text
H_s = 0
```

means the manifest JSON bytes roundtrip through zlib and base64.

```text
H_complete = 0
```

means the proof artifact has the required structural fields.

```text
H_FOL = 0
```

means every step uses the allowed first-order predicate logic rule labels and
the final step reaches the stated conclusion.

```text
H_NL = 0
```

means every formal proof step has a natural-language explanation.

## Boundary

This profile standardizes proof packaging and readability. It does not itself
prove soundness, external mathematical truth, or the classical Riemann
Hypothesis. Bridge axioms still require independent mathematical proof.

## iSH Usage

```sh
apk add --no-cache python3
sh CLZeroPack_FOLNLProof_ONE_LINER.sh rh_standard
```

This creates:

```text
rh_standard.clzerofolnl.json
rh_standard.clzerofolnl.md
```
