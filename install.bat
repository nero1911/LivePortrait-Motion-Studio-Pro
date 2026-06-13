@echo off
echo Installing LivePortrait Motion Studio Pro...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11 is not installed or not in PATH
    echo Please install Python 3.11 from https://www.python.org
    pause
    exit /b 1
)

echo Detected Python version:
python --version
echo.

REM Check for Python 3.11
echo Creating virtual environment with Python 3.11...
py -3.11 -m venv venv >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11 not found
    echo Available versions:
    py --list
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

echo Installing PyTorch (CUDA)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo Installing other dependencies...
pip install -r requirements.txt

echo.
echo Downloading LivePortrait models (this may take 5-10 minutes)...
python download_models.py

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo To run the application:
echo   1. Run: run.bat
echo   2. Or: python main.py
echo.
pause
