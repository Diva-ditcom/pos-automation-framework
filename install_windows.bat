@echo off
REM POS Automation Framework - Windows Installer
REM ============================================
REM This batch file installs the POS automation framework
REM Compatible with all Windows systems

echo ============================================
echo POS AUTOMATION FRAMEWORK INSTALLER
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found, checking version...
python -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.7+ required
    pause
    exit /b 1
)

echo [OK] Python version compatible
echo.

REM Try simple installer first
echo [INFO] Starting package installation...
python simple_installer.py

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo INSTALLATION COMPLETED SUCCESSFULLY!
    echo ============================================
    echo.
    echo Next steps:
    echo 1. Run: python -m pytest tests/ -v
    echo 2. Check reports in reports/ directory
    echo 3. Configure your POS app in config/
    echo.
) else (
    echo.
    echo [WARNING] Simple installer failed, trying manual installation...
    echo.
    
    REM Manual package installation
    echo [INFO] Installing packages manually...
    python -m pip install --upgrade pip
    python -m pip install pywinauto>=0.6.9
    python -m pip install pytest>=7.0.0
    python -m pip install pytest-html>=3.1.0
    python -m pip install selenium>=4.0.0
    python -m pip install pandas>=1.3.0
    python -m pip install openpyxl>=3.0.0
    
    echo.
    echo [INFO] Testing package imports...
    python -c "import pywinauto; print('[OK] pywinauto available')" 2>nul || echo "[WARNING] pywinauto import failed"
    python -c "import pytest; print('[OK] pytest available')" 2>nul || echo "[WARNING] pytest import failed"
    
    echo.
    echo ============================================
    echo MANUAL INSTALLATION COMPLETED
    echo ============================================
)

echo.
echo To test the framework:
echo   python -m pytest tests/ -v
echo.
echo For help, see README.md and EXECUTION_GUIDE.md
echo.
pause
