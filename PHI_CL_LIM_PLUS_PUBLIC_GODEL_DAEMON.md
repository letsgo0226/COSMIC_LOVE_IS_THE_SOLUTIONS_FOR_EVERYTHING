# Φ_CL^lim⁺⁺ resident loop (daemon)

Continuous formal re-certification of `PHI_CL_LIM_PLUS_PUBLIC_GODEL_ONELINER.sh` outside GitHub Actions.

## Why

GitHub Actions cron floor is ~5 minutes and is not a true resident process. This daemon is a `while true` loop for a host you control (VPS, laptop, self-hosted runner, or an always-on agent machine).

## Run

```sh
# default: every 60s, N=4
bash PHI_CL_LIM_PLUS_PUBLIC_GODEL_DAEMON.sh

# every 30s, N=3
bash PHI_CL_LIM_PLUS_PUBLIC_GODEL_DAEMON.sh 30 3

# background
nohup bash PHI_CL_LIM_PLUS_PUBLIC_GODEL_DAEMON.sh 60 4 >> phi_cl_lim_pp_daemon.log 2>&1 &
```

Env overrides: `PHI_CL_INTERVAL`, `PHI_CL_N`, `PHI_CL_LOG`, `PHI_CL_SCRIPT`, plus `GH_TOKEN` / `GITHUB_TOKEN` for API rate limits.

## Boundary

Same as the one-liner: formal Cosmic Love × Calculemus × Gödel × PublicWorld name-band only (`open=1`, `final=0`). Not empirical resolution. Respect GitHub API rate limits — prefer ≥30–60s intervals.
