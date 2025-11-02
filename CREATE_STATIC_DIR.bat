@echo off
setlocal enabledelayedexpansion
echo [STATIC FIX] Ensuring ".\static" exists...
if not exist ".\static" (
    mkdir ".\static"
    echo created ".\static"
) else (
    echo ".\static" already exists
)
echo Done.