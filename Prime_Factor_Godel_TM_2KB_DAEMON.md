# Prime_Factor_Godel_TM_2KB resident loop (daemon)

Continuous formal re-run of the prime-factor Gödel TM 2KB one-liner outside (and alongside) GitHub Actions `*/5`.

## Run

```sh
bash Prime_Factor_Godel_TM_2KB_DAEMON.sh          # 60s, N=4
bash Prime_Factor_Godel_TM_2KB_DAEMON.sh 30 8     # 30s, N=8
nohup bash Prime_Factor_Godel_TM_2KB_DAEMON.sh 60 4 >> prime_factor_godel_tm_daemon.log 2>&1 &
```

Env: `PFG_INTERVAL`, `PFG_N`, `PFG_LOG`, `PFG_SCRIPT`.

## Assert each tick

`model=PRIME_FACTOR_GODEL_TM`, `exact=true`, `omega_attained=0`, `program_equals_zeta=0`, `open=1`, `final=0`.

## Boundary

Formal Gödel / characteristica layer only. Does not claim RH, TOE, or empirical closure. Stays open (`final=0`).
