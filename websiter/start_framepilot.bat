@echo off
setlocal enabledelayedexpansion

REM FramePilot Windows launcher
set ROOT=%~dp0
cd /d "%ROOT%"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on PATH.
  echo Install Python 3.11+ from https://www.python.org/downloads/windows/
  echo Then reopen this launcher.
  pause
  exit /b 1
)

if not exist ".venv" (
  echo Creating a local virtual environment...
  python -m venv .venv
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if not exist "data" mkdir data
if not exist "uploads" mkdir uploads

if not exist ".env" (
  copy .env.example .env
  echo Created .env from .env.example.
  echo IMPORTANT: open .env and add your GEMINI_API_KEY before testing live AI.
)

echo.
echo Starting FramePilot backend on http://localhost:8000
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
