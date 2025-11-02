@echo off
setlocal
cd /d "%~dp0"

REM === Dev launcher without venv ===
where py >NUL 2>&1
if %ERRORLEVEL%==0 (
  for /f "tokens=*" %%v in ('py -0p 2^>NUL ^| find "3.11"') do set PY=py -3.11
) else (
  set PY=python
)

echo [INFO] Using: %PY%
if exist requirements.txt %PY% -m pip install -r requirements.txt
if exist requirements_extra.txt %PY% -m pip install -r requirements_extra.txt

%PY% manage.py migrate --noinput
%PY% manage.py init_ops || echo [INFO] init_ops missing or already ran
%PY% manage.py collectstatic --noinput
%PY% manage.py runserver 0.0.0.0:8000
