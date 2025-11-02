@echo off
setlocal enabledelayedexpansion

REM Windows "production-style" run using Waitress
REM Requires: waitress, whitenoise, python-dotenv (already in requirements_extra.txt)

echo [INFO] Using: py -3.11
py -3.11 --version || (
  echo [ERROR] Python 3.11 not found via launcher. Install Python 3.11 from python.org or adjust this script to your path.
  pause
  exit /b 1
)

echo.
echo === Install requirements (idempotent) ===
py -3.11 -m pip install -r requirements.txt || goto :pip_fail
if exist requirements_extra.txt (
  py -3.11 -m pip install -r requirements_extra.txt || goto :pip_fail
)

echo.
echo === Apply migrations ===
py -3.11 manage.py migrate || goto :migrate_fail

echo.
echo === Collect static ===
py -3.11 manage.py collectstatic --noinput

echo.
echo === Start Waitress on http://127.0.0.1:8080 ===
py -3.11 -m waitress --listen=127.0.0.1:8080 ops_suite.wsgi:application
goto :eof

:pip_fail
echo [ERROR] Pip install failed.
pause
exit /b 1

:migrate_fail
echo [ERROR] Migrate failed.
pause
exit /b 1
