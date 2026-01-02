@echo off
REM run_server.bat - Start Django dev server and open browser
REM Place this file in the project root and double-click it to run.

REM Change to the directory containing this script
cd /d "%~dp0"

REM If a cmd-style venv activate script exists, use it; otherwise run python directly
if exist ".venv\Scripts\activate.bat" (
    start "Django Server" cmd /k ".venv\Scripts\activate.bat && python manage.py runserver"
) else (
    start "Django Server" cmd /k "python manage.py runserver"
)

REM Wait a few seconds for server to start, then open default browser
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:8000/"

REM Note: If your environment uses PowerShell venv activation, open a PowerShell and run:
REM .\.venv\Scripts\Activate.ps1 & python manage.py runserver
