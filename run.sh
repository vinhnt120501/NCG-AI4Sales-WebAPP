#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/salemate"

PORT="${PORT:-8501}"
URL="http://localhost:${PORT}"
LOG_FILE=".streamlit/run.log"

if [ -x ".venv/bin/streamlit" ]; then
  STREAMLIT=".venv/bin/streamlit"
else
  STREAMLIT="streamlit"
fi

command -v open >/dev/null 2>&1 && open "$URL" >/dev/null 2>&1 || true

exec "$STREAMLIT" run app.py \
  --server.headless true \
  --server.port "$PORT" \
  --browser.gatherUsageStats false \
  --logger.level error \
  >"$LOG_FILE" 2>&1
