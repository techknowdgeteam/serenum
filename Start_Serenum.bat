@echo off
setlocal
cd /d "%~dp0"

set "PYTHONW=C:\Program Files\Python310\pythonw.exe"
set "PYTHON=C:\Program Files\Python310\python.exe"

if exist "%PYTHONW%" (
    start "" "%PYTHONW%" "%~dp0serenum.py"
    exit /b 0
)

if exist "%PYTHON%" (
    start "" "%PYTHON%" "%~dp0serenum.py"
    exit /b 0
)

where pyw >nul 2>nul
if not errorlevel 1 (
    start "" pyw -3 "%~dp0serenum.py"
    exit /b 0
)

where py >nul 2>nul
if not errorlevel 1 (
    start "" py -3 "%~dp0serenum.py"
    exit /b 0
)

echo Serenum could not find Python 3.10 or the Python Launcher.
echo Install Python 3.10 or update the Python paths in this BAT file.
pause
endlocal
