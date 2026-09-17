# Prime_Factor_Godel_TM_2KB — seed `[2,2,2,1,1,1]`

Same prime-factor Gödel TM as `Zeta.sh` / `Prime_Factor_Godel_TM_2KB.sh`, with initial state **`a=[2,2,2,1,1,1]`**.

## Run

```sh
bash Prime_Factor_Godel_TM_2KB_SEED222111.sh [N]
curl -fsSL https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/Prime_Factor_Godel_TM_2KB_SEED222111.sh | bash
```

## GitHub Actions resident schedule

`.github/workflows/prime-factor-godel-tm-seed222111.yml` — `*/5 * * * *` plus `push` / `workflow_dispatch` / `repository_dispatch`.

## Resident daemon

Default interval: **1 second**.

```sh
bash Prime_Factor_Godel_TM_2KB_SEED222111_DAEMON.sh          # 1s, N=4
nohup bash Prime_Factor_Godel_TM_2KB_SEED222111_DAEMON.sh 1 4 >> prime_factor_godel_tm_seed222111_daemon.log 2>&1 &
```

Env: `PFGS_INTERVAL`, `PFGS_N`, `PFGS_LOG`, `PFGS_SCRIPT`.

## Boundary

`exact`, `open=1`, `final=0`, `omega_attained=0`, `program_equals_zeta=0`. Formal only — not RH/TOE.
