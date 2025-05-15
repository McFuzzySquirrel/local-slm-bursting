@echo off
echo ===== Local SLM Bursting Application Launcher =====
echo This script will start both the backend API and the frontend UI.
echo.

REM ===== Check for Python installation =====
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ and try again.
    exit /b 1
)

REM ===== Check if virtual environment exists =====
if not exist ".venv" (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
    echo Installing dependencies...
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Using existing virtual environment (.venv)...
)

REM ===== Activate virtual environment =====
call .venv\Scripts\activate.bat

REM ===== Check if requirements are installed =====
pip show uvicorn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
)

REM ===== Check if .env file exists =====
if not exist ".env" (
    echo WARNING: .env file not found.
    echo Creating .env from .env.example...
    
    if exist ".env.example" (
        copy .env.example .env
        echo Created .env file. Please edit it with your configuration.
        echo Press any key to edit the .env file or Ctrl+C to exit.
        pause >nul
        start notepad .env
    ) else (
        echo ERROR: .env.example file not found.
        echo Please create a .env file with required configuration.
        exit /b 1
    )
)

REM ===== Create directories if they don't exist =====
if not exist "data\uploads" mkdir data\uploads
if not exist "models" mkdir models
if not exist "logs" mkdir logs

REM ===== Check for GGUF model =====
set MODEL_FOUND=0
for %%f in (models\*.gguf) do set MODEL_FOUND=1
if %MODEL_FOUND% EQU 0 (
    echo WARNING: No GGUF model found in the models directory.
    echo Please download a model from Hugging Face and place it in the models folder.
    echo Example models: Phi-2, TinyLlama, Mistral-7B
    echo.
)

REM ===== Start the backend API in a new terminal =====
echo Starting backend API server...
start cmd /k "title Local SLM Backend && color 0A && call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --host localhost --port 8000"

REM ===== Wait for the backend to initialize =====
echo Waiting for backend to initialize (5 seconds)...
timeout /t 5 /nobreak >nul

REM ===== Start the frontend in this terminal =====
echo Starting Streamlit frontend...
echo.
echo NOTE: When finished, close both terminal windows to shut down the application.
echo.
call .venv\Scripts\activate.bat
streamlit run frontend/ui.py