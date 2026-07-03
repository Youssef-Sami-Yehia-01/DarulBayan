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
- apps/core — shared mixins, context processors, generic modal CRUD views
- apps/accounts — custom user `accounts.User` with `role`; login + role dispatch (/login/ → portal or panel)
- apps/website — public site: info pages (DB-driven), events, newsletter, gallery, enquiries
- apps/panel — staff admin panel (/panel/): modal CRUD for all content, users, classes, students, announcements
- apps/portals — teacher/student/parent portals (/portal/…): classes, attendance, homework, grades, announcements
- templates/ — base.html + components/ partials + per-app folders
- static/css/ — variables.css (design tokens), base.css, components/, panel/, portals/, website/

## Key conventions
- Modal CRUD: views mix apps.core.views.ModalFormMixin / BaseModalDeleteView with an
  access mixin; fragments load into components/modal.html via static/js/modal.js
  (GET fragment, POST → 204 success / 400 re-render).
- The site logo is white-on-transparent: only place it on the blue header/sidebar
  or inside a .logo-badge wrapper.
- Nav highlighting: views set nav_section (NavSectionMixin); links render through
  components/nav_link.html.

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
