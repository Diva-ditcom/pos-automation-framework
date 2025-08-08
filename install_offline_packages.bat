@echo off
echo.
echo ================================================
echo 📦 POS Automation - Offline Package Installation
echo ================================================
echo.

echo 🔧 Installing packages from offline directory...
python install_offline_packages.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Offline installation failed!
    echo 🔧 Try running: python download_offline_packages.py
    pause
    exit /b 1
)

echo.
echo ✅ Offline installation completed!
echo.
echo 📝 Next steps:
echo    1. Run: python setup_new_machine.py
echo    2. Or run: python run_tests.py
echo.
pause
