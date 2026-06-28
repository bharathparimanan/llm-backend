#!/usr/bin/env bash
# Start the development server with hot-reload.
# Usage: ./scripts/start.sh

set -euo pipefail

uvicorn app.main:app \
  --host "${HOST:-0.0.0.0}" \
  --port "${PORT:-8000}" \
  --reload \
  --log-level info
