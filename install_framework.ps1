# POS Automation Framework - PowerShell Installer
# This script downloads and sets up the complete framework

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "POS Automation Framework - Automated Installer" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to write status messages
function Write-Status {
    param($Message, $Type = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    switch ($Type) {
        "SUCCESS" { Write-Host "[$timestamp] [SUCCESS] $Message" -ForegroundColor Green }
        "ERROR"   { Write-Host "[$timestamp] [ERROR] $Message" -ForegroundColor Red }
        "WARNING" { Write-Host "[$timestamp] [WARNING] $Message" -ForegroundColor Yellow }
        default   { Write-Host "[$timestamp] [INFO] $Message" -ForegroundColor White }
    }
}

# Check PowerShell execution policy
$policy = Get-ExecutionPolicy
if ($policy -eq "Restricted") {
    Write-Status "PowerShell execution policy is restricted" "WARNING"
    Write-Host "Run this command as Administrator: Set-ExecutionPolicy RemoteSigned" -ForegroundColor Yellow
    Write-Host "Then run this script again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Check Python
Write-Status "Checking Python installation..."
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Python found: $pythonVersion" "SUCCESS"
    } else {
        throw "Python not found"
    }
} catch {
    Write-Status "Python is not installed or not in PATH" "ERROR"
    Write-Host "Please install Python 3.7+ from https://python.org" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Download Framework
Write-Status "Checking if framework is already present..."
if (Test-Path "install_clean.bat" -and Test-Path "requirements.txt") {
    Write-Status "Framework already present" "SUCCESS"
} else {
    Write-Status "Downloading framework from GitHub..."
    
    $repoUrl = "https://github.com/Diva-ditcom/pos-automation-framework/archive/refs/heads/main.zip"
    $zipFile = "framework.zip"
    
    try {
        # Download the framework
        Invoke-WebRequest -Uri $repoUrl -OutFile $zipFile -UseBasicParsing
        Write-Status "Framework downloaded successfully" "SUCCESS"
        
        # Extract the framework
        Write-Status "Extracting framework..."
        Expand-Archive -Path $zipFile -DestinationPath "temp" -Force
        
        # Move files to current directory
        $extractedDir = "temp\pos-automation-framework-main"
        if (Test-Path $extractedDir) {
            Get-ChildItem $extractedDir | Move-Item -Destination . -Force
            Write-Status "Framework extracted successfully" "SUCCESS"
        } else {
            throw "Extraction failed - directory not found"
        }
        
        # Cleanup
        Remove-Item $zipFile -Force -ErrorAction SilentlyContinue
        Remove-Item "temp" -Recurse -Force -ErrorAction SilentlyContinue
        
    } catch {
        Write-Status "Download failed: $($_.Exception.Message)" "ERROR"
        Write-Host "Please download manually from: https://github.com/Diva-ditcom/pos-automation-framework" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Step 3: Install Framework Packages
Write-Status "Installing framework packages..."
if (Test-Path "install_clean.bat") {
    try {
        & .\install_clean.bat
        Write-Status "Framework packages installed" "SUCCESS"
    } catch {
        Write-Status "Package installation failed" "ERROR"
    }
} else {
    Write-Status "install_clean.bat not found" "ERROR"
}

# Step 4: Git Setup (Optional)
Write-Status "Checking Git installation..."
try {
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Git found: $gitVersion" "SUCCESS"
        
        # Check if Git is configured
        $gitName = git config --global user.name 2>$null
        if (-not $gitName) {
            Write-Status "Git needs configuration" "WARNING"
            if (Test-Path "install_git_complete.bat") {
                $setupGit = Read-Host "Do you want to setup Git and GitHub now? (y/N)"
                if ($setupGit -eq "y" -or $setupGit -eq "Y") {
                    & .\install_git_complete.bat
                }
            }
        } else {
            Write-Status "Git is already configured for: $gitName" "SUCCESS"
        }
    } else {
        throw "Git not found"
    }
} catch {
    Write-Status "Git not installed" "WARNING"
    if (Test-Path "install_git_auto.bat") {
        $installGit = Read-Host "Do you want to install Git now? (y/N)"
        if ($installGit -eq "y" -or $installGit -eq "Y") {
            & .\install_git_auto.bat
        }
    }
}

# Step 5: Verification
Write-Status "Verifying installation..."

# Check Python packages
try {
    python -c "import pytest, pywinauto, pandas, openpyxl; print('All packages OK')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Status "All Python packages verified" "SUCCESS"
    } else {
        Write-Status "Some Python packages missing" "WARNING"
    }
} catch {
    Write-Status "Package verification failed" "WARNING"
}

# Check framework
try {
    python -c "from utils.pos_base import POSAutomation; print('Framework OK')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Framework loads correctly" "SUCCESS"
    } else {
        Write-Status "Framework has issues" "WARNING"
    }
} catch {
    Write-Status "Framework verification failed" "WARNING"
}

# Final Summary
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "INSTALLATION COMPLETED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Configure POS application: data\app_settings.csv" -ForegroundColor White
Write-Host "2. Update test data: data\test_scenarios.csv" -ForegroundColor White
Write-Host "3. Test connection: python test_pos_connection.py" -ForegroundColor White
Write-Host "4. Run tests: python -m pytest tests\ --verbose" -ForegroundColor White
Write-Host ""
Write-Host "Framework Location: $PWD" -ForegroundColor Cyan
Write-Host ""

$openConfig = Read-Host "Do you want to open configuration files now? (y/N)"
if ($openConfig -eq "y" -or $openConfig -eq "Y") {
    if (Test-Path "data\app_settings.csv") { Start-Process notepad "data\app_settings.csv" }
    if (Test-Path "data\test_scenarios.csv") { Start-Process notepad "data\test_scenarios.csv" }
}

Write-Host "Setup completed! Happy testing! 🎉" -ForegroundColor Green
Read-Host "Press Enter to exit"
