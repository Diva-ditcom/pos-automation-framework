@echo off
REM Complete Automated POS Framework Setup
REM This script automates the entire setup process from scratch

echo ============================================================
echo POS Automation Framework - Complete Automated Setup
echo ============================================================
echo.
echo This script will automatically:
echo [1] Download the framework (if needed)
echo [2] Install Python packages
echo [3] Setup Git and GitHub
echo [4] Prepare for configuration
echo.
pause

REM Step 1: Check Python
echo ============================================================
echo STEP 1: Checking Python Installation
echo ============================================================
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [SUCCESS] Python found:
python --version

REM Step 2: Download Framework (if not already present)
echo.
echo ============================================================
echo STEP 2: Framework Download
echo ============================================================

if exist "install_clean.bat" if exist "requirements.txt" (
    echo [SUCCESS] Framework already present in current directory
    goto STEP3
)

echo [INFO] Framework not found, downloading...

REM Try Git clone first
git --version >nul 2>&1
if errorlevel 0 (
    echo [INFO] Using Git to clone framework...
    git clone https://github.com/Diva-ditcom/pos-automation-framework.git temp_framework
    if errorlevel 0 (
        echo [SUCCESS] Framework cloned successfully
        xcopy temp_framework\* . /E /H /Y
        rmdir temp_framework /S /Q
        goto STEP3
    )
)

REM Try PowerShell download
echo [INFO] Using PowerShell to download framework...
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/Diva-ditcom/pos-automation-framework/archive/refs/heads/main.zip' -OutFile 'framework.zip' } catch { exit 1 }"
if errorlevel 0 (
    powershell -Command "try { Expand-Archive -Path 'framework.zip' -DestinationPath 'temp'; Move-Item 'temp/pos-automation-framework-main/*' '.'; Remove-Item 'temp' -Recurse; Remove-Item 'framework.zip' } catch { exit 1 }"
    if errorlevel 0 (
        echo [SUCCESS] Framework downloaded and extracted
        goto STEP3
    )
)

echo [ERROR] Automated download failed
echo Please download framework manually and run this script again
pause
exit /b 1

:STEP3
REM Step 3: Install Framework
echo.
echo ============================================================
echo STEP 3: Installing Framework Packages
echo ============================================================

if exist "install_clean.bat" (
    echo [INFO] Running framework installer...
    call install_clean.bat
    if errorlevel 1 (
        echo [ERROR] Framework installation failed
        pause
        exit /b 1
    )
) else (
    echo [ERROR] install_clean.bat not found
    exit /b 1
)

REM Step 4: Git Setup
echo.
echo ============================================================
echo STEP 4: Git and GitHub Setup
echo ============================================================

git --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Git not found, installing Git...
    if exist "install_git_auto.bat" (
        call install_git_auto.bat
        echo [INFO] Please restart this script after Git installation
        pause
        exit /b 0
    ) else (
        echo [ERROR] Git installer not found
        echo Please install Git manually from: https://git-scm.com
        pause
        exit /b 1
    )
)

echo [SUCCESS] Git is available:
git --version

REM Configure Git if needed
for /f "tokens=*" %%i in ('git config --global user.name 2^>nul') do set GIT_NAME=%%i
if not defined GIT_NAME (
    echo [INFO] Configuring Git...
    if exist "install_git_complete.bat" (
        call install_git_complete.bat
    ) else (
        echo [WARNING] Git setup script not found, configure manually
    )
)

REM Step 5: Verification
echo.
echo ============================================================
echo STEP 5: Installation Verification
echo ============================================================

echo [INFO] Verifying Python packages...
python -c "import pytest, pywinauto, pandas, openpyxl; print('[SUCCESS] All packages installed')" 2>nul
if errorlevel 1 (
    echo [ERROR] Some packages missing, try running install_clean.bat again
)

echo [INFO] Verifying framework...
python -c "from utils.pos_base import POSAutomation; print('[SUCCESS] Framework loads correctly')" 2>nul
if errorlevel 1 (
    echo [ERROR] Framework has issues, check configuration
)

echo [INFO] Verifying Git...
git status >nul 2>&1
if errorlevel 0 (
    echo [SUCCESS] Git repository initialized
) else (
    echo [WARNING] Git repository not initialized
)

REM Step 6: Next Steps
echo.
echo ============================================================
echo SETUP COMPLETED - Next Steps
echo ============================================================
echo.
echo [SUCCESS] Automated setup completed successfully!
echo.
echo [INFO] Manual configuration required:
echo.
echo 1. Configure POS Application:
echo    - Edit: data/app_settings.csv
echo    - Set your POS application path
echo    - Update window titles and settings
echo.
echo 2. Configure Test Data:
echo    - Edit: data/test_scenarios.csv
echo    - Update item codes, prices, customer data
echo.
echo 3. Test POS Connection:
echo    - Run: python test_pos_connection.py
echo.
echo 4. Run Tests:
echo    - Run: python -m pytest tests/ --verbose
echo.
echo 5. Commit Your Configuration:
echo    - Run: git add .
echo    - Run: git commit -m "Configure POS settings"
echo    - Run: git push origin main
echo.
echo ============================================================
echo Ready for POS Automation Testing!
echo ============================================================
echo.

REM Open configuration files for editing
set /p OPEN_CONFIG="Do you want to open configuration files now? (y/N): "
if /i "%OPEN_CONFIG%"=="y" (
    echo [INFO] Opening configuration files...
    if exist "data\app_settings.csv" start notepad "data\app_settings.csv"
    if exist "data\test_scenarios.csv" start notepad "data\test_scenarios.csv"
)

echo [INFO] Setup script completed
pause
