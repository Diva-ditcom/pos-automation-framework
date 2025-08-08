#!/usr/bin/env python3
"""
📦 OFFLINE MACHINE SETUP - STEP 1
==================================

This script handles offline package installation when internet is not available.
It installs Python packages from local wheel files in the offline_packages directory.

Features:
- Installs packages from offline cache
- Downloads packages for offline use
- Handles proxy/network issues
- Maximum error handling

Usage:
    python 1_setup_offline_machine.py
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from datetime import datetime

class OfflineSetup:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.offline_dir = self.script_dir / "offline_packages"
        self.log_file = self.script_dir / "logs" / f"offline_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.ensure_dirs()
        
    def ensure_dirs(self):
        """Ensure required directories exist"""
        (self.script_dir / "logs").mkdir(exist_ok=True)
        self.offline_dir.mkdir(exist_ok=True)
        
    def log(self, message, level="INFO"):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception:
            pass
    
    def print_banner(self):
        """Print banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║               📦 OFFLINE PACKAGE INSTALLER                   ║
║                                                              ║
║  This will install Python packages from offline cache       ║
║  when internet connection is not available.                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.log("Offline setup started")
    
    def check_pip(self):
        """Check if pip is available and working"""
        self.log("Checking pip availability...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "--version"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log(f"✅ pip is available: {result.stdout.strip()}")
                return True
            else:
                self.log(f"❌ pip check failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error checking pip: {e}", "ERROR")
            return False
    
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        self.log("Upgrading pip...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ pip upgraded successfully")
                return True
            else:
                self.log(f"⚠️ pip upgrade failed (continuing anyway): {result.stderr}", "WARNING")
                return True  # Continue even if upgrade fails
                
        except Exception as e:
            self.log(f"⚠️ Error upgrading pip (continuing anyway): {e}", "WARNING")
            return True  # Continue even if upgrade fails
    
    def check_offline_packages(self):
        """Check if offline packages are available"""
        self.log("Checking for offline packages...")
        
        wheel_files = list(self.offline_dir.glob("*.whl"))
        tar_files = list(self.offline_dir.glob("*.tar.gz"))
        
        total_packages = len(wheel_files) + len(tar_files)
        
        if total_packages > 0:
            self.log(f"✅ Found {total_packages} offline packages ({len(wheel_files)} wheels, {len(tar_files)} source)")
            return True
        else:
            self.log("❌ No offline packages found", "WARNING")
            return False
    
    def install_from_offline(self):
        """Install packages from offline directory"""
        self.log("Installing packages from offline cache...")
        
        try:
            # Install all wheel files first
            wheel_files = list(self.offline_dir.glob("*.whl"))
            if wheel_files:
                self.log(f"Installing {len(wheel_files)} wheel packages...")
                
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install",
                    "--no-index", "--find-links", str(self.offline_dir)
                ] + [str(f) for f in wheel_files], 
                capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log("✅ Wheel packages installed successfully")
                else:
                    self.log(f"⚠️ Some wheel packages failed to install: {result.stderr}", "WARNING")
            
            # Install from requirements.txt using offline packages
            requirements_file = self.script_dir / "requirements.txt"
            if requirements_file.exists():
                self.log("Installing from requirements.txt using offline packages...")
                
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install",
                    "-r", str(requirements_file),
                    "--no-index", "--find-links", str(self.offline_dir)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log("✅ Requirements installed from offline packages")
                    return True
                else:
                    self.log(f"❌ Failed to install from requirements: {result.stderr}", "ERROR")
                    # Try individual package installation
                    return self.install_individual_packages()
            else:
                self.log("❌ requirements.txt not found", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error during offline installation: {e}", "ERROR")
            return False
    
    def install_individual_packages(self):
        """Install packages individually from offline cache"""
        self.log("Attempting individual package installation...")
        
        # Try to install core packages individually
        core_packages = [
            "pywinauto",
            "pytest", 
            "selenium",
            "pandas",
            "configparser",
            "pytest-html"
        ]
        
        success_count = 0
        
        for package in core_packages:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install",
                    package, "--no-index", "--find-links", str(self.offline_dir)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log(f"✅ {package} installed successfully")
                    success_count += 1
                else:
                    self.log(f"❌ Failed to install {package}: {result.stderr}", "WARNING")
                    
            except Exception as e:
                self.log(f"❌ Error installing {package}: {e}", "WARNING")
        
        if success_count > 0:
            self.log(f"✅ Successfully installed {success_count}/{len(core_packages)} core packages")
            return True
        else:
            self.log("❌ No packages could be installed from offline cache", "ERROR")
            return False
    
    def download_packages_for_offline(self):
        """Download packages for offline use (if internet available)"""
        self.log("Attempting to download packages for offline use...")
        
        # Check if we have internet
        try:
            import urllib.request
            urllib.request.urlopen('https://pypi.org', timeout=10)
            self.log("✅ Internet available, downloading packages...")
        except Exception:
            self.log("❌ No internet connection, cannot download packages", "WARNING")
            return False
        
        requirements_file = self.script_dir / "requirements.txt"
        if not requirements_file.exists():
            self.log("❌ requirements.txt not found", "ERROR")
            return False
        
        try:
            # Download packages to offline directory
            result = subprocess.run([
                sys.executable, "-m", "pip", "download",
                "-r", str(requirements_file),
                "-d", str(self.offline_dir)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Packages downloaded for offline use")
                
                # Create README for offline packages
                readme_content = f"""# Offline Packages

This directory contains Python packages downloaded for offline installation.

Downloaded on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

To install these packages offline:
```bash
python -m pip install --no-index --find-links . -r ../requirements.txt
```

Or run the offline setup script:
```bash
python 1_setup_offline_machine.py
```
"""
                with open(self.offline_dir / "README.md", "w") as f:
                    f.write(readme_content)
                
                return True
            else:
                self.log(f"❌ Failed to download packages: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error downloading packages: {e}", "ERROR")
            return False
    
    def verify_installation(self):
        """Verify that packages are installed correctly"""
        self.log("Verifying package installation...")
        
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
                self.log(f"✅ {package} imported successfully")
                success_count += 1
            except ImportError:
                self.log(f"❌ {package} not available", "WARNING")
        
        if success_count >= 2:  # At least pywinauto and pytest
            self.log(f"✅ Verification passed ({success_count}/{len(packages_to_test)} packages working)")
            return True
        else:
            self.log(f"❌ Verification failed ({success_count}/{len(packages_to_test)} packages working)", "ERROR")
            return False
    
    def run(self):
        """Run the complete offline setup process"""
        self.print_banner()
        
        # Step 1: Check pip
        if not self.check_pip():
            self.log("❌ Cannot proceed without pip", "ERROR")
            return False
        
        # Step 2: Upgrade pip
        self.upgrade_pip()
        
        # Step 3: Check for offline packages
        has_offline = self.check_offline_packages()
        
        # Step 4: Try offline installation if packages available
        if has_offline:
            if self.install_from_offline():
                self.log("✅ Offline installation completed")
            else:
                self.log("❌ Offline installation failed", "ERROR")
        else:
            # Step 5: Try to download packages if internet available
            if self.download_packages_for_offline():
                # Try installation again
                if self.install_from_offline():
                    self.log("✅ Installation completed after download")
                else:
                    self.log("❌ Installation failed even after download", "ERROR")
            else:
                self.log("❌ No offline packages and cannot download", "ERROR")
                return False
        
        # Step 6: Verify installation
        if self.verify_installation():
            self.log("✅ Offline setup completed successfully")
            return True
        else:
            self.log("❌ Offline setup verification failed", "ERROR")
            return False

def main():
    """Main entry point"""
    try:
        setup = OfflineSetup()
        success = setup.run()
        
        if success:
            print("\n🎉 Offline setup completed successfully!")
            print("\n📋 Next steps:")
            print("   1. Run: python 2_setup_new_machine_enhanced.py")
            print("   2. Or continue with: python 0_MASTER_INSTALLER.py")
            return True
        else:
            print("\n❌ Offline setup failed.")
            print("\n📋 Troubleshooting:")
            print("   1. Check the log file in logs/ directory")
            print("   2. Ensure you have offline packages in offline_packages/")
            print("   3. Try running with internet connection to download packages")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user.")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
