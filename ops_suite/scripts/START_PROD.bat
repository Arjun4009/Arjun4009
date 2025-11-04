@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

where py >nul 2>&1
if errorlevel 1 (
    echo Python launcher (py.exe) not found.
    exit /b 1
)

py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.11 is required. Run scripts\INIT_WINDOWS.bat first.
    exit /b 1
)

if not exist "%PROJECT_DIR%\.venv" (
    echo Virtual environment missing. Run scripts\INIT_WINDOWS.bat first.
    exit /b 1
)

pushd "%PROJECT_DIR%" || exit /b 1
call .venv\Scripts\activate.bat || goto :error

py -3.11 manage.py collectstatic --noinput || goto :error

echo [OPS Suite] Serving with Waitress on http://0.0.0.0:8080/
waitress-serve --listen=0.0.0.0:8080 ops_suite.wsgi:application
set "EXIT_CODE=%errorlevel%"

deactivate >nul 2>&1
popd
exit /b %EXIT_CODE%

:error
echo [OPS Suite] Failed with error %errorlevel%.
popd
exit /b %errorlevel%
