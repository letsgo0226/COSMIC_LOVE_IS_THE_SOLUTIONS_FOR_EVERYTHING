# ALL_PUBLIC_PROGRAMS Daemon

Resident rotator over public `.sh` / `.py` / `.json` programs catalogued for `letsgo0226` (v2 515-file catalog).

## Purpose

Formal rotation: prefer a local mirror under `APP_LOCAL_ROOT`, else fetch each public program from GitHub raw, execute or validate under a timeout, and append one JSON status line per item. This is a **rate-limited formal rotation / inventory loop**, not an empirical claim that every script "works" as intended, proves theorems, or validates scientific results.

## Boundary

- **Formal rotation only** — pass/fail means process exit code within `APP_TIMEOUT`, not semantic correctness.
- **JSON** — pass = successful `json.load` parse only (structure validate), not schema or domain checks.
- **Rate limits** — `APP_INTERVAL` between items, `APP_CYCLE_SLEEP` after a full pass; local mirror avoids raw rate limits when present.
- **Not empirical** — timeouts, missing deps, interactive prompts, or network calls inside target scripts may yield `fail` / `timeout` without implying the source is invalid.
- **Default branch** — raw URLs use `main` (Cosmic Love and Zeta use `main`).
- **Scope** — public repos only; no secrets; no private clones.

## Manifest

`manifest.jsonl` — one JSON object per line (515 entries from v2 catalog):

```json
{"repo":"...","path":"...","ext":"sh|py|json","bytes":123,"kind":"sh|py|json","raw":"https://raw.githubusercontent.com/letsgo0226/{repo}/main/{path}","local":"/workspace/letsgo0226-precise-programs-v2/by-repo/{repo}/{path}"}
```

Built from `/workspace/letsgo0226-precise-programs-v2/catalog.jsonl`. `local` is set when the file exists under the by-repo mirror.

## Environment

| Variable | Default | Meaning |
|----------|---------|---------|
| `APP_INTERVAL` | `3` | Sleep seconds between items |
| `APP_CYCLE_SLEEP` | `60` | Sleep after full pass |
| `APP_TIMEOUT` | `20` | Per-item curl + run / validate timeout (seconds) |
| `APP_LOG` | `$APP_WORKDIR/all_public_programs_daemon.log` | JSONL log |
| `APP_MANIFEST` | `$APP_WORKDIR/manifest.jsonl` | Manifest path |
| `APP_MAX` | `0` | Max items per pass (`0` = all) |
| `APP_WORKDIR` | script directory | Cache + default paths |
| `APP_LOCAL_ROOT` | `/workspace/letsgo0226-precise-programs-v2/by-repo` | Prefer local `{repo}/{path}` before curl |

## Run rules

| kind | action |
|------|--------|
| `sh` | `timeout $APP_TIMEOUT bash FILE` |
| `py` | `timeout $APP_TIMEOUT python3 FILE` |
| `json` | `timeout $APP_TIMEOUT python3 -c 'import json,sys; json.load(open(sys.argv[1]))' FILE` |

## Log line

```json
{"ts":"ISO8601Z","repo":"...","path":"...","status":"pass|fail|timeout|skip","secs":N,"note":"..."}
```

- `pass` — exit 0 (or JSON parse OK)
- `fail` — non-zero exit (not timeout)
- `timeout` — killed by `timeout` (exit 124)
- `skip` — local copy or curl fetch failed
- `note` — often `local` when served from mirror, `ok` when curled, or `exit_N` / `timeout` / `curl_fail`

## How to run

One pass (smoke / CI):

```sh
cd /workspace/public-programs-daemon
APP_MAX=5 bash ALL_PUBLIC_PROGRAMS_DAEMON.sh once
```

Resident loop:

```sh
cd /workspace/public-programs-daemon
APP_INTERVAL=5 APP_CYCLE_SLEEP=120 APP_TIMEOUT=15 \
  APP_LOCAL_ROOT=/workspace/letsgo0226-precise-programs-v2/by-repo \
  nohup bash ALL_PUBLIC_PROGRAMS_DAEMON.sh >>nohup.out 2>&1 &
echo $! > daemon.pid
```

## Cache

Local or fetched files land in `$APP_WORKDIR/cache/{repo}/{path}` then run / validate via the rules above.

## Deploy surface

Publish to `letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING`:

- `ALL_PUBLIC_PROGRAMS_DAEMON.sh`
- `ALL_PUBLIC_PROGRAMS_DAEMON.md`
- `manifest.jsonl` (sh+py+json; 515 entries)
