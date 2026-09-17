#!/usr/bin/env bash
# ALL_PUBLIC_PROGRAMS resident rotator — formal rotation over public .sh/.py/.json
# Usage:
#   bash ALL_PUBLIC_PROGRAMS_DAEMON.sh          # loop forever
#   bash ALL_PUBLIC_PROGRAMS_DAEMON.sh once     # one pass then exit
# Env: APP_INTERVAL APP_CYCLE_SLEEP APP_TIMEOUT APP_LOG APP_MANIFEST APP_MAX APP_WORKDIR APP_LOCAL_ROOT
set -u

MODE="${1:-loop}"
DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd || pwd)"
APP_INTERVAL="${APP_INTERVAL:-3}"
APP_CYCLE_SLEEP="${APP_CYCLE_SLEEP:-60}"
APP_TIMEOUT="${APP_TIMEOUT:-20}"
APP_WORKDIR="${APP_WORKDIR:-$DIR}"
APP_MANIFEST="${APP_MANIFEST:-$APP_WORKDIR/manifest.jsonl}"
APP_LOG="${APP_LOG:-$APP_WORKDIR/all_public_programs_daemon.log}"
APP_MAX="${APP_MAX:-0}"
APP_LOCAL_ROOT="${APP_LOCAL_ROOT:-/workspace/letsgo0226-precise-programs-v2/by-repo}"

mkdir -p "$APP_WORKDIR/cache"
command -v curl >/dev/null || { echo "need curl" >&2; exit 127; }
command -v python3 >/dev/null || { echo "need python3" >&2; exit 127; }
command -v timeout >/dev/null || { echo "need timeout" >&2; exit 127; }
[[ -f "$APP_MANIFEST" ]] || { echo "missing manifest: $APP_MANIFEST" >&2; exit 1; }

log_line() {
  printf '%s\n' "$1" >>"$APP_LOG"
}

urlencode_path() {
  # encode path segments for raw.githubusercontent.com (preserve /)
  python3 -c 'import sys,urllib.parse; print("/".join(urllib.parse.quote(p, safe="") for p in sys.argv[1].split("/")))' "$1"
}

run_one() {
  local repo="$1" path="$2" kind="$3" raw="$4" local_hint="${5:-}"
  local dest="$APP_WORKDIR/cache/$repo/$path"
  local dest_dir
  dest_dir="$(dirname "$dest")"
  mkdir -p "$dest_dir"
  local ts start end secs status note rc=0 src=""
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  start="$(date +%s)"

  # Prefer explicit local from manifest, then APP_LOCAL_ROOT/{repo}/{path}
  if [[ -n "$local_hint" && -f "$local_hint" ]]; then
    src="$local_hint"
  elif [[ -n "$APP_LOCAL_ROOT" && -f "$APP_LOCAL_ROOT/$repo/$path" ]]; then
    src="$APP_LOCAL_ROOT/$repo/$path"
  fi

  if [[ -n "$src" ]]; then
    # Use local file (copy into cache for consistent run path)
    if ! cp -f "$src" "$dest" 2>/dev/null; then
      end="$(date +%s)"; secs=$((end - start))
      note="local_copy_fail"
      status="skip"
      log_line "$(python3 -c 'import json,sys; print(json.dumps({"ts":sys.argv[1],"repo":sys.argv[2],"path":sys.argv[3],"status":sys.argv[4],"secs":int(sys.argv[5]),"note":sys.argv[6]},separators=(",",":")))' "$ts" "$repo" "$path" "$status" "$secs" "$note")"
      return 0
    fi
    note="local"
  else
    local enc raw_enc
    enc="$(urlencode_path "$path")"
    raw_enc="https://raw.githubusercontent.com/letsgo0226/${repo}/main/${enc}"
    if ! curl -fsSL --max-time "$APP_TIMEOUT" "$raw_enc" -o "$dest" 2>/dev/null; then
      end="$(date +%s)"; secs=$((end - start))
      note="curl_fail"
      status="skip"
      log_line "$(python3 -c 'import json,sys; print(json.dumps({"ts":sys.argv[1],"repo":sys.argv[2],"path":sys.argv[3],"status":sys.argv[4],"secs":int(sys.argv[5]),"note":sys.argv[6]},separators=(",",":")))' "$ts" "$repo" "$path" "$status" "$secs" "$note")"
      return 0
    fi
    note="ok"
  fi

  if [[ "$kind" == "sh" ]]; then
    if timeout "$APP_TIMEOUT" bash "$dest" >/dev/null 2>&1; then
      status="pass"; rc=0
    else
      rc=$?
      if [[ $rc -eq 124 ]]; then status="timeout"; note="timeout"
      else status="fail"; note="exit_$rc"
      fi
    fi
  elif [[ "$kind" == "json" ]]; then
    if timeout "$APP_TIMEOUT" python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$dest" >/dev/null 2>&1; then
      status="pass"; rc=0
    else
      rc=$?
      if [[ $rc -eq 124 ]]; then status="timeout"; note="timeout"
      else status="fail"; note="exit_$rc"
      fi
    fi
  else
    # py (default)
    if timeout "$APP_TIMEOUT" python3 "$dest" >/dev/null 2>&1; then
      status="pass"; rc=0
    else
      rc=$?
      if [[ $rc -eq 124 ]]; then status="timeout"; note="timeout"
      else status="fail"; note="exit_$rc"
      fi
    fi
  fi
  end="$(date +%s)"; secs=$((end - start))
  log_line "$(python3 -c 'import json,sys; print(json.dumps({"ts":sys.argv[1],"repo":sys.argv[2],"path":sys.argv[3],"status":sys.argv[4],"secs":int(sys.argv[5]),"note":sys.argv[6]},separators=(",",":")))' "$ts" "$repo" "$path" "$status" "$secs" "$note")"
}

one_pass() {
  local n=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" ]] && continue
    if [[ "$APP_MAX" != "0" && "$n" -ge "$APP_MAX" ]]; then
      break
    fi
    # parse with python for robust JSON
    local repo path kind raw local_path
    eval "$(python3 -c 'import json,sys,shlex; o=json.loads(sys.argv[1]);
print("repo="+shlex.quote(o["repo"]));
print("path="+shlex.quote(o["path"]));
print("kind="+shlex.quote(o["kind"]));
print("raw="+shlex.quote(o.get("raw","")));
print("local_path="+shlex.quote(o.get("local","")))' "$line")"
    run_one "$repo" "$path" "$kind" "$raw" "$local_path"
    n=$((n + 1))
    sleep "$APP_INTERVAL"
  done <"$APP_MANIFEST"
}

boot_ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
log_line "$(python3 -c 'import json,sys; print(json.dumps({"ts":sys.argv[1],"daemon":"ALL_PUBLIC_PROGRAMS","mode":sys.argv[2],"interval":int(sys.argv[3]),"cycle_sleep":int(sys.argv[4]),"timeout":int(sys.argv[5]),"max":int(sys.argv[6]),"manifest":sys.argv[7],"local_root":sys.argv[8]},separators=(",",":")))' "$boot_ts" "$MODE" "$APP_INTERVAL" "$APP_CYCLE_SLEEP" "$APP_TIMEOUT" "$APP_MAX" "$APP_MANIFEST" "$APP_LOCAL_ROOT")"

if [[ "$MODE" == "once" ]]; then
  one_pass
  exit 0
fi

while true; do
  one_pass
  sleep "$APP_CYCLE_SLEEP"
done
