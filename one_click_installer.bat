@echo off
REM One-Click POS Framework Installer
REM Run this on any fresh Windows machine to get everything setup

title POS Automation Framework - One-Click Installer

echo.
echo  ██████╗  ██████╗ ███████╗    ███████╗██████╗  █████╗ ███╗   ███╗███████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗
echo  ██╔══██╗██╔═══██╗██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝
echo  ██████╔╝██║   ██║███████╗    █████╗  ██████╔╝███████║██╔████╔██║█████╗  ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ 
echo  ██╔═══╝ ██║   ██║╚════██║    ██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ██║███╗██║██║   ██║██╔══██╗██╔═██╗ 
echo  ██║     ╚██████╔╝███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗
echo  ╚═╝      ╚═════╝ ╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo                               AUTOMATED INSTALLATION SYSTEM
echo.
echo =====================================================================================================
echo.
echo  This installer will automatically set up everything you need for POS automation testing:
echo.
echo  [✓] Download framework from GitHub
echo  [✓] Install Python packages (pytest, pywinauto, pandas, etc.)
echo  [✓] Setup Git and GitHub integration
echo  [✓] Configure development environment
echo  [✓] Prepare test framework
echo.
echo  Requirements: Windows 10+, Python 3.7+
echo  Time: ~5-10 minutes (depending on internet speed)
echo.
echo =====================================================================================================
echo.

set /p PROCEED="Ready to start automated installation? (Y/n): "
if /i "%PROCEED%"=="n" exit /b 0

echo.
echo [INFO] Starting automated installation...
echo [INFO] This may take several minutes, please be patient...
echo.

REM Create installation log
set LOG_FILE=installation_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.log
echo Installation started at %date% %time% > "%LOG_FILE%"

REM Check if we need to download the framework
if not exist "setup_complete_automated.bat" (
    echo [STEP 1/4] Downloading framework...
    
    REM Try multiple download methods
    curl --version >nul 2>&1
    if errorlevel 0 (
        curl -L -o framework.zip "https://github.com/Diva-ditcom/pos-automation-framework/archive/refs/heads/main.zip"
    ) else (
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Diva-ditcom/pos-automation-framework/archive/refs/heads/main.zip' -OutFile 'framework.zip'"
    )
    
    if exist "framework.zip" (
        powershell -Command "Expand-Archive -Path 'framework.zip' -DestinationPath '.'"
        move "pos-automation-framework-main\*" . >nul 2>&1
        rmdir "pos-automation-framework-main" /S /Q >nul 2>&1
        del "framework.zip" >nul 2>&1
        echo [SUCCESS] Framework downloaded
    ) else (
        echo [ERROR] Download failed - please check internet connection
        echo See manual instructions at: https://github.com/Diva-ditcom/pos-automation-framework
        pause
        exit /b 1
    )
) else (
    echo [INFO] Framework already present
)

REM Run the complete automated setup
if exist "setup_complete_automated.bat" (
    echo [STEP 2/4] Running automated setup...
    call setup_complete_automated.bat
) else (
    echo [ERROR] Setup script not found
    exit /b 1
)

echo.
echo =====================================================================================================
echo                                 INSTALLATION COMPLETED!
echo =====================================================================================================
echo.
echo [SUCCESS] POS Automation Framework is now ready!
echo.
echo [INFO] Installation log saved to: %LOG_FILE%
echo.
echo [NEXT STEPS]
echo 1. Configure your POS application in: data\app_settings.csv
echo 2. Update test data in: data\test_scenarios.csv  
echo 3. Test connection: python test_pos_connection.py
echo 4. Run tests: python -m pytest tests\ --verbose
echo.
echo [QUICK START]
echo - Framework location: %CD%
echo - Documentation: README.md
echo - Configuration: data\app_settings.csv
echo - Tests: tests\pos_automation\
echo.
echo Happy testing! 🎉
echo.
pause
