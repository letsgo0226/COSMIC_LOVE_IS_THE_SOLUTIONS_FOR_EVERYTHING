# CLZeroPack Coordinate Runtime Profile

`CLZeroPack/CoordinateRuntime/1.0` lets a zero-spectrum coordinate act as a
runtime locator.

It does not claim that:

```text
rho_CL alone contains the whole program
```

Instead it defines:

```text
rho_CL or G_alg
-> lookup in CLZeroPack certificate or registry
-> Payload
-> base64 decode
-> zlib decompress
-> write bytes to the operating system
```

## Why This Is Needed

The coordinate:

```text
rho_CL = 1/2+i*log(1+G_alg)
```

can be short and fixed in shape. But lossless recovery still requires the
payload:

```text
Payload = base64(zlib(subject_bytes))
```

`CoordinateRuntime` connects the short coordinate to the payload at runtime.

## Registry Shape

The runtime accepts either a single CLZeroPack envelope:

```json
{
  "Protocol": "CLZeroPack/Tiny/1.0",
  "Payload": "...",
  "G_alg": 123,
  "rho_CL": "1/2+i*log(1+123)"
}
```

or a registry:

```json
{
  "Entries": [
    {
      "Name": "program_a",
      "Payload": "...",
      "G_alg": 123,
      "rho_CL": "1/2+i*log(1+123)"
    }
  ]
}
```

## Usage

Install Python once:

```sh
apk add --no-cache python3
```

Decode by `G_alg`:

```sh
sh CLZeroPack_COORDINATE_RUNTIME_ONE_LINER.sh registry.json 123 output.bin
```

Decode by `rho_CL`:

```sh
sh CLZeroPack_COORDINATE_RUNTIME_ONE_LINER.sh registry.json '1/2+i*log(1+123)' output.bin
```

If the registry is a single CLZeroPack envelope, `*` selects it:

```sh
sh CLZeroPack_COORDINATE_RUNTIME_ONE_LINER.sh item.clzeropack.json '*' output.bin
```

Running the script without arguments prints a compact JSON usage object instead
of raising a Python traceback.

## Boundary

The runtime writes decoded bytes and a `.runtime.json` certificate. It does not
execute decoded bytes. Any execution layer must be a separate explicit profile.
