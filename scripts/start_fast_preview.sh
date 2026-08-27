#!/usr/bin/env bash
# Fast local preview: mint (compile) on :3001 + HTML/RSC cache proxy on :3000
# After first warm, cached pages load in ~1s (vs 6–12s raw mint dev).
set -euo pipefail
export PATH="/opt/homebrew/opt/node@22/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:${PATH:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

pkill -f 'mint_cache_proxy.py' 2>/dev/null || true
pkill -f 'mintlify/cli/bin/start.js' 2>/dev/null || true
pkill -f 'mint dev' 2>/dev/null || true
sleep 1
for p in 3000 3001; do
  pids=$(lsof -tiTCP:$p -sTCP:LISTEN 2>/dev/null || true)
  [ -n "${pids:-}" ] && kill -9 $pids 2>/dev/null || true
done
sleep 1

echo "Refreshing homepage Documentation pages / Products counts..."
python3 "$ROOT/scripts/compute_doc_stats.py"

echo "Starting mint on :3001..."
node /opt/homebrew/lib/node_modules/mint/node_modules/@mintlify/cli/bin/start.js dev --no-open --port 3001 \
  > /tmp/mint-fast-3001.log 2>&1 &
MINT_PID=$!

for i in $(seq 1 40); do
  if curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://127.0.0.1:3001/ | grep -q 200; then
    echo "mint ready (try $i)"
    break
  fi
  sleep 3
done

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
echo "mint_pid=$MINT_PID proxy_pid=$PROXY_PID"
echo "Warming common pages..."
for path in / /T3AF/Index /T3AF/Installation/Index /AllExtensions/Index /AllTemplates/Index /License/Index; do
  curl -s -o /dev/null --max-time 180 "http://127.0.0.1:3000$path" || true
  echo "  warmed $path"
done
echo "Done. Hard-refresh http://127.0.0.1:3000/  (or http://${LAN}:3000/)"
echo "Keep this terminal open (mint=$MINT_PID proxy=$PROXY_PID)."
# Keep children alive without blocking forever in tooling — disown
disown $MINT_PID $PROXY_PID 2>/dev/null || true
