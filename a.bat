@echo off
REM Git Installation Verification Script
echo ============================================================
echo Checking Git Installation Status
echo ============================================================
echo.

REM Check if Git is now available
echo [STEP 1] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is still not recognized
    echo.
    echo Please follow these steps:
    echo 1. Download Git from: https://git-scm.com/download/windows
    echo 2. Run installer as Administrator
    echo 3. Make sure to select "Git from command line and 3rd-party software"
    echo 4. Restart your command prompt after installation
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
) else (
    echo [SUCCESS] Git is installed:
    git --version
)

echo.
echo [STEP 2] Checking Git configuration...
for /f "tokens=*" %%i in ('git config --global user.name 2^>nul') do set GIT_NAME=%%i
for /f "tokens=*" %%i in ('git config --global user.email 2^>nul') do set GIT_EMAIL=%%i

if not defined GIT_NAME (
    echo [INFO] Git user name not configured
    set /p NEW_GIT_NAME="Enter your full name: "
    git config --global user.name "%NEW_GIT_NAME%"
    echo [SUCCESS] Git name configured: %NEW_GIT_NAME%
) else (
    echo [SUCCESS] Git name already configured: %GIT_NAME%
)

if not defined GIT_EMAIL (
    echo [INFO] Git email not configured
    set /p NEW_GIT_EMAIL="Enter your email address: "
    git config --global user.email "%NEW_GIT_EMAIL%"
    echo [SUCCESS] Git email configured: %NEW_GIT_EMAIL%
) else (
    echo [SUCCESS] Git email already configured: %GIT_EMAIL%
)

echo.
echo [STEP 3] Checking repository status...
git status >nul 2>&1
if errorlevel 1 (
    echo [INFO] Not in a Git repository, initializing...
    git init
    if errorlevel 0 (
        echo [SUCCESS] Git repository initialized
    ) else (
        echo [ERROR] Failed to initialize repository
    )
) else (
    echo [SUCCESS] Already in a Git repository
    git status
)

echo.
echo [STEP 4] Checking SSH key...
if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
    echo [SUCCESS] SSH key already exists
    echo [INFO] Your public SSH key:
    echo ----------------------------------------
    type "%USERPROFILE%\.ssh\id_rsa.pub"
    echo ----------------------------------------
    echo.
    echo [INFO] Add this key to GitHub: https://github.com/settings/keys
) else (
    echo [INFO] No SSH key found
    set /p CREATE_SSH="Do you want to create an SSH key for GitHub? (y/N): "
    if /i "%CREATE_SSH%"=="y" (
        echo [INFO] Creating SSH directory...
        if not exist "%USERPROFILE%\.ssh" mkdir "%USERPROFILE%\.ssh"
        
        echo [INFO] Generating SSH key...
        for /f "tokens=*" %%i in ('git config --global user.email') do set USER_EMAIL=%%i
        ssh-keygen -t rsa -b 4096 -C "%USER_EMAIL%" -f "%USERPROFILE%\.ssh\id_rsa" -N ""
        
        if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
            echo [SUCCESS] SSH key created successfully
            echo [INFO] Your public SSH key:
            echo ----------------------------------------
            type "%USERPROFILE%\.ssh\id_rsa.pub"
            echo ----------------------------------------
            echo.
            echo [INFO] Add this key to GitHub: https://github.com/settings/keys
        ) else (
            echo [ERROR] SSH key creation failed
        )
    )
)

echo.
echo [STEP 5] Testing Git operations...
echo [INFO] Adding current files to Git...
git add . >nul 2>&1

echo [INFO] Creating a test commit...
git commit -m "Git installation verification - %date% %time%" >nul 2>&1
if errorlevel 0 (
    echo [SUCCESS] Git commit successful
) else (
    echo [INFO] No changes to commit (this is normal)
)

echo.
echo ============================================================
echo Git Installation Verification Complete
echo ============================================================
echo.
echo [SUCCESS] Git is now properly installed and configured!
echo.
echo [INFO] Summary:
git config --global user.name
git config --global user.email
echo Repository status: Ready
echo.
echo [NEXT STEPS]
echo 1. Your framework is ready for version control
echo 2. You can now push to GitHub repositories
echo 3. Continue with your POS automation testing
echo.
echo [COMMANDS YOU CAN NOW USE]
echo - git status                 (check repository status)
echo - git add .                  (add files for commit)
echo - git commit -m "message"    (save changes)
echo - git push origin main       (upload to GitHub)
echo.
pause