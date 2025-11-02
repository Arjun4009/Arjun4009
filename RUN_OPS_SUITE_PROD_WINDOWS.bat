@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM === Production-like launcher for Windows using Waitress + WhiteNoise static ===

REM Choose Python
where py >NUL 2>&1
if %ERRORLEVEL%==0 (
  for /f "tokens=*" %%v in ('py -0p 2^>NUL ^| find "3.11"') do set PY=py -3.11
) else (
  set PY=python
)

REM Ensure venv
if not exist .venv (
  echo [INFO] Creating virtual environment .venv
  %PY% -m venv .venv || ( echo [ERROR] Could not create venv & exit /b 1 )
)
call .venv\Scripts\activate.bat

echo [INFO] Installing production deps
python -m pip install --upgrade pip
if exist requirements.txt python -m pip install -r requirements.txt
if exist requirements_extra.txt python -m pip install -r requirements_extra.txt
python -m pip install waitress whitenoise python-dotenv

REM Apply migrations & collect static
python manage.py migrate --noinput || ( echo [ERROR] migrate failed & exit /b 1 )
python manage.py collectstatic --noinput

REM Optional: load .env if present (Django can read via python-dotenv in settings)
set PORT=8000
if not "%PORT%"=="" (
  set BIND=0.0.0.0:%PORT%
) else (
  set BIND=0.0.0.0:8000
)

echo [INFO] Starting Waitress on %BIND%
waitress-serve --port=%PORT% --host=0.0.0.0 ops_suite.wsgi:application
