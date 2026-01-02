#!/usr/bin/env bash
# run_server.sh - POSIX shell helper for Linux/macOS/WSL
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Creating virtualenv .venv with python3..."
  python3 -m venv .venv
fi

echo "Activating virtualenv..."
. .venv/bin/activate

echo "Upgrading pip and installing dev requirements..."
python -m pip install --upgrade pip
if [ -f requirements-dev.txt ]; then
  python -m pip install -r requirements-dev.txt
fi

echo "Applying migrations..."
python manage.py migrate

echo "Starting Django dev server (in background)..."
python manage.py runserver &
sleep 2
xdg-open http://127.0.0.1:8000/ 2>/dev/null || open http://127.0.0.1:8000/ || echo "Open http://127.0.0.1:8000/ in your browser"

echo "Server started. Use 'fg' or check the background job to stop it." 
