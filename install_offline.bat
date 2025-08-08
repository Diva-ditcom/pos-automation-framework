@echo off
REM OFFLINE PACKAGE INSTALLER FOR WINDOWS
REM =====================================
REM This script installs Python packages from offline wheel files
REM Use this when there's no internet connection available

echo ============================================
echo OFFLINE PACKAGE INSTALLER
echo ============================================
echo.

REM Check if offline_packages directory exists
if not exist "offline_packages" (
    echo [ERROR] offline_packages directory not found
    echo.
    echo This means you need to download packages first.
    echo On a machine with internet, run:
    echo   python download_offline_packages.py
    echo.
    echo Then copy the entire folder to this machine.
    pause
    exit /b 1
)

REM Check if there are any package files
dir /b offline_packages\*.whl >nul 2>&1
if %errorlevel% neq 0 (
    dir /b offline_packages\*.tar.gz >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] No package files found in offline_packages
        echo.
        echo Download packages first on a machine with internet:
        echo   python download_offline_packages.py
        echo.
        pause
        exit /b 1
    )
)

echo [INFO] Found offline packages directory
echo [INFO] Installing packages from offline cache...
echo.

REM Install packages from offline directory
echo [INFO] Installing core packages...
python -m pip install --no-index --find-links offline_packages pywinauto

if %errorlevel% equ 0 (
    echo [OK] pywinauto installed
) else (
    echo [WARNING] pywinauto installation had issues
)

python -m pip install --no-index --find-links offline_packages pytest

if %errorlevel% equ 0 (
    echo [OK] pytest installed
) else (
    echo [WARNING] pytest installation had issues
)

python -m pip install --no-index --find-links offline_packages pytest-html

if %errorlevel% equ 0 (
    echo [OK] pytest-html installed
) else (
    echo [WARNING] pytest-html installation had issues
)

python -m pip install --no-index --find-links offline_packages selenium

if %errorlevel% equ 0 (
    echo [OK] selenium installed
) else (
    echo [WARNING] selenium installation had issues
)

python -m pip install --no-index --find-links offline_packages pandas

if %errorlevel% equ 0 (
    echo [OK] pandas installed
) else (
    echo [WARNING] pandas installation had issues
)

python -m pip install --no-index --find-links offline_packages openpyxl

if %errorlevel% equ 0 (
    echo [OK] openpyxl installed
) else (
    echo [WARNING] openpyxl installation had issues
)

echo.
echo ============================================
echo INSTALLATION COMPLETED
echo ============================================
echo.

echo [INFO] Testing package imports...
python -c "import pywinauto; print('[OK] pywinauto available')" 2>nul || echo "[WARNING] pywinauto import failed"
python -c "import pytest; print('[OK] pytest available')" 2>nul || echo "[WARNING] pytest import failed"

echo.
echo To test the framework:
echo   python -m pytest tests/ -v
echo.
echo If packages are missing, try:
echo   python -m pip install --no-index --find-links offline_packages -r requirements.txt
echo.
pause
