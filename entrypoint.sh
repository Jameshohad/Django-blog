#!/bin/sh
set -e

python - <<'PY'
import os
import socket
import time

host = os.environ.get("POSTGRES_HOST")

if host:
    port = int(os.environ.get("POSTGRES_PORT", "5432"))

    for i in range(30):
        try:
            with socket.create_connection((host, port), timeout=2):
                print("Database is ready")
                break
        except OSError:
            print("Waiting for database...")
            time.sleep(2)
    else:
        raise SystemExit("Database is not available")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"