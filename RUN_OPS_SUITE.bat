@echo off
setlocal enabledelayedexpansion

REM === Dev launcher with venv (prefers Python 3.11) ===
cd /d "%~dp0"

REM Try to find Python
where py >NUL 2>&1
if %ERRORLEVEL%==0 (
  for /f "tokens=*" %%v in ('py -0p 2^>NUL ^| find "3.11"') do set PY=py -3.11
) else (
  set PY=python
)

if not defined PY set PY=python

echo [INFO] Using Python launcher: %PY%

REM Create venv if missing
if not exist .venv (
  echo [INFO] Creating virtual environment .venv
  %PY% -m venv .venv
  if errorlevel 1 (
    echo [WARN] Could not create venv. Falling back to global interpreter.
    goto RUN_GLOBAL
  )
)

REM Activate venv
call .venv\Scripts\activate.bat

echo [INFO] Upgrading pip
python -m pip install --upgrade pip

echo [INFO] Installing requirements (main + extras if present)
if exist requirements.txt python -m pip install -r requirements.txt
if exist requirements_extra.txt python -m pip install -r requirements_extra.txt

echo [INFO] Django prep: makemigrations (safe), migrate, init, collectstatic
if exist manage.py (
  python manage.py makemigrations --noinput || echo [WARN] makemigrations returned non-zero (may be fine)
  python manage.py migrate --noinput || ( echo [ERROR] migrate failed & goto :END )
  python manage.py init_ops || echo [INFO] init_ops command missing or already ran
  python manage.py collectstatic --noinput
) else (
  echo [ERROR] manage.py not found in %cd%
  goto END
)

echo [INFO] Starting Django dev server at http://127.0.0.1:8000
python manage.py runserver 0.0.0.0:8000
goto END

:RUN_GLOBAL
echo [INFO] Running without venv
if exist requirements.txt %PY% -m pip install -r requirements.txt
if exist requirements_extra.txt %PY% -m pip install -r requirements_extra.txt
%PY% manage.py migrate --noinput
%PY% manage.py init_ops || echo [INFO] init_ops missing or already ran
%PY% manage.py collectstatic --noinput
%PY% manage.py runserver 0.0.0.0:8000

:END
echo.
echo [DONE]
timeout /t 2 >NUL
