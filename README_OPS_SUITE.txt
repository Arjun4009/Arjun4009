OPS Suite — Windows Helpers
===========================

These helpers assume your project root already has:
- manage.py
- ops_suite/ (settings, wsgi, etc.)
- requirements.txt and requirements_extra.txt

They are **safe to drop into your project root**. No code changes are required.

Files included
--------------
1) START_DEV.bat
   • Uses your system Python 3.11 (via `py -3.11`) directly.
   • Installs requirements (skips if already satisfied), runs migrations, collects static,
     and launches Django dev server with autoreload.
   • URL: http://127.0.0.1:8000/

2) START_PROD.bat
   • Runs Django via Waitress (production-friendly, Windows-compatible).
   • Serves `ops_suite.wsgi:application` on http://127.0.0.1:8080/
   • Uses WhiteNoise for static files (you already installed `whitenoise`).
   • NOTE: For true production, put a reverse proxy (e.g., nginx/Apache) in front.

3) COLLECTSTATIC.bat
   • Runs `manage.py collectstatic --noinput`

4) CREATE_SUPERUSER.bat
   • Creates a superuser if missing using environment variables:
       DJ_SUPERUSER_USERNAME, DJ_SUPERUSER_EMAIL, DJ_SUPERUSER_PASSWORD
     Example:
       set DJ_SUPERUSER_USERNAME=Arjun
       set DJ_SUPERUSER_EMAIL=arjun@example.com
       set DJ_SUPERUSER_PASSWORD=Bubbles
       CREATE_SUPERUSER.bat

5) .env.example  (optional)
   • Copy to `.env` and customize. Safe defaults for local dev.

How to use quickly
------------------
1) Drop all files next to your `manage.py` (project root).
2) Double‑click `START_DEV.bat` to run locally on port 8000.
3) For a Windows production-style run, use `START_PROD.bat` (port 8080).

If you see a staticfiles warning again
--------------------------------------
- Create a `static/` folder in your project root OR
- Use the settings "static guard" snippet we discussed to make STATICFILES_DIRS optional.

Logs to DB
----------
- Your apps can write to the DB using Django logging (LOGGING in settings) or custom models.
- Once you add your log models/handlers, these scripts don't need changes; they just run your project.

Enjoy! — Junz Ops Helpers