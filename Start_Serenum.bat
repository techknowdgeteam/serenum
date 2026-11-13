@echo off
setlocal EnableExtensions
 title Serenum Startup
cd /d "%~dp0"

 echo.
 echo ============================================================
 echo   SERENUM - STARTUP DIAGNOSTICS
 echo ============================================================
 echo.

set "SCRIPT=%~dp0serenum.py"
set "PYTHON310=C:\Program Files\Python310\python.exe"

if not exist "%SCRIPT%" (
    echo [ERROR] serenum.py was not found beside this launcher.
    echo [INFO] Extract the COMPLETE ZIP into your Serenum folder.
    echo.
    pause
    exit /b 2
)

if exist "%PYTHON310%" (
    set "PYTHON_CMD=%PYTHON310%"
    goto :run
)

where py >nul 2>nul
if not errorlevel 1 (
    py -3.10 --version >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=py -3.10"
        goto :run
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python --version
    set "PYTHON_CMD=python"
    goto :run
)

echo [ERROR] Python was not found.
echo [INFO] Install Python 3.10 or update the Python path in this BAT file.
echo.
pause
exit /b 3

:run
echo [INFO] Launching Serenum with visible startup diagnostics.
echo [INFO] If startup fails, the Python error will appear below.
echo [INFO] Close the Serenum window to return here.
echo.

if "%PYTHON_CMD%"=="py -3.10" (
    py -3.10 -X utf8 "%SCRIPT%"
) else (
    "%PYTHON_CMD%" -X utf8 "%SCRIPT%"
)
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%EXIT_CODE%"=="0" (
    echo [ERROR] Serenum exited with code %EXIT_CODE%.
    echo [INFO] Copy the complete error shown above when requesting support.
) else (
    echo [SUCCESS] Serenum closed normally.
)
echo.
pause
endlocal
