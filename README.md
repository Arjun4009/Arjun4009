# OPS Suite

OPS Suite is a Windows-friendly Django 5.2 application that centralises transition and offboarding workflows while recording activity history. The project ships with demo data seeders, database logging, and batch scripts for one-click setup and deployment.

## Quick Start

1. Clone the repository **or** download `OPS_Suite.zip` from the project root and extract it.
2. Run `INIT_WINDOWS.bat` (or `scripts\INIT_WINDOWS.bat`) to create the virtual environment, install dependencies, run migrations, collect static files, and create the default superuser.
3. Launch the development server with `START_DEV.bat` (or `scripts\START_DEV.bat`) and visit http://127.0.0.1:8000/ (you will be redirected to `/transitions/`).

## Project Layout

- **Project home folder**: `ops_suite/` (inside the repository root). This holds the Django settings package, apps, templates, and middleware.
- Root-level helpers:
  - `manage.py` — Django entry point.
  - `scripts/` — Windows batch utilities for setup, running, and maintenance.
  - `OPS_Suite.zip` — packaged copy of the entire project for quick download.

## Demo Data

- Seed transition sheets: http://127.0.0.1:8000/transitions/seed/
- Seed offboarding records: http://127.0.0.1:8000/offboarding/seed/

## Admin Access

- URL: http://127.0.0.1:8000/admin/
- Username: `Arjun`
- Password: `Bubbles`
- Email: `arjun@example.com`

Run `python manage.py ensure_superuser` (or rely on `INIT_WINDOWS.bat`) if the account is missing.

## Operations Scripts

- `INIT_WINDOWS.bat` / `scripts\INIT_WINDOWS.bat` — full environment setup and migrations.
- `START_DEV.bat` / `scripts\START_DEV.bat` — activate the virtual environment and run the Django development server.
- `START_PROD.bat` / `scripts\START_PROD.bat` — collect static files and serve using Waitress on port 8080.
- `FIX_MIGRATIONS.bat` / `scripts\FIX_MIGRATIONS.bat` — regenerate, merge, and apply migrations plus collect static files.
- `HARD_RESET_DB.bat` / `scripts\HARD_RESET_DB.bat` — rebuilds the SQLite database (destructive) and recreates the default superuser.

## Troubleshooting

- If pages warn about missing tables, run `FIX_MIGRATIONS.bat` (or `scripts\FIX_MIGRATIONS.bat`).
- Static files are served through WhiteNoise; rerun `collectstatic` if assets appear missing.
- Health check: http://127.0.0.1:8000/health/

## Downloadable Package

- `OPS_Suite.zip` — contains the complete project (manage.py, apps, scripts, and requirements). Download and extract this archive if you prefer a ready-to-run bundle instead of cloning via Git.

## Production

1. Run `INIT_WINDOWS.bat` (or `scripts\INIT_WINDOWS.bat`) once per environment or when dependencies change.
2. Execute `START_PROD.bat` (or `scripts\START_PROD.bat`) to serve OPS Suite with Waitress on port 8080.

## Publishing to GitHub

This environment is not connected to any remote repository. To push your latest
changes to GitHub:

1. Run `PUSH_TO_GITHUB.bat https://github.com/<user>/<repo>.git` (or `scripts\PUSH_TO_GITHUB.bat ...`) from a
   Windows terminal. The script will ensure you are in the project root,
   configure (or update) the `origin` remote, and push the current HEAD to the
   `main` branch.
2. If you prefer to run the commands manually, execute:
   - `git remote add origin <your-repo-url>` (skip if already set)
   - `git push origin HEAD:main`
3. Verify on GitHub that the commits appear on the `main` branch and any
   automations (such as CI or deployments) complete successfully.
