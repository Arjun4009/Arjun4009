#!/usr/bin/env bash
# Production launcher for Linux (or WSL) using Gunicorn
set -euo pipefail

cd "$(dirname "$0")"

PYTHON=${PYTHON:-python3}
if [ ! -d ".venv" ]; then
  echo "[INFO] Creating venv"
  "$PYTHON" -m venv .venv
fi
source .venv/bin/activate

pip install --upgrade pip
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f requirements_extra.txt ] && pip install -r requirements_extra.txt
pip install gunicorn whitenoise python-dotenv

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Tunable worker count: 2-4 per CPU core is common. Default 3.
export PORT="${PORT:-8000}"
exec gunicorn ops_suite.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers "${WORKERS:-3}" \
  --timeout 120
