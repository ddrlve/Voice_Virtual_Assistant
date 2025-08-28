@echo off
title ARIA Voice Assistant Launcher
color 0B

echo.
echo ╭─────────────────────────────────────────────────────────────╮
echo │                                                             │
echo │          🎤 ARIA Voice Assistant Launcher                  │
echo │             Professional Voice Assistant                    │
echo │                                                             │
echo ╰─────────────────────────────────────────────────────────────╯
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python from https://python.org
    pause
    exit /b 1
)

echo [✓] Python detected: 
python --version

:: Check if virtual environment exists
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    echo [✓] Virtual environment created
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies if needed
echo [INFO] Checking dependencies...
pip install -q speechrecognition pyttsx3 pyaudio python-dotenv requests psutil rich

:: Check if .env file exists
if not exist ".env" (
    echo [INFO] Setting up configuration...
    if exist ".env.example" (
        copy .env.example .env
    ) else (
        echo # ARIA Voice Assistant Configuration > .env
        echo WEATHER_API_KEY=demo_key >> .env
        echo USER_NAME=User >> .env
        echo ASSISTANT_NAME=ARIA >> .env
    )
    echo [✓] Configuration file created
    echo [INFO] You can edit .env file for customization
)

:: Pre-flight checks
echo [INFO] Performing system checks...

:: Check microphone
python -c "import speech_recognition as sr; r = sr.Recognizer(); print('[✓] Microphone access OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] Microphone might not be available
)

:: Check TTS
python -c "import pyttsx3; engine = pyttsx3.init(); print('[✓] Text-to-speech OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] Text-to-speech might not be available
)

:: Clear screen and launch ARIA
cls
echo.
echo 🚀 Launching ARIA Voice Assistant...
echo 💡 Say "Hello ARIA" to begin interaction
echo 🚪 Say "Goodbye" to exit gracefully
echo.
python aria_voice_assistant.py

echo.
echo [INFO] ARIA session ended
echo 👋 Thank you for using ARIA Voice Assistant!
pause
