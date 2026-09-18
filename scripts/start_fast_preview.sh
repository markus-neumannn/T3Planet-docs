#!/usr/bin/env bash
# Fast local preview: mint (compile) on :3001 + HTML/RSC cache proxy on :3000
# After first warm, cached pages load in ~1–5ms (vs 6–20s raw mint cold compile).
set -euo pipefail
export PATH="/opt/homebrew/opt/node@22/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:${PATH:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Only recycle our proxy — do not pkill mint when mintlify-dev/run.sh owns :3001
# (killing mint causes a restart loop and 502s through the proxy).
pkill -f 'mint_cache_proxy.py' 2>/dev/null || true
sleep 1
pids=$(lsof -tiTCP:3000 -sTCP:LISTEN 2>/dev/null || true)
[ -n "${pids:-}" ] && kill -9 $pids 2>/dev/null || true
sleep 1

echo "Refreshing homepage Documentation pages / Products counts..."
python3 "$ROOT/scripts/compute_doc_stats.py"

mint_ok=0
if curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:3001/ | grep -q 200; then
  echo "Reusing existing mint on :3001"
  mint_ok=1
  MINT_PID=$(lsof -tiTCP:3001 -sTCP:LISTEN 2>/dev/null | head -1 || echo "")
else
  echo "Starting mint on :3001..."
  node /opt/homebrew/lib/node_modules/mint/node_modules/@mintlify/cli/bin/start.js dev --no-open --port 3001 \
    > /tmp/mint-fast-3001.log 2>&1 &
  MINT_PID=$!
  for i in $(seq 1 40); do
    if curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://127.0.0.1:3001/ | grep -q 200; then
      echo "mint ready (try $i)"
      mint_ok=1
      break
    fi
    sleep 3
  done
fi

if [ "$mint_ok" != "1" ]; then
  echo "ERROR: mint on :3001 is not ready" >&2
  exit 1
fi

echo "Starting cache proxy on :3000..."
MINT_ORIGIN=http://127.0.0.1:3001 PROXY_HOST=0.0.0.0 PROXY_PORT=3000 \
  python3 "$ROOT/scripts/mint_cache_proxy.py" > /tmp/mint-fast-proxy.log 2>&1 &
PROXY_PID=$!
sleep 1

LAN=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1")
echo ""
echo "Fast docs preview (use :3000 — not raw mint):"
echo "  http://127.0.0.1:3000/"
echo "  http://${LAN}:3000/   (LAN)"
echo "  http://127.0.0.1:3001/   (raw mint — slow, avoid)"
echo "mint_pid=${MINT_PID:-existing} proxy_pid=$PROXY_PID"
echo "Warming common pages (correct ExtNs paths)..."
for path in \
  / \
  /AIFoundationExtensions/Index \
  /AllExtensions/Index \
  /AllTemplates/Index \
  /License/Index \
  /License/Introduction/Index \
  /ExtNsT3AF/Index \
  /ExtNsT3AF/Introduction/Index \
  /ExtNsT3AF/Installation/Index \
  /ExtNsT3AF/DPAandGDPR/Index \
  /ExtNsT3AF/Configuration/AIPermissions/Index \
  /ExtNsT3AA/Index \
  /ExtNsT3AA/DPAandGDPR/Index \
  /ExtNsT3AI/Index \
  /ExtNsT3AI/DPAandGDPR/Index \
  /EXTKarma/Index \
  ; do
  curl -s -o /dev/null --max-time 180 "http://127.0.0.1:3000$path" || true
  echo "  warmed $path"
done
# Kick proxy background warm for the full hub catalog (non-blocking for the user).
curl -s "http://127.0.0.1:3000/__t3_cache_warm?all=1" >/dev/null 2>&1 || true
echo "Done. Hard-refresh http://127.0.0.1:3000/  (or http://${LAN}:3000/)"
echo "Keep this terminal open (mint=${MINT_PID:-existing} proxy=$PROXY_PID)."
disown $PROXY_PID 2>/dev/null || true
[ -n "${MINT_PID:-}" ] && disown $MINT_PID 2>/dev/null || true
