@echo off
echo Starting local API server...
echo Press Ctrl+C to stop the server
echo.

REM ===== Load Environment Variables from .env =====
if not exist ".env" (
    echo ERROR: .env file not found. Please create it and configure the required environment variables.
    exit /b 1
)
for /f "usebackq tokens=1,2 delims==" %%A in (`type ".env" ^| findstr /r "^[^#]"`) do set %%A=%%B

REM ===== Validate Environment Variables =====
if "%AZURE_OPENAI_API_KEY%"=="" (
    echo ERROR: AZURE_OPENAI_API_KEY is not set. Please configure it in your environment or .env file.
    exit /b 1
)

REM ===== Display Environment Variables =====
echo ===== Environment Variables =====
echo AZURE_OPENAI_API_KEY=%AZURE_OPENAI_API_KEY:~0,5%*** (masked)
echo.

REM ===== Start the Server =====
set PORT=8000
python -m uvicorn app.main:app --reload --host localhost --port %PORT% --timeout-keep-alive 60
if errorlevel 1 (
    echo ERROR: Failed to start the server. Check the logs for details.
    exit /b 1
)