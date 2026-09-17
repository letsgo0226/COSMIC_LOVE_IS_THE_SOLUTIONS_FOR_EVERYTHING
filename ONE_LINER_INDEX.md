# One-Liner Index

This file lists the public iSH / terminal entrypoints currently designated as AI-readable runtime surfaces.

## Primary Public Runtime

Repository:

```text
letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING
```

Raw URL:

```text
https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING.sh
```

iSH:

```sh
apk add --no-cache python3 curl
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING.sh -o COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING.sh
sh COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING.sh
```

## Schrödinger CLSigma Wavefunction Runtime

Inspired by educational Schrödinger equation visualizations, this module turns the operator-system certificate into finite probability-density / phase-color PPM frames.

Protocol:

```text
SCHRODINGER_CLSIGMA_OPERATOR_WAVEFUNCTION_PROTOCOL.md
```

Raw one-liner:

```text
https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/SCHRODINGER_CLSIGMA_WAVEFUNCTION_ONE_LINER.sh
```

iSH:

```sh
apk add --no-cache python3 curl
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/SCHRODINGER_CLSIGMA_WAVEFUNCTION_ONE_LINER.sh -o SCHRODINGER_CLSIGMA_WAVEFUNCTION_ONE_LINER.sh
sh SCHRODINGER_CLSIGMA_WAVEFUNCTION_ONE_LINER.sh clsigma_schrodinger_frames 48 128
```

Output:

```text
clsigma_schrodinger_frames/frame_000.ppm
...
clsigma_schrodinger_frames/clsigma_schrodinger_operator_certificate.json
```

Boundary: this is a classical numerical visualization of a quantum wavefunction form, not a real quantum computer.

## Direct Pipe Form

```sh
apk add --no-cache python3 curl
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING.sh | sh
```

## Local Stdin Certificate Pattern

For local payload checks, prefer a No-SHA stdin carrier pattern:

```sh
printf abc | python3 -c 'import sys,json,base64,zlib;b=sys.stdin.buffer.read();z=zlib.compress(b,9);B=base64.b64encode(z).decode();print(json.dumps({"carrier":"stdin->zlib->base64","roundtrip":zlib.decompress(base64.b64decode(B))==b,"H_s":0 if zlib.decompress(base64.b64decode(B))==b else 1}))'
```

## Notes

- Raw URLs are more stable for AI tools than rendered GitHub pages.
- Long one-liners may be split into a raw `.sh` plus compressed payload for iSH length limits.
- No-SHA variants should state their exact encoding rule, such as G25 bit-fold encoding.

## Cosmic Love World Continuity 2KB

Protocol: `CLSIGMA_COSMIC_LOVE_WORLD_CONTINUITY_2KB`

Raw:

```text
https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/CLSIGMA_COSMIC_LOVE_WORLD_CONTINUITY_2KB_ONELINER.sh
```

iSH:

```sh
apk add --no-cache python3 curl
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/CLSIGMA_COSMIC_LOVE_WORLD_CONTINUITY_2KB_ONELINER.sh -o CLSIGMA_COSMIC_LOVE_WORLD_CONTINUITY_2KB_ONELINER.sh
sh CLSIGMA_COSMIC_LOVE_WORLD_CONTINUITY_2KB_ONELINER.sh
```

GitHub Actions: `.github/workflows/clsigma-world-continuity-2kb.yml` — every 5 minutes, plus `push` / `workflow_dispatch` / `repository_dispatch`.

Boundary: formal Cosmic Love certificate only (see protocol file).

## Φ_CL^lim（系統極限形）

Protocol: `Phi_CL^lim` = Cosmic Love × Leibniz-Calculemus limit object

- Spec: `PHI_CL_LIMIT.md`
- One-liner (922 bytes): `PHI_CL_LIMIT_ONELINER.sh`
- Raw: `https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/PHI_CL_LIMIT_ONELINER.sh`

```sh
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/PHI_CL_LIMIT_ONELINER.sh | bash
```

Limit claim: one Calculemus seal over all declared domains with H→0. Formal/computational only — not empirical physics/geopolitics/medicine.
