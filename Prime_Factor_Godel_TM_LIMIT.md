# Φ_G^lim — Prime-Factor Gödel TM limit object

## Form

**Φ_G^lim := ExactDecode( G = ∏ p^(a+1) ) → exact，且 ω 僅作形式 colim**

with **`open=1`**, **`final=0`**, **`omega_attained=0`**, **`program_equals_zeta=0`**.

## Relation to 2KB body

| | `Prime_Factor_Godel_TM_2KB.sh` | `Prime_Factor_Godel_TM_LIMIT_ONELINER.sh` |
|--|--|--|
| Role | Explanatory finite-prefix certificate (`levels`) | Limit / contract object |
| Size | 999B | &lt;1024B (currently ~978B) |
| Trace | full `levels` | seed + `a_last` only |
| η depth | K=128 | K=32 |

## Run

```sh
bash Prime_Factor_Godel_TM_LIMIT_ONELINER.sh [N]   # default N=1
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/Prime_Factor_Godel_TM_LIMIT_ONELINER.sh | bash
```

## Resident loop

See `Prime_Factor_Godel_TM_LIMIT_DAEMON.sh`.

## Boundary

Formal characteristica limit only. Not RH, TOE, or empirical closure. Does not replace the 2KB body on `Zeta.sh`.
