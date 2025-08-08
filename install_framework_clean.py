#!/usr/bin/env python3
"""
Clean Windows-Compatible POS Automation Framework Installer
Removes all Unicode characters and provides robust error handling
"""

import os
import sys
import subprocess
import logging
import json
from pathlib import Path

# Configure logging with ASCII-only output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('installation.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class FrameworkInstaller:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.requirements_file = self.base_dir / "requirements.txt"
        self.offline_packages_dir = self.base_dir / "offline_packages"
        self.installation_log = []
        
    def log_step(self, message, success=True):
        """Log installation step with ASCII-only characters"""
        status = "[SUCCESS]" if success else "[FAILED]"
        log_message = f"{status} {message}"
        logger.info(log_message)
        self.installation_log.append({
            "message": message,
            "success": success,
            "timestamp": str(Path().cwd())
        })
        
    def check_python_version(self):
        """Check Python version compatibility"""
        try:
            version = sys.version_info
            if version.major < 3 or (version.major == 3 and version.minor < 7):
                self.log_step("Python 3.7+ required. Current version: {}.{}".format(
                    version.major, version.minor), False)
                return False
            
            self.log_step("Python version check passed: {}.{}.{}".format(
                version.major, version.minor, version.micro))
            return True
        except Exception as e:
            self.log_step(f"Failed to check Python version: {e}", False)
            return False
    
    def install_pip_if_missing(self):
        """Ensure pip is available"""
        try:
            import pip
            self.log_step("pip is already available")
            return True
        except ImportError:
            try:
                self.log_step("Installing pip...")
                subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
                self.log_step("pip installed successfully")
                return True
            except Exception as e:
                self.log_step(f"Failed to install pip: {e}", False)
                return False
    
    def install_from_offline_packages(self):
        """Install packages from offline cache if available"""
        if not self.offline_packages_dir.exists():
            self.log_step("No offline packages directory found")
            return False
            
        try:
            wheel_files = list(self.offline_packages_dir.glob("*.whl"))
            if not wheel_files:
                self.log_step("No wheel files found in offline packages")
                return False
                
            self.log_step(f"Found {len(wheel_files)} offline packages")
            
            # Install all wheel files
            cmd = [sys.executable, "-m", "pip", "install", "--no-index", 
                   "--find-links", str(self.offline_packages_dir)]
            cmd.extend([str(whl) for whl in wheel_files])
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                self.log_step("Offline packages installed successfully")
                return True
            else:
                self.log_step(f"Offline installation failed: {result.stderr}", False)
                return False
                
        except Exception as e:
            self.log_step(f"Error during offline installation: {e}", False)
            return False
    
    def install_from_requirements(self):
        """Install packages from requirements.txt"""
        if not self.requirements_file.exists():
            self.log_step("requirements.txt not found", False)
            return False
            
        try:
            self.log_step("Installing packages from requirements.txt...")
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)]
            
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  encoding='utf-8', timeout=300)
            
            if result.returncode == 0:
                self.log_step("Requirements installed successfully")
                return True
            else:
                self.log_step(f"Requirements installation failed: {result.stderr}", False)
                return False
                
        except subprocess.TimeoutExpired:
            self.log_step("Installation timed out (network issues?)", False)
            return False
        except Exception as e:
            self.log_step(f"Error during requirements installation: {e}", False)
            return False
    
    def verify_installation(self):
        """Verify that key packages are installed"""
        required_packages = ['pytest', 'pywinauto', 'pandas', 'openpyxl']
        
        for package in required_packages:
            try:
                __import__(package)
                self.log_step(f"Package {package} is available")
            except ImportError:
                self.log_step(f"Package {package} is NOT available", False)
                return False
        
        self.log_step("All required packages verified")
        return True
    
    def run_simple_test(self):
        """Run a simple test to verify framework works"""
        try:
            test_script = """
import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Framework test completed successfully")
"""
            
            exec(test_script)
            self.log_step("Framework test passed")
            return True
            
        except Exception as e:
            self.log_step(f"Framework test failed: {e}", False)
            return False
    
    def save_installation_report(self):
        """Save installation report"""
        try:
            report = {
                "installation_steps": self.installation_log,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
                "working_directory": str(Path.cwd())
            }
            
            report_file = self.base_dir / "installation_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
                
            self.log_step(f"Installation report saved to {report_file}")
            
        except Exception as e:
            self.log_step(f"Failed to save installation report: {e}", False)
    
    def install(self):
        """Main installation process"""
        print("=" * 60)
        print("POS Automation Framework Installer")
        print("=" * 60)
        
        # Step 1: Check Python version
        if not self.check_python_version():
            print("\nInstallation failed: Python version incompatible")
            return False
        
        # Step 2: Ensure pip is available
        if not self.install_pip_if_missing():
            print("\nInstallation failed: Could not setup pip")
            return False
        
        # Step 3: Try offline installation first
        offline_success = self.install_from_offline_packages()
        
        # Step 4: If offline failed, try online installation
        if not offline_success:
            self.log_step("Attempting online installation...")
            online_success = self.install_from_requirements()
            
            if not online_success:
                print("\nInstallation failed: Could not install packages")
                print("Please check your internet connection or use offline packages")
                return False
        
        # Step 5: Verify installation
        if not self.verify_installation():
            print("\nInstallation failed: Package verification failed")
            return False
        
        # Step 6: Run simple test
        if not self.run_simple_test():
            print("\nWarning: Framework test failed, but packages are installed")
        
        # Step 7: Save report
        self.save_installation_report()
        
        print("\n" + "=" * 60)
        print("INSTALLATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run: python -m pytest tests/ --verbose")
        print("2. Check installation_report.json for details")
        print("3. Review README.md for usage instructions")
        
        return True

def main():
    """Main entry point"""
    try:
        installer = FrameworkInstaller()
        success = installer.install()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
