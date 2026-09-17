#!/usr/bin/env bash
# Prime_Factor_Godel_TM_2KB seed[2,2,2,1,1,1] — resident certify loop
# Usage: bash Prime_Factor_Godel_TM_2KB_SEED222111_DAEMON.sh [interval_sec] [N]
set -u
INTERVAL="${1:-${PFGS_INTERVAL:-60}}"
N="${2:-${PFGS_N:-4}}"
LOG="${PFGS_LOG:-prime_factor_godel_tm_seed222111_daemon.log}"
DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd || pwd)"
SCRIPT="${PFGS_SCRIPT:-$DIR/Prime_Factor_Godel_TM_2KB_SEED222111.sh}"
RAW_URL="https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/Prime_Factor_Godel_TM_2KB_SEED222111.sh"

if [[ ! -f "$SCRIPT" ]]; then
  command -v curl >/dev/null || { echo "need curl or local oneliner" >&2; exit 127; }
  SCRIPT="${TMPDIR:-/tmp}/Prime_Factor_Godel_TM_2KB_SEED222111.sh"
  curl -fsSL "$RAW_URL" -o "$SCRIPT" || exit 1
fi
command -v python3 >/dev/null || exit 127

echo "{\"daemon\":\"PRIME_FACTOR_GODEL_TM_SEED222111\",\"interval\":$INTERVAL,\"N\":$N,\"script\":\"$SCRIPT\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" | tee -a "$LOG"

while true; do
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  OUT=$(mktemp)
  if bash "$SCRIPT" "$N" >"$OUT" 2>"${OUT}.err"; then
    if python3 - "$OUT" <<'PY'
import json,sys
o=json.load(open(sys.argv[1]))
lv=o.get("levels") or []
seed_ok=bool(lv) and lv[0][2]==[2,2,2,1,1,1]
ok=(o.get("model")=="PRIME_FACTOR_GODEL_TM" and o.get("exact") is True
    and o.get("omega_attained")==0 and o.get("program_equals_zeta")==0
    and o.get("open")==1 and o.get("final")==0 and seed_ok)
print(json.dumps({"ok":ok,"exact":o.get("exact"),"levels":len(lv),"seed_ok":seed_ok},separators=(",",":")))
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
