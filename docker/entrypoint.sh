#!/bin/sh
set -eu

mkdir -p /app/instance /app/app/static/uploads/avatars

# Zapewnienie trwałego SECRET_KEY między restartami kontenera
# jeśli klucz nie został podany jawnie w zmiennych środowiskowych lub pliku .env.
if [ -z "${SECRET_KEY:-}" ]; then
    SECRET_FILE="/app/instance/.secret_key"
    if [ ! -s "$SECRET_FILE" ]; then
        python -c "import secrets; print(secrets.token_urlsafe(48), end='')" > "$SECRET_FILE"
        chmod 600 "$SECRET_FILE"
        echo "[docker-entrypoint] Wygenerowano i zapisano nowy klucz SECRET_KEY w $SECRET_FILE."
    fi
    SECRET_KEY="$(cat "$SECRET_FILE")"
    export SECRET_KEY
fi

python /app/docker/init_db.py

exec "$@"
