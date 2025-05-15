@echo off
echo ===== Local SLM Bursting Quick Start =====
echo This script will start both the backend API and the frontend UI using the existing virtual environment.
echo.

REM ===== Check if virtual environment exists =====
if not exist ".venv" (
    echo ERROR: Virtual environment not found.
    echo Please run run_app.bat first to set up the environment.
    exit /b 1
)

REM ===== Activate virtual environment =====
call .venv\Scripts\activate.bat

REM ===== Check if .env file exists =====
if not exist ".env" (
    echo ERROR: .env file not found.
    echo Please run run_app.bat first to set up the configuration.
    exit /b 1
)

REM ===== Start the backend API in a new terminal =====
echo Starting backend API server...
start cmd /k "title Local SLM Backend && color 0A && call .venv\Scripts\activate.bat && run_local_api.bat"

REM ===== Wait for the backend to initialize =====
echo Waiting for backend to initialize (5 seconds)...
timeout /t 5 /nobreak >nul

REM ===== Start the frontend in this terminal =====
echo Starting Streamlit frontend...
echo.
echo NOTE: When finished, close both terminal windows to shut down the application.
echo.
call run_streamlit.bat
