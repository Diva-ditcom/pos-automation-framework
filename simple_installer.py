#!/usr/bin/env python3
"""
SIMPLE PACKAGE INSTALLER - NO UNICODE
=====================================

Simple package installer that works in any terminal without Unicode support.
Installs core packages needed for POS automation testing.

Usage:
    python simple_installer.py
"""

import os
import sys
import subprocess
from pathlib import Path

def log(message):
    """Simple logging without Unicode"""
    print(f"[INFO] {message}")

def error(message):
    """Error logging without Unicode"""
    print(f"[ERROR] {message}")

def install_packages():
    """Install core packages using pip"""
    log("Installing core packages...")
    
    packages = [
        "pywinauto>=0.6.9",
        "pytest>=7.0.0", 
        "pytest-html>=3.1.0",
        "selenium>=4.0.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.0"
    ]
    
    success_count = 0
    
    for package in packages:
        log(f"Installing {package}...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                log(f"[OK] {package} installed successfully")
                success_count += 1
            else:
                error(f"Failed to install {package}: {result.stderr}")
                
        except Exception as e:
            error(f"Error installing {package}: {e}")
    
    log(f"Installation completed: {success_count}/{len(packages)} packages installed")
    return success_count >= 3  # At least 3 core packages

def verify_packages():
    """Verify that packages can be imported"""
    log("Verifying package installation...")
    
    packages_to_test = [
        "pywinauto",
        "pytest", 
        "selenium",
        "pandas"
    ]
    
    success_count = 0
    
    for package in packages_to_test:
        try:
            __import__(package)
            log(f"[OK] {package} imported successfully")
            success_count += 1
        except ImportError:
            error(f"{package} not available")
    
    return success_count >= 2

def main():
    """Main entry point"""
    print("=" * 60)
    print("POS AUTOMATION FRAMEWORK - SIMPLE INSTALLER")
    print("=" * 60)
    
    log("Starting simple package installation...")
    
    # Upgrade pip first
    log("Upgrading pip...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], capture_output=True, text=True)
        log("[OK] pip upgraded")
    except Exception as e:
        error(f"pip upgrade failed: {e}")
    
    # Install packages
    if install_packages():
        log("[OK] Package installation completed")
    else:
        error("Package installation failed")
        return False
    
    # Verify installation
    if verify_packages():
        log("[OK] Package verification passed")
        print("\n" + "=" * 60)
        print("INSTALLATION SUCCESSFUL!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run: python -m pytest tests/ -v")
        print("2. Check reports in reports/ directory")
        print("3. Configure your POS app settings in config/")
        return True
    else:
        error("Package verification failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
