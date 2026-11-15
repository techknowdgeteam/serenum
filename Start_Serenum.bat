@echo off
setlocal EnableExtensions
 title Serenum Startup Diagnostics
cd /d "%~dp0"
set "SCRIPT=%~dp0serenum.py"
if not exist "%SCRIPT%" (
  echo [ERROR] serenum.py was not found beside this launcher.
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
  for %%P in ("C:\Program Files\Python312\python.exe" "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" "C:\Program Files\Python311\python.exe" "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" "C:\Program Files\Python310\python.exe" "%LOCALAPPDATA%\Programs\Python\Python310\python.exe") do (
    if not defined PYTHON_CMD if exist %%~P set "PYTHON_CMD=%%~P"
  )
)
if not defined PYTHON_CMD (
  echo [ERROR] Python 3.10, 3.11 or 3.12 was not found.
  echo [INFO] Install Python 3.12. Python 3.14 does not need to be removed.
  pause
  exit /b 3
)
echo [INFO] Launching with supported Python: %PYTHON_CMD%
if "%PYTHON_CMD:~0,2%"=="py" (
  %PYTHON_CMD% -X utf8 "%SCRIPT%"
) else (
  "%PYTHON_CMD%" -X utf8 "%SCRIPT%"
)
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" echo [ERROR] Serenum exited with code %EXIT_CODE%.
pause
endlocal
