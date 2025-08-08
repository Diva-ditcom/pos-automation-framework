@echo off
REM Quick Git Installer using Windows Package Managers
echo ============================================================
echo Installing Git using Windows Package Managers
echo ============================================================

REM Try winget first (Windows 10+)
echo [INFO] Trying to install Git using winget...
winget install --id Git.Git -e --source winget --silent
if errorlevel 0 (
    echo [SUCCESS] Git installed via winget
    goto REFRESH_PATH
)

REM Try chocolatey if available
echo [INFO] Trying to install Git using chocolatey...
choco install git -y
if errorlevel 0 (
    echo [SUCCESS] Git installed via chocolatey
    goto REFRESH_PATH
)

REM Manual download option
echo [ERROR] Package managers not available
echo.
echo Please install Git manually:
echo 1. Download from: https://git-scm.com/download/windows
echo 2. Run the installer with default settings
echo 3. Restart your command prompt
echo 4. Run this script again
echo.
pause
exit /b 1

:REFRESH_PATH
echo [INFO] Refreshing PATH environment variable...
REM Add common Git paths
set PATH=%PATH%;C:\Program Files\Git\bin;C:\Program Files\Git\cmd
refreshenv

REM Test Git installation
echo [INFO] Testing Git installation...
git --version
if errorlevel 0 (
    echo [SUCCESS] Git is now available
) else (
    echo [WARNING] Git may need PATH refresh - restart command prompt
)

echo.
echo [SUCCESS] Git installation completed
echo Please restart your command prompt and run: install_git_complete.bat
pause
