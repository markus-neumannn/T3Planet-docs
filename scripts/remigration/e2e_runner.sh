#!/bin/bash
# Durable E2E runner for LaunchAgent. Resumes from e2e_progress.json.
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT" || exit 1
export PATH="/opt/homebrew/Cellar/node@22/22.22.3/bin:/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export PYTHONUNBUFFERED=1
LOG="$ROOT/scripts/remigration/e2e_run.log"
STATUS="$ROOT/scripts/remigration/e2e_runner.status"
echo "started $(date) pid=$$ root=$ROOT" > "$STATUS"

for round in $(seq 1 120); do
  left=$(cd "$ROOT/scripts/remigration" && /usr/bin/python3 -c '
import json
from pathlib import Path
from route_link_check import load_docs_json, collect_nav_paths
nav = sorted(collect_nav_paths(load_docs_json().get("navigation")))
prog = json.loads(Path("e2e_progress.json").read_text())
print(sum(1 for p in nav if prog.get(p, {}).get("status") != "ok"))
')
  echo "[runner $(date '+%F %T')] round=$round left=$left" | tee -a "$LOG" >> "$STATUS"
  if [ "$left" = "0" ]; then
    echo "[runner] COMPLETE" | tee -a "$LOG" >> "$STATUS"
    /usr/bin/python3 -u scripts/remigration/e2e_batch_check.py --batch-size 15 >> "$LOG" 2>&1
    exit 0
  fi
  pcode=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://127.0.0.1:3000/ || echo 000)
  if [ "$pcode" != "200" ]; then
    echo "[runner] kickstart (proxy=$pcode)" >> "$STATUS"
    /bin/launchctl kickstart -k "gui/$(/usr/bin/id -u)/com.nitsan.mintlify.dev" || true
    /bin/sleep 50
  fi
  /usr/bin/python3 -u scripts/remigration/e2e_batch_check.py --batch-size 10 --retry-failed >> "$LOG" 2>&1
  rc=$?
  echo "[runner] batch rc=$rc at $(date '+%T')" >> "$STATUS"
  /bin/sleep 2
done
echo "[runner] gave up" >> "$STATUS"
exit 1
