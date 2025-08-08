@echo off
REM GitHub Authentication and Push Helper
REM Fixes common authentication issues

echo ============================================================
echo GitHub Authentication Setup
echo ============================================================
echo.

echo [INFO] Current Git configuration:
git config --list | findstr "user\|remote"
echo.

echo [INFO] Fixing common SSL and authentication issues...

REM Fix SSL certificate issues
git config --global http.sslVerify false
echo [SUCCESS] SSL verification disabled for Git

REM Set up credential manager
git config --global credential.helper manager-core
echo [SUCCESS] Credential manager configured

REM Update remote URL to use token authentication
echo.
echo [INFO] Your current remote:
git remote -v
echo.

echo GitHub Authentication Options:
echo 1. Use Personal Access Token (Recommended)
echo 2. Use SSH authentication 
echo 3. Use GitHub CLI
echo 4. Fix current HTTPS authentication
echo.

set /p AUTH_OPTION="Choose authentication method (1-4): "

if "%AUTH_OPTION%"=="1" goto :use_token
if "%AUTH_OPTION%"=="2" goto :use_ssh
if "%AUTH_OPTION%"=="3" goto :use_gh_cli
if "%AUTH_OPTION%"=="4" goto :fix_https
goto :use_token

:use_token
echo.
echo ============================================================
echo Personal Access Token Setup
echo ============================================================
echo.
echo Steps to create a Personal Access Token:
echo 1. Go to GitHub.com ^> Settings ^> Developer settings ^> Personal access tokens
echo 2. Click "Generate new token (classic)"
echo 3. Set expiration (recommended: 90 days)
echo 4. Select scopes: repo, workflow, write:packages
echo 5. Click "Generate token"
echo 6. Copy the token (you won't see it again!)
echo.

echo Opening GitHub token creation page...
start "" "https://github.com/settings/tokens"
echo.

set /p GITHUB_TOKEN="Paste your GitHub token here: "

if "%GITHUB_TOKEN%"=="" (
    echo [ERROR] No token provided
    pause
    exit /b 1
)

REM Update remote URL with token
for /f "tokens=2" %%i in ('git remote get-url origin') do set REPO_URL=%%i
echo %REPO_URL% | findstr "github.com" >nul
if errorlevel 1 (
    echo [ERROR] Not a GitHub repository
    pause
    exit /b 1
)

REM Extract repository path
for /f "tokens=2 delims=/" %%i in ("%REPO_URL%") do set GITHUB_USER=%%i
for /f "tokens=3 delims=/" %%i in ("%REPO_URL%") do set REPO_NAME=%%i

set NEW_URL=https://%GITHUB_TOKEN%@github.com/%GITHUB_USER%/%REPO_NAME%

git remote set-url origin "%NEW_URL%"
echo [SUCCESS] Remote URL updated with token authentication

goto :test_push

:use_ssh
echo.
echo ============================================================
echo SSH Authentication Setup
echo ============================================================
echo.

REM Check if SSH key exists
if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
    echo [INFO] SSH key found. Make sure it's added to GitHub.
    echo Your public key:
    type "%USERPROFILE%\.ssh\id_rsa.pub"
    echo.
    echo Add this key to GitHub: https://github.com/settings/ssh/new
    pause
) else (
    echo [ERROR] No SSH key found. Generate one first.
    ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
    echo [SUCCESS] SSH key generated. Add it to GitHub.
    pause
)

REM Update remote to use SSH
for /f "tokens=2" %%i in ('git remote get-url origin') do set REPO_URL=%%i
echo %REPO_URL% | findstr "github.com" >nul
if errorlevel 1 (
    echo [ERROR] Not a GitHub repository
    pause
    exit /b 1
)

REM Extract repository path for SSH
for /f "tokens=2 delims=/" %%i in ("%REPO_URL%") do set GITHUB_USER=%%i
for /f "tokens=3 delims=/" %%i in ("%REPO_URL%") do set REPO_NAME=%%i

set SSH_URL=git@github.com:%GITHUB_USER%/%REPO_NAME%

git remote set-url origin "%SSH_URL%"
echo [SUCCESS] Remote URL updated to use SSH

goto :test_push

:use_gh_cli
echo.
echo ============================================================
echo GitHub CLI Setup
echo ============================================================
echo.

REM Check if GitHub CLI is installed
gh --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] GitHub CLI not installed. Installing...
    winget install --id GitHub.cli
    if errorlevel 1 (
        echo [ERROR] Failed to install GitHub CLI
        echo Please install manually from: https://cli.github.com/
        pause
        exit /b 1
    )
)

echo [INFO] Authenticating with GitHub CLI...
gh auth login

if errorlevel 0 (
    echo [SUCCESS] GitHub CLI authentication completed
    echo [INFO] Setting up Git credentials...
    gh auth setup-git
) else (
    echo [ERROR] GitHub CLI authentication failed
    pause
    exit /b 1
)

goto :test_push

:fix_https
echo.
echo ============================================================
echo HTTPS Authentication Fix
echo ============================================================
echo.

REM Clear any existing credentials
git config --global --unset credential.helper
git config --global credential.helper manager-core

REM Clear credential cache
for /f %%i in ('git config --get remote.origin.url') do (
    cmdkey /delete:git:%%i >nul 2>&1
)

echo [SUCCESS] Cleared existing credentials
echo [INFO] Next push will prompt for username and password/token

goto :test_push

:test_push
echo.
echo ============================================================
echo Testing Push to GitHub
echo ============================================================
echo.

echo [INFO] Attempting to push to GitHub...
git push -u origin main

if errorlevel 0 (
    echo.
    echo [SUCCESS] Successfully pushed to GitHub!
    echo.
    echo Your repository is now available at:
    for /f "tokens=2" %%i in ('git remote get-url origin') do echo https://github.com/%%i
    echo.
) else (
    echo.
    echo [ERROR] Push failed. Please check:
    echo 1. Your internet connection
    echo 2. GitHub repository exists and you have access
    echo 3. Authentication credentials are correct
    echo.
    echo Manual troubleshooting:
    echo - Try: git push -v origin main (verbose output)
    echo - Check: git remote -v
    echo - Verify: git config --list | findstr credential
)

echo.
echo ============================================================
echo GitHub Setup Status
echo ============================================================
echo.

echo Git Configuration:
git config --list | findstr "user\|credential\|remote"
echo.

echo Repository Status:
git status --short
echo.

echo Remote Repository:
git remote -v
echo.

echo Recent Commits:
git log --oneline -3
echo.

pause
