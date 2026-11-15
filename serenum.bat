@echo off
setlocal EnableExtensions
 title Serenum Automation Launcher
cd /d "%~dp0"
set "SCRIPT=%~dp0serenum.py"
if not exist "%SCRIPT%" (
  echo [ERROR] serenum.py was not found in this folder.
  pause
  exit /b 2
)
set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 (
  py -3.12 --version >nul 2>nul && set "PYTHON_CMD=py -3.12"
  if not defined PYTHON_CMD py -3.11 --version >nul 2>nul && set "PYTHON_CMD=py -3.11"
  if not defined PYTHON_CMD py -3.10 --version >nul 2>nul && set "PYTHON_CMD=py -3.10"
)
if not defined PYTHON_CMD (
  echo [ERROR] Python 3.10, 3.11 or 3.12 was not found. Install Python 3.12.
  pause
  exit /b 3
)
%PYTHON_CMD% -X utf8 "%SCRIPT%"
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" echo [ERROR] Serenum exited with code %EXIT_CODE%.
pause
endlocal
