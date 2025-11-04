@echo off
setlocal enabledelayedexpansion

REM Ensure the script runs from the project root (one level up from scripts).
set SCRIPT_DIR=%~dp0
pushd "%SCRIPT_DIR%.." >nul 2>&1
if errorlevel 1 (
    echo Failed to change directory to project root from %SCRIPT_DIR%.
    exit /b 1
)

if "%~1"=="" (
    echo Usage: scripts\PUSH_TO_GITHUB.bat ^<https-remote-url^>
    echo Example: scripts\PUSH_TO_GITHUB.bat https://github.com/username/OPS_Suite.git
    popd >nul
    exit /b 1
)

set REMOTE_URL=%~1

git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not available on PATH. Install Git and retry.
    popd >nul
    exit /b 1
)

REM Configure or update the origin remote.
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Configuring origin remote to !REMOTE_URL!
    git remote add origin "!REMOTE_URL!"
    if errorlevel 1 (
        echo Failed to add origin remote.
        popd >nul
        exit /b 1
    )
) else (
    echo Updating origin remote to !REMOTE_URL!
    git remote set-url origin "!REMOTE_URL!"
    if errorlevel 1 (
        echo Failed to update origin remote.
        popd >nul
        exit /b 1
    )
)

echo Pushing current HEAD to origin\main ...
git push origin HEAD:main
if errorlevel 1 (
    echo Git push failed. Check your credentials or remote permissions.
    popd >nul
    exit /b 1
)

echo Push completed successfully.

popd >nul
exit /b 0
