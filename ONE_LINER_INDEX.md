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

## CLZeroPack Core iSH Runtime

This runtime is the short reversible CLZeroPack carrier for iSH. The script is one physical shell line, excludes SHA-style digest functions, emits compact JSON fields, and defaults to `CLZ_L=6` for faster iSH operation.

Protocol:

```text
CLZEROPACK_CORE_PROTOCOL.md
```

Raw one-liner:

```text
https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/CLZEROPACK_CORE_ISH.sh
```

iSH pack/unpack:

```sh
apk add --no-cache python3 curl
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/CLZEROPACK_CORE_ISH.sh -o CLZEROPACK_CORE_ISH.sh
sh CLZEROPACK_CORE_ISH.sh pack input.py input.clzp.json
sh CLZEROPACK_CORE_ISH.sh unpack input.clzp.json restored.py
```

Maximum compression mode:

```sh
CLZ_L=9 sh CLZEROPACK_CORE_ISH.sh pack input.py input.max.clzp.json
```

Stdin pack:

```sh
printf abc | sh CLZEROPACK_CORE_ISH.sh pack - abc.clzp.json
```

Boundary: `H=0` means only that the finite local roundtrip check closed.

## Notes

- Raw URLs are more stable for AI tools than rendered GitHub pages.
- Long one-liners may be split into a raw `.sh` plus compressed payload for iSH length limits.
- No-SHA variants should state their exact encoding rule, such as G25 bit-fold encoding or compact weighted compressed-byte coordinates.
