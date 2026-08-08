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
