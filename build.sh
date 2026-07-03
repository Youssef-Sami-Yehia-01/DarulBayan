#!/usr/bin/env bash
# Render build script: install, collect static files, migrate, ensure admin.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py ensure_superuser
