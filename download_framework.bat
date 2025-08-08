@echo off
REM Automated Framework Downloader
REM This script automatically downloads the POS automation framework

echo ============================================================
echo POS Automation Framework - Automated Downloader
echo ============================================================
echo.

REM Check if we're already in the framework directory
if exist "install_clean.bat" if exist "requirements.txt" if exist "tests" (
    echo [INFO] Framework already exists in current directory
    echo [SUCCESS] Framework is ready to use
    goto END_SUCCESS
)

REM Check if Git is available for cloning
git --version >nul 2>&1
if errorlevel 0 (
    echo [INFO] Git found, using git clone method
    goto GIT_CLONE
) else (
    echo [INFO] Git not found, using download method
    goto DOWNLOAD_METHOD
)

:GIT_CLONE
echo [INFO] Cloning framework from GitHub...
set REPO_URL=https://github.com/Diva-ditcom/pos-automation-framework.git

REM Try to clone the repository
git clone %REPO_URL% pos-automation-framework
if errorlevel 0 (
    echo [SUCCESS] Framework cloned successfully
    cd pos-automation-framework
    goto VERIFY_DOWNLOAD
) else (
    echo [WARNING] Git clone failed, trying download method...
    goto DOWNLOAD_METHOD
)

:DOWNLOAD_METHOD
echo [INFO] Downloading framework as ZIP file...

REM Try using PowerShell to download
powershell -Command "& {try { Invoke-WebRequest -Uri 'https://github.com/Diva-ditcom/pos-automation-framework/archive/refs/heads/main.zip' -OutFile 'framework.zip'; Write-Host '[SUCCESS] Download completed' } catch { Write-Host '[ERROR] Download failed:' $_.Exception.Message; exit 1 }}"

if errorlevel 1 (
    echo [ERROR] Automated download failed
    goto MANUAL_INSTRUCTIONS
)

echo [INFO] Extracting framework...
powershell -Command "& {try { Expand-Archive -Path 'framework.zip' -DestinationPath '.'; Move-Item 'pos-automation-framework-main' 'pos-automation-framework'; Remove-Item 'framework.zip'; Write-Host '[SUCCESS] Extraction completed' } catch { Write-Host '[ERROR] Extraction failed:' $_.Exception.Message; exit 1 }}"

if errorlevel 1 (
    echo [ERROR] Extraction failed
    goto MANUAL_INSTRUCTIONS
)

cd pos-automation-framework
goto VERIFY_DOWNLOAD

:VERIFY_DOWNLOAD
echo [INFO] Verifying framework download...

REM Check for key files
if not exist "install_clean.bat" (
    echo [ERROR] install_clean.bat not found
    goto DOWNLOAD_FAILED
)

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found
    goto DOWNLOAD_FAILED
)

if not exist "tests" (
    echo [ERROR] tests directory not found
    goto DOWNLOAD_FAILED
)

if not exist "config" (
    echo [ERROR] config directory not found
    goto DOWNLOAD_FAILED
)

echo [SUCCESS] Framework verification completed
echo [INFO] Framework downloaded to: %CD%

:END_SUCCESS
echo.
echo ============================================================
echo Framework Download Completed Successfully
echo ============================================================
echo.
echo [INFO] Framework is ready in: %CD%
echo.
echo [INFO] Next steps:
echo 1. Run: install_clean.bat
echo 2. Run: install_git_complete.bat (if Git setup needed)
echo 3. Configure: data/app_settings.csv
echo 4. Test: python test_pos_connection.py
echo.
echo [SUCCESS] Ready to proceed with installation!
pause
exit /b 0

:DOWNLOAD_FAILED
echo [ERROR] Framework download/verification failed
goto MANUAL_INSTRUCTIONS

:MANUAL_INSTRUCTIONS
echo.
echo ============================================================
echo Manual Download Instructions
echo ============================================================
echo.
echo Automated download failed. Please download manually:
echo.
echo Option 1: Using Git (if available)
echo   git clone https://github.com/Diva-ditcom/pos-automation-framework.git
echo   cd pos-automation-framework
echo.
echo Option 2: Download ZIP file
echo   1. Go to: https://github.com/Diva-ditcom/pos-automation-framework
echo   2. Click "Code" button
echo   3. Click "Download ZIP"
echo   4. Extract the ZIP file
echo   5. Navigate to the extracted folder
echo.
echo Option 3: Use provided USB/network drive
echo   Copy the framework folder from your source location
echo.
echo After manual download, run this script again to verify
echo.
pause
exit /b 1
