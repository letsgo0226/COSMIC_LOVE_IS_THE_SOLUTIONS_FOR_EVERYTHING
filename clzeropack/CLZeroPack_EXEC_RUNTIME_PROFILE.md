# CLZeroPack Exec Runtime Profile

`CLZeroPack/ExecRuntime/1.0` is the explicit execution profile for CLZeroPack.

It extends `CoordinateRuntime`:

```text
rho_CL or G_alg
-> lookup in CLZeroPack certificate or registry
-> Payload
-> base64 decode
-> zlib decompress
-> write restored bytes
-> execute restored local payload
-> write .exec.json certificate
```

## Why This Is Separate

`CoordinateRuntime` only restores bytes. `ExecRuntime` restores and runs them.
Keeping the two profiles separate makes execution an explicit act instead of a
hidden side effect.

## Usage

Install Python once:

```sh
apk add --no-cache python3
```

Execute the first or only CLZeroPack envelope:

```sh
sh CLZeroPack_EXEC_RUNTIME_ONE_LINER.sh item.clzeropack.json '*' restored.sh
```

Execute by `G_alg`:

```sh
sh CLZeroPack_EXEC_RUNTIME_ONE_LINER.sh registry.json 123 restored.sh
```

Pass arguments to the restored program:

```sh
sh CLZeroPack_EXEC_RUNTIME_ONE_LINER.sh registry.json 123 restored.sh arg1 arg2
```

If the output filename ends in `.py`, the runtime executes it with `python3`.
If the restored bytes start with a shebang, the runtime executes the restored
file directly. Otherwise it executes the restored file with `sh`.

Running the script without arguments prints a compact JSON usage object instead
of raising a Python traceback.

## Boundary

This profile executes restored local code. Use it only with trusted CLZeroPack
certificates or registries. It does not prove mathematical claims, guarantee
external-world outcomes, or make arbitrary downloaded code safe.
