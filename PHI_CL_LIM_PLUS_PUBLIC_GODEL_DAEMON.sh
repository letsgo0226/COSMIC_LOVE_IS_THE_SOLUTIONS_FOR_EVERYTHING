#!/usr/bin/env bash
# Phi_CL^lim++ PublicWorld Godel — resident certify loop
# Usage: bash PHI_CL_LIM_PLUS_PUBLIC_GODEL_DAEMON.sh [interval_sec] [N]
# Env: PHI_CL_INTERVAL, PHI_CL_N, PHI_CL_LOG, PHI_CL_SCRIPT, GH_TOKEN/GITHUB_TOKEN
set -u
INTERVAL="${1:-${PHI_CL_INTERVAL:-60}}"
N="${2:-${PHI_CL_N:-4}}"
LOG="${PHI_CL_LOG:-phi_cl_lim_pp_daemon.log}"
DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd || pwd)"
SCRIPT="${PHI_CL_SCRIPT:-$DIR/PHI_CL_LIM_PLUS_PUBLIC_GODEL_ONELINER.sh}"
RAW_URL="https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/PHI_CL_LIM_PLUS_PUBLIC_GODEL_ONELINER.sh"

if [[ ! -f "$SCRIPT" ]]; then
  command -v curl >/dev/null || { echo "need curl or local oneliner" >&2; exit 127; }
  SCRIPT="${TMPDIR:-/tmp}/PHI_CL_LIM_PLUS_PUBLIC_GODEL_ONELINER.sh"
  curl -fsSL "$RAW_URL" -o "$SCRIPT" || exit 1
fi
command -v python3 >/dev/null || exit 127
command -v bash >/dev/null || exit 127

echo "{\"daemon\":\"Phi_CL^lim++\",\"interval\":$INTERVAL,\"N\":$N,\"script\":\"$SCRIPT\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" | tee -a "$LOG"

while true; do
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  OUT=$(mktemp)
  if bash "$SCRIPT" "$N" >"$OUT" 2>"${OUT}.err"; then
    if python3 - "$OUT" <<'PY'
import json,sys
o=json.load(open(sys.argv[1]))
ok=(o.get("Phi")=="Phi_CL^lim++" and o.get("H")==0 and o.get("Done") is True
    and o.get("open")==1 and o.get("final")==0
    and (o.get("World") or {}).get("W_rev") is True
    and (o.get("Godel") or {}).get("exact") is True)
print(json.dumps({"ok":ok,"H":o.get("H"),"n":(o.get("World") or {}).get("n"),"W_bytes":(o.get("World") or {}).get("W_bytes"),"Ts":o.get("Ts")},separators=(",",":")))
sys.exit(0 if ok else 2)
PY
    then
      echo "{\"ts\":\"$TS\",\"status\":\"pass\"} $(cat "$OUT" | tr -d '\n')" >>"$LOG"
    else
      echo "{\"ts\":\"$TS\",\"status\":\"assert_fail\"} $(head -c 500 "$OUT" | tr -d '\n')" >>"$LOG"
    fi
  else
    echo "{\"ts\":\"$TS\",\"status\":\"run_fail\",\"err\":\"$(head -c 300 "${OUT}.err" | tr '\n' ' ')\"}" >>"$LOG"
  fi
  rm -f "$OUT" "${OUT}.err"
  sleep "$INTERVAL"
done
