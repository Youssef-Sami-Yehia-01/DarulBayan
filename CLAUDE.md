# Darulbayan — School Website + Management System

Django rebuild of https://www.darulbayan.co.uk/ plus role-based portals
(student / parent / teacher / management) and a custom admin panel that
edits all site content (events, newsletter, gallery, images).

## Stack
- Django 6 / Python 3.13 (venv at .venv)
- Postgres on Neon via DATABASE_URL (SQLite fallback in dev)
- Cloudflare R2 for uploads via django-storages (local media/ fallback)
- Hosting target: Render free tier; WhiteNoise serves static files
- No CSS frameworks — hand-written CSS matching the original site

## Layout
- config/ — env-driven settings, root urls
- apps/core — shared utilities and template components
- apps/accounts — custom user model `accounts.User` with `role` field
- apps/website — public site: pages, events, newsletter, gallery, enquiries
- templates/ — base.html + components/ partials + per-app folders
- static/css/ — variables.css (design tokens), base.css, components/

## Design tokens (sampled from the original site)
Primary #1976d2, accent #ffbf00, text #000000 / #444950, backgrounds
#ffffff / #f9f9f9 / #ebedf0, borders #e0e0e0 / #d4d7e5. Font: 'Caladea'
(Google Fonts) for everything, Arial fallback. Always use the CSS
variables in static/css/variables.css — never raw hex in components.

## Client rules — always follow
- No inline styles/scripts; keep files small and modular
- No duplicated code — build reusable components/partials
- No Bootstrap/Tailwind or any CSS framework
- No hardcoded values or placeholder content; site content is DB-driven
- Everything responsive: desktop, tablet, mobile
- Create/edit flows (users, staff, etc.) open in popup modals, not pages
- Clean, commented code that is cheap for AI to read

## Commands (Windows)
- Run dev server: `.venv\Scripts\python manage.py runserver`
- Migrations: `.venv\Scripts\python manage.py makemigrations` then `migrate`
