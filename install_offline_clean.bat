@echo off
REM Offline Package Installer for POS Automation Framework
REM This script installs packages from the offline_packages directory

echo ============================================================
echo POS Automation Framework - Offline Installation
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

echo [INFO] Python found:
python --version
echo.

REM Check if offline packages directory exists
if not exist "offline_packages" (
    echo [ERROR] offline_packages directory not found
    echo Please ensure you have downloaded the offline packages first
    echo Run: python prepare_offline_packages.py
    pause
    exit /b 1
)

REM Check if there are any package files
dir /b "offline_packages\*.whl" >nul 2>&1
set WHEEL_EXISTS=%errorlevel%

dir /b "offline_packages\*.tar.gz" >nul 2>&1
set TAR_EXISTS=%errorlevel%

if %WHEEL_EXISTS% neq 0 if %TAR_EXISTS% neq 0 (
    echo [ERROR] No package files found in offline_packages directory
    echo Please download packages first using prepare_offline_packages.py
    pause
    exit /b 1
)

echo [INFO] Found offline packages, starting installation...
echo.

REM Upgrade pip first (offline)
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install packages from offline directory
echo [INFO] Installing packages from offline directory...
python -m pip install --no-index --find-links offline_packages --force-reinstall offline_packages/*.whl

if errorlevel 1 (
    echo.
    echo [WARNING] Wheel installation had issues, trying with all files...
    python -m pip install --no-index --find-links offline_packages pytest pywinauto pandas openpyxl
)

if errorlevel 1 (
    echo.
    echo [ERROR] Offline installation failed
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Offline installation completed
echo.

REM Verify installation
echo [INFO] Verifying installation...
python -c "import pytest; print('pytest: OK')" 2>nul
if errorlevel 1 echo [WARNING] pytest not properly installed

python -c "import pywinauto; print('pywinauto: OK')" 2>nul
if errorlevel 1 echo [WARNING] pywinauto not properly installed

python -c "import pandas; print('pandas: OK')" 2>nul
if errorlevel 1 echo [WARNING] pandas not properly installed

python -c "import openpyxl; print('openpyxl: OK')" 2>nul
if errorlevel 1 echo [WARNING] openpyxl not properly installed

echo.
echo Installation verification completed
echo.
echo Next steps:
echo 1. Run tests: python -m pytest tests/ --verbose
echo 2. Check the main README.md for usage instructions
echo 3. Review config/config.py for application settings
echo.
pause
