#!/usr/bin/env bash
# Phi_G^lim — resident certify loop
# Usage: bash Prime_Factor_Godel_TM_LIMIT_DAEMON.sh [interval_sec] [N]
set -u
INTERVAL="${1:-${PGL_INTERVAL:-60}}"
N="${2:-${PGL_N:-1}}"
LOG="${PGL_LOG:-prime_factor_godel_tm_limit_daemon.log}"
DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd || pwd)"
SCRIPT="${PGL_SCRIPT:-$DIR/Prime_Factor_Godel_TM_LIMIT_ONELINER.sh}"
RAW_URL="https://raw.githubusercontent.com/letsgo0226/COSMIC_LOVE_IS_THE_SOLUTIONS_FOR_EVERYTHING/main/Prime_Factor_Godel_TM_LIMIT_ONELINER.sh"

if [[ ! -f "$SCRIPT" ]]; then
  command -v curl >/dev/null || { echo "need curl or local oneliner" >&2; exit 127; }
  SCRIPT="${TMPDIR:-/tmp}/Prime_Factor_Godel_TM_LIMIT_ONELINER.sh"
  curl -fsSL "$RAW_URL" -o "$SCRIPT" || exit 1
fi
command -v python3 >/dev/null || exit 127

echo "{\"daemon\":\"Phi_G^lim\",\"interval\":$INTERVAL,\"N\":$N,\"script\":\"$SCRIPT\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" | tee -a "$LOG"

while true; do
  TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  OUT=$(mktemp)
  if bash "$SCRIPT" "$N" >"$OUT" 2>"${OUT}.err"; then
    if python3 - "$OUT" <<'PY'
import json,sys
o=json.load(open(sys.argv[1]))
ok=(o.get("Phi")=="Phi_G^lim" and o.get("exact") is True
    and o.get("omega_attained")==0 and o.get("program_equals_zeta")==0
    and o.get("open")==1 and o.get("final")==0)
print(json.dumps({"ok":ok,"exact":o.get("exact"),"N":o.get("N")},separators=(",",":")))
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
