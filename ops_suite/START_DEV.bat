@echo off
setlocal
set "SCRIPT_DIR=%~dp0scripts"
if not exist "%SCRIPT_DIR%" (
    echo [ERROR] scripts folder is missing.
    exit /b 1
)
call "%SCRIPT_DIR%\START_DEV.bat" %*
