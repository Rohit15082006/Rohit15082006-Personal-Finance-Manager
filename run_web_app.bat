@echo off
REM Personal Finance Manager - Web Version Launcher
REM This script installs dependencies and starts the Flask app

echo.
echo ============================================
echo  Personal Finance Manager - Web Version
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking Python installation... OK
echo.

REM Install dependencies
echo [2/3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/3] Dependencies installed... OK
echo.

REM Start the Flask app
echo [3/3] Starting Finance Manager Web App...
echo.
echo ============================================
echo  Opening at http://localhost:5000
echo ============================================
echo.
echo NOTE: Keep this window open while using the app
echo Press CTRL+C to stop the server
echo.

python app.py
pause
