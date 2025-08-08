@echo off
echo.
echo ================================================
echo 🚀 POS Automation Framework Setup
echo ================================================
echo.

echo 📋 Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! 
    echo Please install Python 3.8+ from https://python.org
    echo Then run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Python found
    python --version
)

echo.
echo 📦 Step 2: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
)

echo.
echo 🧪 Step 3: Testing framework components...

echo    Testing CSV Manager...
python -c "from data.csv_data_manager import csv_data_manager; print('   ✅ CSV Manager loaded')" 2>nul
if %errorlevel% neq 0 (
    echo    ❌ CSV Manager failed to load
    goto :error
)

echo    Testing Configuration...
python -c "from config.config import Config; print('   ✅ Config loaded')" 2>nul
if %errorlevel% neq 0 (
    echo    ❌ Configuration failed to load
    goto :error
)

echo    Testing POS Automation...
python -c "from utils.pos_base import POSAutomation; print('   ✅ POS Automation loaded')" 2>nul
if %errorlevel% neq 0 (
    echo    ❌ POS Automation failed to load
    goto :error
)

echo.
echo 🎯 Step 4: Testing pytest discovery...
python -m pytest --collect-only >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pytest test discovery failed
    goto :error
) else (
    echo ✅ Pytest can discover all tests
)

echo.
echo 📊 Step 5: Testing CSV data loading...
python -c "from data.csv_data_manager import csv_data_manager; scenarios = csv_data_manager.list_available_scenarios(); print(f'   ✅ Found {len(scenarios)} test scenarios'); settings = csv_data_manager.load_settings(); print(f'   ✅ Loaded {len(settings)} application settings')"

echo.
echo ================================================
echo ✅ Framework setup completed successfully!
echo ================================================
echo.
echo 📝 Next steps:
echo    1. Update data\app_settings.csv with your POS application path
echo    2. Update data\test_scenarios.csv with your test data  
echo    3. Run tests: python run_tests.py
echo    4. Manage data: python manage_csv_data.py
echo.
echo 🎯 Quick test: python run_tests.py
echo 📊 View data: python manage_csv_data.py
echo.
pause
goto :end

:error
echo.
echo ❌ Setup failed! Please check the error messages above.
echo.
echo 🔧 Troubleshooting tips:
echo    - Ensure you're running from the correct directory
echo    - Check if all files are present in the framework folder
echo    - Try running: pip install --upgrade -r requirements.txt
echo.
pause

:end
