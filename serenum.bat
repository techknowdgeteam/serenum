@echo off
title Serenum Automation Launcher
color 0A

echo ========================================
echo   SERENUM AUTOMATION LAUNCHER
echo ========================================
echo.

:: Find Python installation
set PYTHON_CMD=python

:: Check if python command works
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python and add it to your PATH.
    pause
    exit /b 1
)

:: Display Python version
echo [INFO] Python found:
python --version
echo.

:: Find serenum.py
echo [INFO] Searching for serenum.py...

:: Search in current directory and subdirectories
set SCRIPT_FOUND=0
for /r %%i in (serenum.py) do (
    if exist "%%i" (
        set SCRIPT_PATH=%%i
        set SCRIPT_FOUND=1
        echo [SUCCESS] Found: %%i
        goto :found_script
    )
)

:found_script
if %SCRIPT_FOUND% equ 0 (
    echo [ERROR] Could not find serenum.py!
    echo.
    echo Please make sure serenum.py is in the current directory
    echo or one of its subdirectories.
    echo.
    pause
    exit /b 1
)

:: Check if script exists (double-check)
if not exist "%SCRIPT_PATH%" (
    echo [ERROR] Script not found at: %SCRIPT_PATH%
    pause
    exit /b 1
)

:: Display script info
echo.
echo [INFO] Script location: %SCRIPT_PATH%
echo [INFO] Starting execution...
echo.
echo ========================================
echo.

:: Execute the Python script
python "%SCRIPT_PATH%"

:: Check execution result
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo [ERROR] Script exited with error code: %errorlevel%
    echo ========================================
) else (
    echo.
    echo ========================================
    echo [SUCCESS] Script completed successfully!
    echo ========================================
)

echo.
pause