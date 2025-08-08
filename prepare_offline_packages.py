#!/usr/bin/env python3
"""
Offline Package Downloader for POS Automation Framework
Downloads all required packages as wheel files for offline installation
Handles encoding issues and provides robust error handling
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import json

# Configure logging with proper encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('package_download.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class OfflinePackageDownloader:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.requirements_file = self.base_dir / "requirements.txt"
        self.offline_dir = self.base_dir / "offline_packages"
        self.download_log = []
        
    def log_step(self, message, success=True):
        """Log download step with ASCII-only output"""
        status = "[SUCCESS]" if success else "[FAILED]"
        log_message = f"{status} {message}"
        logger.info(log_message)
        self.download_log.append({
            "message": message,
            "success": success
        })
        
    def check_internet_connection(self):
        """Check if internet connection is available"""
        try:
            import urllib.request
            urllib.request.urlopen('https://pypi.org', timeout=10)
            self.log_step("Internet connection verified")
            return True
        except Exception as e:
            self.log_step(f"No internet connection: {e}", False)
            return False
    
    def setup_offline_directory(self):
        """Create offline packages directory"""
        try:
            self.offline_dir.mkdir(exist_ok=True)
            self.log_step(f"Offline directory ready: {self.offline_dir}")
            return True
        except Exception as e:
            self.log_step(f"Failed to create offline directory: {e}", False)
            return False
    
    def download_packages(self):
        """Download all packages from requirements.txt as wheel files"""
        if not self.requirements_file.exists():
            self.log_step("requirements.txt not found", False)
            return False
            
        try:
            self.log_step("Starting package download...")
            
            # Download packages
            cmd = [
                sys.executable, "-m", "pip", "download",
                "-r", str(self.requirements_file),
                "--dest", str(self.offline_dir),
                "--prefer-binary"
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0:
                self.log_step("Package download completed")
                return True
            else:
                self.log_step(f"Download failed: {result.stderr}", False)
                return False
                
        except subprocess.TimeoutExpired:
            self.log_step("Download timed out", False)
            return False
        except Exception as e:
            self.log_step(f"Error during download: {e}", False)
            return False
    
    def verify_downloads(self):
        """Verify that packages were downloaded"""
        try:
            wheel_files = list(self.offline_dir.glob("*.whl"))
            tar_files = list(self.offline_dir.glob("*.tar.gz"))
            
            total_files = len(wheel_files) + len(tar_files)
            
            if total_files == 0:
                self.log_step("No packages downloaded", False)
                return False
            
            self.log_step(f"Downloaded {len(wheel_files)} wheel files and {len(tar_files)} source packages")
            
            # Log file sizes
            total_size = 0
            for file_path in wheel_files + tar_files:
                size = file_path.stat().st_size
                total_size += size
                
            self.log_step(f"Total download size: {total_size / (1024*1024):.1f} MB")
            return True
            
        except Exception as e:
            self.log_step(f"Error verifying downloads: {e}", False)
            return False
    
    def create_offline_installer(self):
        """Create a simple offline installer script"""
        try:
            installer_content = '''#!/usr/bin/env python3
"""
Offline Package Installer
Run this script on the target machine to install all downloaded packages
"""

import sys
import subprocess
from pathlib import Path

def install_offline_packages():
    """Install packages from offline directory"""
    offline_dir = Path(__file__).parent
    wheel_files = list(offline_dir.glob("*.whl"))
    tar_files = list(offline_dir.glob("*.tar.gz"))
    
    if not wheel_files and not tar_files:
        print("[ERROR] No package files found")
        return False
    
    print(f"[INFO] Installing {len(wheel_files)} wheel files and {len(tar_files)} source packages...")
    
    try:
        # Install wheel files first
        if wheel_files:
            cmd = [sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(offline_dir)]
            cmd.extend([str(whl) for whl in wheel_files])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[ERROR] Failed to install packages: {result.stderr}")
                return False
        
        print("[SUCCESS] Offline packages installed successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] Installation failed: {e}")
        return False

if __name__ == "__main__":
    success = install_offline_packages()
    sys.exit(0 if success else 1)
'''
            
            installer_path = self.offline_dir / "install_offline_packages.py"
            with open(installer_path, 'w', encoding='utf-8') as f:
                f.write(installer_content)
                
            self.log_step(f"Offline installer created: {installer_path}")
            return True
            
        except Exception as e:
            self.log_step(f"Failed to create offline installer: {e}", False)
            return False
    
    def create_readme(self):
        """Create README for offline packages"""
        try:
            readme_content = """# Offline Packages for POS Automation Framework

This directory contains all the packages needed to install the POS Automation Framework offline.

## Installation on Offline Machine

1. Copy this entire 'offline_packages' directory to the target machine
2. Navigate to this directory in a terminal/command prompt
3. Run one of the following:

### Option 1: Use Python installer
```
python install_offline_packages.py
```

### Option 2: Use pip directly
```
python -m pip install --no-index --find-links . *.whl
```

### Option 3: Use Windows batch file (if available)
```
install_offline.bat
```

## Files in this directory

- *.whl: Pre-compiled wheel packages (preferred)
- *.tar.gz: Source packages (fallback)
- install_offline_packages.py: Python installer script
- README.md: This file

## Requirements

- Python 3.7 or higher
- pip (usually included with Python)

## Troubleshooting

If installation fails:
1. Check that Python is in your PATH
2. Try upgrading pip: `python -m pip install --upgrade pip`
3. Install packages one by one to identify issues
4. Check the error messages for specific package conflicts

## Package List

This offline package set includes all dependencies for:
- pytest (testing framework)
- pywinauto (Windows GUI automation)
- pandas (data manipulation)
- openpyxl (Excel file handling)
- And all their dependencies
"""
            
            readme_path = self.offline_dir / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
                
            self.log_step(f"README created: {readme_path}")
            return True
            
        except Exception as e:
            self.log_step(f"Failed to create README: {e}", False)
            return False
    
    def save_download_report(self):
        """Save download report"""
        try:
            report = {
                "download_steps": self.download_log,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
                "offline_directory": str(self.offline_dir),
                "files_downloaded": []
            }
            
            # List downloaded files
            for file_path in self.offline_dir.iterdir():
                if file_path.is_file() and file_path.suffix in ['.whl', '.tar.gz']:
                    report["files_downloaded"].append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size
                    })
            
            report_file = self.base_dir / "package_download_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
                
            self.log_step(f"Download report saved: {report_file}")
            
        except Exception as e:
            self.log_step(f"Failed to save download report: {e}", False)
    
    def download(self):
        """Main download process"""
        print("=" * 60)
        print("POS Automation Framework - Offline Package Downloader")
        print("=" * 60)
        print()
        
        # Step 1: Check internet connection
        if not self.check_internet_connection():
            print("\n[ERROR] No internet connection available")
            print("This script must be run on a machine with internet access")
            return False
        
        # Step 2: Setup offline directory
        if not self.setup_offline_directory():
            print("\n[ERROR] Could not create offline directory")
            return False
        
        # Step 3: Download packages
        if not self.download_packages():
            print("\n[ERROR] Package download failed")
            return False
        
        # Step 4: Verify downloads
        if not self.verify_downloads():
            print("\n[ERROR] Download verification failed")
            return False
        
        # Step 5: Create offline installer
        if not self.create_offline_installer():
            print("\n[WARNING] Could not create offline installer")
        
        # Step 6: Create README
        if not self.create_readme():
            print("\n[WARNING] Could not create README")
        
        # Step 7: Save report
        self.save_download_report()
        
        print("\n" + "=" * 60)
        print("PACKAGE DOWNLOAD COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"\nOffline packages saved to: {self.offline_dir}")
        print("\nNext steps:")
        print("1. Copy the 'offline_packages' directory to your target machine")
        print("2. Run 'python install_offline_packages.py' in that directory")
        print("3. Or use the install_offline.bat script if available")
        
        return True

def main():
    """Main entry point"""
    try:
        downloader = OfflinePackageDownloader()
        success = downloader.download()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nDownload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
