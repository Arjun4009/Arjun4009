@echo off
setlocal enabledelayedexpansion

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
echo === Collect static (safe if none) ===
py -3.11 manage.py collectstatic --noinput

echo.
echo === Start Django dev server (Ctrl+C to stop) ===
py -3.11 manage.py runserver 0.0.0.0:8000
goto :eof

:pip_fail
echo [ERROR] Pip install failed.
pause
exit /b 1

:migrate_fail
echo [ERROR] Migrate failed.
pause
exit /b 1
