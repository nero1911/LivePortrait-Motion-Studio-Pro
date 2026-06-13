@echo off
echo Installing LivePortrait Motion Studio Pro...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11+ is not installed or not in PATH
    echo Please install Python 3.11 from https://www.python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To run the application:
echo   1. Run: run.bat
echo.
pause
