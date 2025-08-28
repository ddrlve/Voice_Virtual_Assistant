@echo off
title ARIA Voice Assistant Launcher
color 0B

echo.
echo ============================================
echo    🎙️  ARIA Voice Assistant Launcher
echo ============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies if needed
echo 📋 Checking dependencies...
pip install -q speechrecognition pyttsx3 pyaudio python-dotenv requests psutil

:: Check if .env file exists
if not exist ".env" (
    echo ⚙️  Setting up configuration...
    copy .env.example .env
    echo.
    echo 📝 Please edit .env file with your API keys if needed
    echo 💡 You can use ARIA without API keys for basic features
    echo.
    pause
)

:: Clear screen and launch ARIA
cls
echo.
echo 🚀 Launching ARIA Voice Assistant...
echo.
python aria_voice_assistant.py

echo.
echo 👋 ARIA session ended
pause
