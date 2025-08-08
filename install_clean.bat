@echo off
REM POS Automation Framework - Windows Installer
REM This batch file ensures compatibility with all Windows terminals

echo ============================================================
echo POS Automation Framework - Windows Installation
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found, checking version...
python --version

REM Check if we're in the right directory
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found
    echo Please run this script from the pywinauto project directory
    pause
    exit /b 1
)

echo [INFO] Starting framework installation...

REM Run the clean installer
python install_framework_clean.py

if errorlevel 1 (
    echo.
    echo [ERROR] Installation failed
    echo Check installation.log for details
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Installation completed successfully
echo.
echo Next steps:
echo 1. Run tests: python -m pytest tests/ --verbose
echo 2. Check installation_report.json for details
echo 3. Read README.md for usage instructions
echo.
pause
