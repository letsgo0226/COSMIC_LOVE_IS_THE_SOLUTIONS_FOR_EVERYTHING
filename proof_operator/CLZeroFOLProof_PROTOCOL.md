# CLZeroFOLProof Protocol

`CLZeroFOLProof` is a CLZeroPack profile that requires proof artifacts to be
organized through first-order predicate logic.

It extends `CLZeroProofArtifact` by adding:

```text
Language
Axioms
AllowedRules
Steps
Conclusion
H_FOL
```

## Required Rule Policy

Formal validity, when checked by this profile, must be expressed through
first-order predicate logic rule labels. The compact iSH version uses this core
schema:

```text
AXIOM
UI          universal instantiation
MP          modus ponens
AND_INTRO   conjunction introduction
```

Longer versions may add:

```text
UG
EXISTS_INTRO
EXISTS_ELIM
AND_ELIM
OR_INTRO
OR_ELIM
IMP_INTRO
NEG_INTRO
EQ_SUBST
```

## Default RH Skeleton

The default generated artifact uses the language:

```text
SelfAdjoint(t)
RealSpectrum(t)
SpectrumMatches(t,ZetaZeros)
RH
```

with explicit axioms:

```text
forall t (SelfAdjoint(t) -> RealSpectrum(t))
forall t ((RealSpectrum(t) & SpectrumMatches(t,ZetaZeros)) -> RH)
SelfAdjoint(T)
SpectrumMatches(T,ZetaZeros)
```

The proof then derives:

```text
RH
```

by `UI`, `MP`, and `AND_INTRO`.

## Meaning of Residuals

```text
H_s = 0
```

means the CLZeroPack payload roundtrips losslessly.

```text
H_complete = 0
```

means the proof object contains question, language, axioms, rules, steps, and
conclusion.

```text
H_FOL = 0
```

means the artifact is organized under the required first-order predicate logic
rule schema.

It does not mean:

```text
the bridge axioms have been externally justified
the system is sound for classical number theory
the Riemann Hypothesis has been proven
```

## iSH Usage

```sh
apk add --no-cache python3
sh CLZeroFOLProof_ONE_LINER.sh rh_fol
```

This creates:

```text
rh_fol.clzerofol.json
rh_fol.clzerofol.md
```
