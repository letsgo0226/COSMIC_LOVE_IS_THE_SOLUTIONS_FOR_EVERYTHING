# CLZeroPack Zero-Spectrum Coordinate Restore Profile

`CLZeroPack/ZeroSpectrumCoordinateRestore/1.0` defines the zero-spectrum
coordinate as the standard restore index for CLZeroPack payloads.

The central distinction is:

```text
rho_CL = coordinate / index
Payload = lossless content
```

Therefore:

```text
rho_CL alone
-> not enough to restore bytes

rho_CL + registry entry + Payload
-> enough to restore bytes
```

## Standard Restore Form

```json
{
  "Protocol": "CLZeroPack/<Profile>/1.0",
  "G_alg": 57774241,
  "rho_CL": "1/2+i*log(1+57774241)",
  "Payload": "base64(zlib(raw_program_bytes))",
  "H_s": 0
}
```

## Restore Pipeline

```text
rho_CL or G_alg
-> lookup registry entry
-> Payload
-> base64 decode
-> zlib decompress
-> restored raw bytes
-> .zsr.json certificate
```

## Usage

Install Python once:

```sh
apk add --no-cache python3
```

Restore the first or only CLZeroPack envelope:

```sh
sh CLZeroPack_ZERO_SPECTRUM_RESTORE_ONE_LINER.sh item.clzeropack.json '*' restored.bin
```

Restore by `G_alg`:

```sh
sh CLZeroPack_ZERO_SPECTRUM_RESTORE_ONE_LINER.sh registry.json 57774241 restored.bin
```

Restore by `rho_CL`:

```sh
sh CLZeroPack_ZERO_SPECTRUM_RESTORE_ONE_LINER.sh registry.json '1/2+i*log(1+57774241)' restored.bin
```

The runtime writes:

```text
restored.bin
restored.bin.zsr.json
```

## Relation To CoordinateRuntime

`CoordinateRuntime` is the general runtime implementation. This profile gives
the same mechanism a stricter standard name for the mathematical role of the
coordinate:

```text
ZeroSpectrumCoordinateRestore = rho_CL as canonical restore index
```

## Boundary

This profile restores bytes. It does not execute them. It does not claim that a
coordinate alone contains all information. Lossless restoration requires the
registry entry and its payload.
