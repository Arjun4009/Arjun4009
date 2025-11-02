OPS Suite — Dev + Production Launchers
======================================

What you got
------------
- RUN_OPS_SUITE.bat              → Dev (with venv), safe, idempotent
- RUN_OPS_SUITE_NO_VENV.bat      → Dev (global Python), if venv is blocked
- RUN_OPS_SUITE_PROD_WINDOWS.bat → Production-like on Windows (Waitress + WhiteNoise)
- RUN_OPS_SUITE_PROD_GUNICORN.sh → Production on Linux/WSL (Gunicorn + WhiteNoise)
- settings_static_snippet.txt    → Fix STATICFILES_DIRS warning safely
- settings_production_snippet.txt→ Hardened static + WhiteNoise + .env loader
- requirements_extra.txt         → Extra deps (whitenoise, dotenv, waitress, gunicorn)


Quick start (Dev)
-----------------
1) Drop these files in your **project root** (where `manage.py` lives).
2) (Optional) Create a folder named `static` in project root to silence W004.
3) Double-click `RUN_OPS_SUITE.bat`. It will:
   - create & activate `.venv`
   - install requirements
   - run makemigrations (safe), migrate, init_ops (if present), collectstatic
   - start dev server at http://127.0.0.1:8000

If venv creation fails on your machine, use `RUN_OPS_SUITE_NO_VENV.bat`.


Production-like on Windows (Waitress)
-------------------------------------
1) (Recommended) Append contents of `settings_production_snippet.txt` to
   your `ops_suite/settings.py` (or integrate it cleanly).
2) Ensure you have a `.env` in project root with at least:
     SECRET_KEY=change_me
     DEBUG=false
     ALLOWED_HOSTS=127.0.0.1,localhost
3) Double-click `RUN_OPS_SUITE_PROD_WINDOWS.bat`.
   - This will serve via waitress-serve (WSGI), better than Django dev server.
   - Static files will be served by WhiteNoise from `static_root/`.

Production on Linux / WSL (Gunicorn)
------------------------------------
1) Copy all files to the server (or WSL path).
2) Make the script executable: `chmod +x RUN_OPS_SUITE_PROD_GUNICORN.sh`
3) Run: `PORT=8000 ./RUN_OPS_SUITE_PROD_GUNICORN.sh`
4) Put it behind Nginx for TLS and caching.

Notes
-----
- These launchers are **drop-in** and do not modify your code.
- They assume your Django project module is `ops_suite` with `wsgi.py` present.
- If you see STATICFILES_DIRS warnings, either create `static/` or use the provided snippet.
- `init_ops` is optional. If you don't have that management command, it's safely skipped.