@echo off
REM Git Installation and Setup for Windows
REM This script will guide you through installing Git and setting up GitHub

echo ============================================================
echo POS Automation Framework - Git and GitHub Setup
echo ============================================================
echo.

REM Check if Git is already installed
git --version >nul 2>&1
if errorlevel 0 (
    echo [SUCCESS] Git is already installed:
    git --version
    echo.
    goto :configure_git
) else (
    echo [INFO] Git is not installed on this machine
    echo.
)

:install_git
echo ============================================================
echo STEP 1: Git Installation Required
echo ============================================================
echo.
echo Git is required for version control and GitHub integration.
echo.
echo Please follow these steps:
echo.
echo 1. Download Git for Windows from: https://git-scm.com/download/win
echo 2. Run the installer with these recommended settings:
echo    - Use Git from the Windows Command Prompt
echo    - Use the OpenSSL library
echo    - Checkout Windows-style, commit Unix-style line endings
echo    - Use Windows' default console window
echo    - Enable file system caching
echo 3. Restart this script after installation
echo.
echo [OPTION] Quick install using winget (if available):
echo    winget install --id Git.Git -e --source winget
echo.
pause
echo.

REM Try winget installation
echo [INFO] Attempting automatic installation with winget...
winget install --id Git.Git -e --source winget >nul 2>&1
if errorlevel 0 (
    echo [SUCCESS] Git installed via winget
    echo [INFO] Please restart your command prompt and run this script again
    pause
    exit /b 0
) else (
    echo [INFO] winget not available or failed
    echo Please install Git manually from https://git-scm.com/download/win
    pause
    exit /b 1
)

:configure_git
echo ============================================================
echo STEP 2: Git Configuration
echo ============================================================
echo.

REM Check if Git is configured
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo [INFO] Git user configuration not found
    echo Please provide your Git configuration details:
    echo.
    set /p GIT_USERNAME="Enter your name (for Git commits): "
    set /p GIT_EMAIL="Enter your email address: "
    
    git config --global user.name "%GIT_USERNAME%"
    git config --global user.email "%GIT_EMAIL%"
    
    echo [SUCCESS] Git configured with:
    echo Name: %GIT_USERNAME%
    echo Email: %GIT_EMAIL%
) else (
    echo [SUCCESS] Git is already configured:
    echo Name: 
    git config --global user.name
    echo Email: 
    git config --global user.email
)
echo.

:setup_ssh
echo ============================================================
echo STEP 3: SSH Key Setup (Recommended)
echo ============================================================
echo.

set /p SETUP_SSH="Do you want to set up SSH keys for GitHub? (y/N): "
if /i "%SETUP_SSH%"=="y" (
    echo [INFO] Setting up SSH keys...
    
    REM Check if SSH key already exists
    if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
        echo [INFO] SSH key already exists
        echo Your public key:
        type "%USERPROFILE%\.ssh\id_rsa.pub"
        echo.
        echo Copy this key to GitHub Settings ^> SSH and GPG keys ^> New SSH key
    ) else (
        echo [INFO] Generating new SSH key...
        ssh-keygen -t rsa -b 4096 -C "%GIT_EMAIL%" -f "%USERPROFILE%\.ssh\id_rsa" -N ""
        
        if exist "%USERPROFILE%\.ssh\id_rsa.pub" (
            echo [SUCCESS] SSH key generated successfully
            echo.
            echo Your public key:
            type "%USERPROFILE%\.ssh\id_rsa.pub"
            echo.
            echo IMPORTANT: Copy the above key to GitHub:
            echo 1. Go to GitHub.com ^> Settings ^> SSH and GPG keys
            echo 2. Click "New SSH key"
            echo 3. Paste the key above
            echo 4. Give it a title like "Windows-POS-Framework"
        ) else (
            echo [ERROR] Failed to generate SSH key
        )
    )
    
    echo.
    pause
)

:repository_setup
echo ============================================================
echo STEP 4: Repository Setup
echo ============================================================
echo.

REM Check if we're already in a Git repository
git status >nul 2>&1
if errorlevel 0 (
    echo [SUCCESS] Already in a Git repository
    echo Repository status:
    git status --short
    echo.
    goto :github_remote
) else (
    echo [INFO] Initializing Git repository...
    git init
    if errorlevel 0 (
        echo [SUCCESS] Git repository initialized
    ) else (
        echo [ERROR] Failed to initialize Git repository
        pause
        exit /b 1
    )
)

:github_remote
echo Current remote repositories:
git remote -v
echo.

set /p SETUP_REMOTE="Do you want to set up GitHub remote repository? (y/N): "
if /i "%SETUP_REMOTE%"=="y" (
    echo.
    echo GitHub Repository Setup Options:
    echo 1. Connect to existing GitHub repository
    echo 2. Create new GitHub repository (manual)
    echo.
    set /p REMOTE_OPTION="Choose option (1/2): "
    
    if "%REMOTE_OPTION%"=="1" (
        set /p GITHUB_URL="Enter GitHub repository URL (https or SSH): "
        git remote add origin "%GITHUB_URL%"
        if errorlevel 0 (
            echo [SUCCESS] Remote repository added
        ) else (
            echo [ERROR] Failed to add remote repository
        )
    )
    
    if "%REMOTE_OPTION%"=="2" (
        echo.
        echo To create a new GitHub repository:
        echo 1. Go to GitHub.com
        echo 2. Click the "+" button ^> "New repository"
        echo 3. Name it: pos-automation-framework
        echo 4. Make it Private (recommended for business use)
        echo 5. Do NOT initialize with README (we already have files)
        echo 6. Copy the repository URL and run this script again
        echo.
        pause
    )
)

:commit_and_push
echo ============================================================
echo STEP 5: Initial Commit and Push
echo ============================================================
echo.

REM Check if there are changes to commit
git status --porcelain >nul 2>&1
if errorlevel 0 (
    echo [INFO] Checking for changes to commit...
    
    REM Add all files
    git add .
    
    REM Check if there's anything to commit
    git diff --cached --quiet
    if errorlevel 1 (
        echo [INFO] Committing changes...
        git commit -m "Initial commit: POS Automation Framework with clean installers and offline packages"
        
        if errorlevel 0 (
            echo [SUCCESS] Changes committed successfully
            
            REM Try to push if remote exists
            git remote get-url origin >nul 2>&1
            if errorlevel 0 (
                echo [INFO] Pushing to GitHub...
                git push -u origin main
                if errorlevel 0 (
                    echo [SUCCESS] Successfully pushed to GitHub
                ) else (
                    echo [WARNING] Push failed - you may need to authenticate
                    echo Try: git push -u origin main
                )
            ) else (
                echo [INFO] No remote repository configured
                echo Your changes are committed locally
            )
        ) else (
            echo [ERROR] Commit failed
        )
    ) else (
        echo [INFO] No changes to commit
    )
) else (
    echo [ERROR] Git status check failed
)

:final_verification
echo.
echo ============================================================
echo STEP 6: Verification
echo ============================================================
echo.

echo Git Configuration:
git config --list | findstr user
echo.

echo Repository Status:
git status
echo.

echo Remote Repositories:
git remote -v
echo.

echo Recent Commits:
git log --oneline -5 2>nul
echo.

echo ============================================================
echo GITHUB SETUP COMPLETED
echo ============================================================
echo.
echo Next Steps:
echo 1. Verify your repository on GitHub.com
echo 2. Set up branch protection rules (optional)
echo 3. Configure GitHub Actions (optional)
echo 4. Invite collaborators (if needed)
echo.
echo Framework Files Ready for GitHub:
echo - Clean installers (no Unicode issues)
echo - Offline packages (45.9 MB)
echo - Complete documentation
echo - Test automation scripts
echo.
pause
