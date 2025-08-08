@echo off
REM Complete Git Installation and Setup for Windows
REM This script handles Git download, installation, and GitHub setup

echo ============================================================
echo POS Automation Framework - Complete Git Setup
echo ============================================================
echo.

REM Check if Git is already installed
git --version >nul 2>&1
if errorlevel 0 (
    echo [SUCCESS] Git is already installed:
    git --version
    goto CONFIGURE_GIT
)

echo [INFO] Git not found, checking if installer is available...

REM Check if Git installer exists
if exist "Git-2.47.1-64-bit.exe" (
    echo [INFO] Git installer found, running installation...
    goto INSTALL_GIT
)

echo [ERROR] Git is not installed and installer not found
echo.
echo Please download Git installer manually:
echo 1. Go to https://git-scm.com/download/windows
echo 2. Download "64-bit Git for Windows Setup"
echo 3. Save it in this directory as "Git-2.47.1-64-bit.exe"
echo 4. Run this script again
echo.
echo OR install Git using chocolatey:
echo choco install git
echo.
echo OR install Git using winget:
echo winget install --id Git.Git -e --source winget
echo.
pause
exit /b 1

:INSTALL_GIT
echo [INFO] Installing Git...
echo Please follow the Git installer prompts:
echo - Use default settings for most options
echo - Make sure "Git from the command line" is selected
echo - Use OpenSSL library
echo - Checkout Windows-style, commit Unix-style endings
start /wait Git-2.47.1-64-bit.exe
echo [INFO] Git installation completed

REM Add Git to PATH for current session
set PATH=%PATH%;C:\Program Files\Git\bin;C:\Program Files\Git\cmd
echo [INFO] Added Git to PATH for current session

REM Verify installation
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git installation failed or not in PATH
    echo Please restart your command prompt and try again
    pause
    exit /b 1
)

echo [SUCCESS] Git installed successfully:
git --version

:CONFIGURE_GIT
echo.
echo ============================================================
echo STEP 2: Git Configuration
echo ============================================================
echo.

REM Check if Git is already configured
for /f "tokens=*" %%i in ('git config --global user.name 2^>nul') do set GIT_NAME=%%i
for /f "tokens=*" %%i in ('git config --global user.email 2^>nul') do set GIT_EMAIL=%%i

if defined GIT_NAME if defined GIT_EMAIL (
    echo [INFO] Git is already configured:
    echo Name: %GIT_NAME%
    echo Email: %GIT_EMAIL%
    
    set /p RECONFIG="Do you want to reconfigure? (y/N): "
    if /i not "%RECONFIG%"=="y" goto SSH_SETUP
)

echo [INFO] Configuring Git user information...
set /p GIT_USERNAME="Enter your name for Git commits: "
set /p GIT_USEREMAIL="Enter your email address: "

git config --global user.name "%GIT_USERNAME%"
git config --global user.email "%GIT_USEREMAIL%"

echo [SUCCESS] Git configured successfully:
echo Name: %GIT_USERNAME%
echo Email: %GIT_USEREMAIL%

:SSH_SETUP
echo.
echo ============================================================
echo STEP 3: SSH Key Setup for GitHub
echo ============================================================
echo.

REM Create .ssh directory if it doesn't exist
if not exist "%USERPROFILE%\.ssh" (
    echo [INFO] Creating SSH directory...
    mkdir "%USERPROFILE%\.ssh"
)

REM Check if SSH key already exists
if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
    echo [INFO] SSH key already exists
    set /p REGENERATE="Do you want to generate a new SSH key? (y/N): "
    if /i not "%REGENERATE%"=="y" goto SHOW_SSH_KEY
)

echo [INFO] Generating SSH key...
ssh-keygen -t rsa -b 4096 -C "%GIT_USEREMAIL%" -f "%USERPROFILE%\.ssh\id_rsa" -N ""

if errorlevel 1 (
    echo [ERROR] Failed to generate SSH key
    echo Please check if ssh-keygen is available
    goto HTTPS_SETUP
)

echo [SUCCESS] SSH key generated successfully

:SHOW_SSH_KEY
echo.
echo [INFO] Your public SSH key (copy this to GitHub):
echo ============================================================
type "%USERPROFILE%\.ssh\id_rsa.pub"
echo ============================================================
echo.
echo [INFO] To add this key to GitHub:
echo 1. Go to https://github.com/settings/keys
echo 2. Click "New SSH key"
echo 3. Paste the key above
echo 4. Give it a title like "Windows PC"
echo 5. Click "Add SSH key"
echo.
pause

goto REPO_SETUP

:HTTPS_SETUP
echo.
echo ============================================================
echo STEP 3: HTTPS Setup (Alternative to SSH)
echo ============================================================
echo.
echo [INFO] Using HTTPS instead of SSH
echo You'll need to use Personal Access Token for authentication
echo.
echo To create a token:
echo 1. Go to https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Select scopes: repo, workflow
echo 4. Copy the token (save it securely)
echo.

:REPO_SETUP
echo.
echo ============================================================
echo STEP 4: Repository Setup
echo ============================================================
echo.

REM Check if we're already in a Git repository
git status >nul 2>&1
if errorlevel 0 (
    echo [INFO] Already in a Git repository
    git remote -v
    goto TEST_CONNECTION
)

echo [INFO] Initializing Git repository...
git init

echo [INFO] Adding files to repository...
git add .

echo [INFO] Creating initial commit...
git commit -m "Initial commit: POS Automation Framework setup"

echo [SUCCESS] Local repository initialized

set /p REPO_URL="Enter your GitHub repository URL (or press Enter to skip): "
if "%REPO_URL%"=="" goto TEST_CONNECTION

echo [INFO] Adding remote repository...
git remote add origin %REPO_URL%

:TEST_CONNECTION
echo.
echo ============================================================
echo STEP 5: Test Connection and Push
echo ============================================================
echo.

echo [INFO] Testing Git connection...

REM Try to push with SSL verification
git push -u origin main 2>git_error.txt
if errorlevel 0 (
    echo [SUCCESS] Successfully pushed to GitHub
    goto CLEANUP
)

echo [WARNING] Push failed, trying with SSL workaround...

REM Try with SSL disabled (for corporate networks)
git config http.sslVerify false
git push -u origin main 2>git_error_ssl.txt
if errorlevel 0 (
    echo [SUCCESS] Successfully pushed to GitHub (SSL disabled)
    git config http.sslVerify true
    echo [INFO] Re-enabled SSL verification
    goto CLEANUP
)

echo [ERROR] Push failed even with SSL workaround
echo [INFO] Error details:
type git_error_ssl.txt 2>nul

echo.
echo [INFO] Manual steps to complete setup:
echo 1. Check your GitHub repository URL
echo 2. Verify your credentials/SSH key
echo 3. Try manual push: git push -u origin main
echo 4. If behind corporate firewall, contact IT support

:CLEANUP
echo.
echo ============================================================
echo Git Setup Completed
echo ============================================================
echo.

REM Clean up error files
del git_error.txt 2>nul
del git_error_ssl.txt 2>nul

echo [INFO] Summary of setup:
git config --global user.name
git config --global user.email
echo.
echo [INFO] Next steps:
echo 1. Configure your POS application path in data/app_settings.csv
echo 2. Run tests: python -m pytest tests/ --verbose
echo 3. Push changes: git add . && git commit -m "message" && git push
echo.
echo [SUCCESS] Git and GitHub setup completed!
pause
