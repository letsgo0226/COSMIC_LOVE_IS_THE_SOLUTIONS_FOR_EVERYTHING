# ALL_PUBLIC_PROGRAMS Daemon

Resident rotator over public `.sh` / `.py` programs catalogued for `letsgo0226`.

## Purpose

Formal rotation: fetch each public program from GitHub raw, execute under a timeout, and append one JSON status line per item. This is a **rate-limited formal rotation / inventory loop**, not an empirical claim that every script "works" as intended, proves theorems, or validates scientific results.

## Boundary

- **Formal rotation only** — pass/fail means process exit code within `APP_TIMEOUT`, not semantic correctness.
- **Rate limits** — `APP_INTERVAL` between items, `APP_CYCLE_SLEEP` after a full pass; respect GitHub raw / API limits.
- **Not empirical** — timeouts, missing deps, interactive prompts, or network calls inside target scripts may yield `fail` / `timeout` without implying the source is invalid.
- **Default branch** — raw URLs use `main` (Cosmic Love and Zeta use `main`).
- **Scope** — public repos only; no secrets; no private clones.

## Manifest

`manifest.jsonl` — one JSON object per line:

```json
{"repo":"...","path":"...","bytes":123,"kind":"sh|py","raw":"https://raw.githubusercontent.com/letsgo0226/{repo}/main/{path}"}
```

Built from `/workspace/letsgo0226-precise-programs.jsonl` filtered to paths ending in `.sh` or `.py`.

## Environment

| Variable | Default | Meaning |
|----------|---------|---------|
| `APP_INTERVAL` | `3` | Sleep seconds between items |
| `APP_CYCLE_SLEEP` | `60` | Sleep after full pass |
| `APP_TIMEOUT` | `20` | Per-item curl + run timeout (seconds) |
| `APP_LOG` | `$APP_WORKDIR/all_public_programs_daemon.log` | JSONL log |
| `APP_MANIFEST` | `$APP_WORKDIR/manifest.jsonl` | Manifest path |
| `APP_MAX` | `0` | Max items per pass (`0` = all) |
| `APP_WORKDIR` | script directory | Cache + default paths |

## Log line

```json
{"ts":"ISO8601Z","repo":"...","path":"...","status":"pass|fail|timeout|skip","secs":N,"note":"..."}
```

- `pass` — exit 0  
- `fail` — non-zero exit (not timeout)  
- `timeout` — killed by `timeout` (exit 124)  
- `skip` — curl fetch failed  

## How to run

One pass (smoke / CI):

```sh
cd /workspace/public-programs-daemon
APP_MAX=3 bash ALL_PUBLIC_PROGRAMS_DAEMON.sh once
```

Resident loop:

```sh
cd /workspace/public-programs-daemon
APP_INTERVAL=5 APP_CYCLE_SLEEP=120 APP_TIMEOUT=15 \
  nohup bash ALL_PUBLIC_PROGRAMS_DAEMON.sh >>nohup.out 2>&1 &
echo $! > daemon.pid
```

## Cache

Fetched files land in `$APP_WORKDIR/cache/{repo}/{path}` then run via `timeout $APP_TIMEOUT bash` or `python3`.

## Deploy surface

Optional publish to `letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING`:

- `ALL_PUBLIC_PROGRAMS_DAEMON.sh`
- `ALL_PUBLIC_PROGRAMS_DAEMON.md`
- `manifest.jsonl` (path list; may be truncated if oversized)
