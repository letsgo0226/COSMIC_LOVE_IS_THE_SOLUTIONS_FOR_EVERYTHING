#!/usr/bin/env bash
# Prime_Factor_Godel_TM_2KB — resident certify loop
# Usage: bash Prime_Factor_Godel_TM_2KB_DAEMON.sh [interval_sec] [N]
# Env: PFG_INTERVAL, PFG_N, PFG_LOG, PFG_SCRIPT
set -u
INTERVAL="${1:-${PFG_INTERVAL:-60}}"
N="${2:-${PFG_N:-4}}"
LOG="${PFG_LOG:-prime_factor_godel_tm_daemon.log}"
DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd || pwd)"
SCRIPT="${PFG_SCRIPT:-$DIR/Prime_Factor_Godel_TM_2KB.sh}"
RAW_URL="https://raw.githubusercontent.com/letsgo0226/Zeta.sh/main/Prime_Factor_Godel_TM_2KB.sh"

if [[ ! -f "$SCRIPT" ]]; then
  command -v curl >/dev/null || { echo "need curl or local script" >&2; exit 127; }
  SCRIPT="${TMPDIR:-/tmp}/Prime_Factor_Godel_TM_2KB.sh"
  curl -fsSL "$RAW_URL" -o "$SCRIPT" || exit 1
fi
command -v python3 >/dev/null || exit 127

echo "{\"daemon\":\"PRIME_FACTOR_GODEL_TM\",\"interval\":$INTERVAL,\"N\":$N,\"script\":\"$SCRIPT\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" | tee -a "$LOG"

while true; do
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  OUT=$(mktemp)
  if bash "$SCRIPT" "$N" >"$OUT" 2>"${OUT}.err"; then
    if python3 - "$OUT" <<'PY'
import json,sys
o=json.load(open(sys.argv[1]))
ok=(o.get("model")=="PRIME_FACTOR_GODEL_TM"
    and o.get("exact") is True
    and o.get("omega_attained")==0
    and o.get("program_equals_zeta")==0
    and o.get("open")==1
    and o.get("final")==0)
print(json.dumps({"ok":ok,"exact":o.get("exact"),"levels":len(o.get("levels") or []),"open":o.get("open"),"final":o.get("final")},separators=(",",":")))
sys.exit(0 if ok else 2)
PY
    then
      echo "{\"ts\":\"$TS\",\"status\":\"pass\"} $(tr -d '\n' <"$OUT")" >>"$LOG"
    else
      echo "{\"ts\":\"$TS\",\"status\":\"assert_fail\"} $(head -c 500 "$OUT" | tr -d '\n')" >>"$LOG"
    fi
  else
    echo "{\"ts\":\"$TS\",\"status\":\"run_fail\",\"err\":\"$(head -c 300 "${OUT}.err" | tr '\n' ' ')\"}" >>"$LOG"
  fi
  rm -f "$OUT" "${OUT}.err"
  sleep "$INTERVAL"
done
