# CLZeroPack iSH Compliance Profile

`CLZeroPack/iSH-Compliance/1.0` checks whether a shell one-liner satisfies the
official CLZeroPack iSH constraint.

## Compliance Rule

```text
H_iSH = 0 iff
  one physical shell line
  and source bytes <= 8000
  and no SHA/hashlib dependency
  and H_s-capable by design
```

## iSH Tiers

| Tier | Source Bytes | Meaning |
|---|---:|---|
| `A` | `<= 1500` | best direct iSH one-liner |
| `B` | `<= 3500` | acceptable official iSH one-liner |
| `C` | `<= 8000` | usable but loader/stdin mode recommended |
| `LoaderRequired` | `> 8000` | not direct iSH compliant |

## Usage

```sh
apk add --no-cache python3
sh CLZeroPack_iSH_COMPLIANCE_ONE_LINER.sh target.sh target.ish.json
```

The checker is static: it does not execute the target program.

## Boundary

This profile checks length, line shape, No-SHA policy, and H_s-capable syntax
signals. It does not prove semantic correctness of the target one-liner.
