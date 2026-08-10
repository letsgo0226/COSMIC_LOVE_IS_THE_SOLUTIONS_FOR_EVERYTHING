# CLZeroPack Core iSH Protocol

`CLZeroPack-Core` is the short, No-SHA carrier form of CLZeroPack for iSH and terminal use. The runtime file is one physical shell line.

## Rule

```text
raw bytes -> zlib(level=9) -> base64 -> G_alg -> rho_CL
```

The core format excludes SHA-style digest functions. It is intended as a reversible terminal carrier, not as an archival integrity certificate.

## Minimal Fields

| Field | Meaning |
| --- | --- |
| `P` | Protocol name |
| `A` | Axiom tag, usually `CL` |
| `Z` | Encoding rule, `zlib9+b64` |
| `G` | No-SHA weighted compressed-byte coordinate |
| `r` | Formal critical-line coordinate |
| `n` | Raw byte length |
| `zn` | Compressed byte length |
| `H` | `0` when roundtrip closes |
| `B` | Base64 zlib payload |

## Coordinate

```text
G = sum((i + 1) * byte_i for byte_i in zlib_payload) mod 1000000007
rho_CL = 1/2 + i*log(1 + G)
```

This is a compact deterministic coordinate. It is not a cryptographic hash.

## iSH Runtime

```sh
apk add --no-cache python3 curl
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/CLZEROPACK_CORE_ISH.sh -o CLZEROPACK_CORE_ISH.sh
sh CLZEROPACK_CORE_ISH.sh pack input.py input.clzp.json
sh CLZEROPACK_CORE_ISH.sh unpack input.clzp.json restored.py
```

Stdin pack form:

```sh
printf abc | sh CLZEROPACK_CORE_ISH.sh pack - abc.clzp.json
```

## Boundary

`H=0` means only that the finite local roundtrip check closed. `rho_CL` is a formal indexing convention, not a proof of RH, GRH, TOE, or any external-world guarantee.
