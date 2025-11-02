OPS Suite — Static Files Warning Fix
====================================

You are seeing:
  (staticfiles.W004) The directory '<project>\static' in the STATICFILES_DIRS setting does not exist.

Two quick ways to fix it (pick ONE):

A) Create the folder:
   - Drop the 'static' folder from this ZIP into your project root (where manage.py lives).
   - Run collectstatic again if needed:
       py -3.11 manage.py collectstatic --noinput

B) Guard STATICFILES_DIRS in settings.py:
   - Open ops_suite/settings.py
   - Paste the contents of settings_static_guard.txt near your existing STATIC_URL/STATIC_ROOT section.
   - This makes STATICFILES_DIRS only point to BASE_DIR/static if it actually exists, removing W004.

Notes:
- In development, it's fine to keep STATICFILES_DIRS empty.
- In production (with WhiteNoise), you mainly serve from STATIC_ROOT after collectstatic.
- If you prefer zero warnings, option A is the quickest: keep an empty 'static' folder in the repo.

— Ready to drop-in.