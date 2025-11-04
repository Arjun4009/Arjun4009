@echo off
setlocal ENABLEDELAYEDEXPANSION

set "SCRIPT_DIR=%~dp0"
if not defined SCRIPT_DIR (
    echo Unable to determine script directory.
    exit /b 1
)
set "PROJECT_DIR=%SCRIPT_DIR%.."

where py >nul 2>&1
if errorlevel 1 (
    echo Python launcher (py.exe) not found. Install Python 3.11 and try again.
    exit /b 1
)

py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.11 is required. Install it and ensure py -3.11 works.
    exit /b 1
)

pushd "%PROJECT_DIR%" || exit /b 1

if not exist .venv (
    echo [OPS Suite] Creating virtual environment...
    py -3.11 -m venv .venv || goto :error
) else (
    echo [OPS Suite] Using existing virtual environment.
)

call .venv\Scripts\activate.bat || goto :error

python -m pip install --upgrade pip || goto :error
pip install -r requirements.txt || goto :error
pip install -r requirements_extra.txt || goto :error

py -3.11 manage.py makemigrations activitylog transitions offboarding || goto :error
py -3.11 manage.py makemigrations --merge || goto :error
py -3.11 manage.py migrate || goto :error
py -3.11 manage.py ensure_superuser || goto :error
py -3.11 manage.py collectstatic --noinput || goto :error

echo [OPS Suite] Init complete.

popd
exit /b 0

:error
echo [OPS Suite] Failed with error %errorlevel%.
popd
exit /b %errorlevel%
