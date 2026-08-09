# CLZeroPack Tiny Profile

`CLZeroPack/Tiny/1.0` is the shortest direct iSH profile for lossless
CLZeroPack packaging.

It keeps the canonical envelope:

```text
Protocol
Payload
G_alg
rho_CL
H_s
Manifest
UTC
```

but removes helper text and automatic dependency installation.

## Usage

Install Python once:

```sh
apk add --no-cache python3
```

Then run:

```sh
sh CLZeroPack_TINY_ONE_LINER.sh input.txt out.clzeropack.json
```

Or from stdin:

```sh
printf 'hello' | sh CLZeroPack_TINY_ONE_LINER.sh - out.clzeropack.json
```

## Why Tiny Exists

Some iSH terminals truncate or mishandle long pasted commands. Tiny keeps the
program below the strongest CLZeroPack Tier A threshold while preserving:

```text
raw bytes -> zlib -> base64 -> H_s roundtrip
```

## Boundary

Tiny assumes `python3` already exists. If not, run `apk add --no-cache python3`
first.
