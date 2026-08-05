#!/usr/bin/env bash
# Fast local preview: export static site and serve (no on-demand compilation).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PORT="${1:-3340}"
EXPORT_DIR="$ROOT/.mint-export"
ZIP="$ROOT/scripts/export.zip"

export PATH="/opt/homebrew/Cellar/node@22/22.22.3/bin:$PATH"

echo "Exporting static site (this may take several minutes)..."
mint export --output "$ZIP"

rm -rf "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR"
unzip -q -o "$ZIP" -d "$EXPORT_DIR"

echo ""
echo "Serving static export at:"
echo "  http://localhost:$PORT"
echo "  http://$(ipconfig getifaddr en0 2>/dev/null || hostname):$PORT"
echo ""
python3 -m http.server "$PORT" --directory "$EXPORT_DIR"
