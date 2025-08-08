#!/usr/bin/env python3
"""
Offline Package Installation Script
Installs packages from local wheel files without internet access
"""
import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"[*] {text}")
    print("=" * 60)


def install_offline_packages():
    """Install packages from offline directory"""
    print_header("Offline Package Installation")
    
    offline_dir = Path("offline_packages")
    
    if not offline_dir.exists():
        print("[-] Offline packages directory not found!")
        return False
    
    # Check for packages
    wheel_files = list(offline_dir.glob("*.whl"))
    tar_files = list(offline_dir.glob("*.tar.gz"))
    
    if not (wheel_files or tar_files):
        print("[-] No packages found in offline_packages directory!")
        return False
    
    print(f"[*] Found {len(wheel_files)} wheel files and {len(tar_files)} source packages")
    
    # Install from offline packages
    try:
        print("\n[+] Installing packages from offline directory...")
        
        # Method 1: Install using --find-links (preferred)
        install_cmd = [
            sys.executable, "-m", "pip", "install",
            "--no-index",  # Don't use PyPI
            "--find-links", str(offline_dir),  # Look in offline directory
            "-r", "requirements.txt"
        ]
        
        result = subprocess.run(install_cmd, check=True)
        
        print("[+] All packages installed successfully from offline directory!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[-] Installation failed with exit code {e.returncode}")
        
        # Fallback: Try installing wheel files directly
        print("\n[!] Trying fallback installation method...")
        try:
            for wheel_file in wheel_files:
                print(f"   Installing {wheel_file.name}...")
                subprocess.run([sys.executable, "-m", "pip", "install", str(wheel_file)], check=True)
            
            print("[+] Packages installed using fallback method!")
            return True
            
        except subprocess.CalledProcessError as e2:
            print(f"[-] Fallback installation also failed: {e2}")
            return False
    
    except Exception as e:
        print(f"[-] Installation error: {e}")
        return False


def verify_installation():
    """Verify that packages are installed correctly"""
    print("\n[*] Verifying installation...")
    
    # Test imports
    tests = [
        ("pywinauto", "import pywinauto; print(f'pywinauto {pywinauto.__version__}')"),
        ("pytest", "import pytest; print(f'pytest {pytest.__version__}')"),
        ("pytest-html", "import pytest_html; print('pytest-html available')"),
    ]
    
    for name, test_code in tests:
        try:
            result = subprocess.run([sys.executable, "-c", test_code], 
                                 capture_output=True, text=True, check=True)
            print(f"   [+] {name}: {result.stdout.strip()}")
        except:
            print(f"   [-] {name}: Failed to import")


if __name__ == "__main__":
    success = install_offline_packages()
    
    if success:
        verify_installation()
        print("\n[+] Offline installation completed successfully!")
        print("\nNext steps:")
        print("   1. Run: python setup_new_machine.py")
        print("   2. Or run: python run_tests.py")
    else:
        print("\n[-] Offline installation failed!")
        print("\nTroubleshooting:")
        print("   • Ensure offline_packages directory contains wheel files")
        print("   • Try: python download_offline_packages.py")
        print("   • Check Python version compatibility")
    
    input("\nPress Enter to continue...")
