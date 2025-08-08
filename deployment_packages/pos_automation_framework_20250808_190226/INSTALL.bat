@echo off
REM One-Click POS Automation Framework Installer
echo ========================================
echo POS Automation Framework - One Click Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 💡 Download from: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run enhanced setup
echo 🚀 Starting framework installation...
python setup_new_machine_enhanced.py

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    pause
    exit /b 1
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo 📋 Next steps:
echo   1. Run: python run_all_diagnostics.py
echo   2. Open VS Code workspace: pos-automation.code-workspace
echo   3. Deploy to GitHub: python deploy_to_github.py
echo.
pause
