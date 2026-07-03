# Darulbayan — School Website & Management System

Django rebuild of [darulbayan.co.uk](https://www.darulbayan.co.uk/) with a
custom admin panel (events, newsletter, gallery, enquiries, users) and,
next, role-based portals for students, parents, teachers and management.

**Stack:** Django 6 · Neon Postgres · Cloudflare R2 (uploads) · Render (hosting)

## Local development

```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env   # then fill in the values
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py ensure_superuser
.venv\Scripts\python manage.py runserver
```

Public site at `/`, admin panel at `/panel/`.

## Deployment

Deployed on Render via [render.yaml](render.yaml) (Blueprint). The build
runs [build.sh](build.sh): install → collectstatic → migrate →
ensure_superuser. See [.env.example](.env.example) for every variable.

Project conventions and design tokens are documented in [CLAUDE.md](CLAUDE.md).
