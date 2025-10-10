@echo off
echo ===================================================
echo   PreCog UI - Environment Setup and Launcher
echo ===================================================

if not exist venv (
    echo [INFO] Creating Python Virtual Environment...
    python -m venv venv
)

echo [INFO] Activating Environment...
call venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

echo [INFO] Verifying Dependencies...
:: Installs missing packages without forcing repeated downloads
pip install opencv-python mediapipe==0.10.11 numpy psutil pyautogui

echo [INFO] Setup Complete. Launching PreCog UI...
echo ===================================================
python -m precog_ui.main
pause
