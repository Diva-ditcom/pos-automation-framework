#!/usr/bin/env python3
"""
🚀 MASTER POS AUTOMATION FRAMEWORK INSTALLER 🚀
==================================================

This is the ONE-CLICK master installer that will:
1. Check your system
2. Install offline packages if needed
3. Set up the project environment
4. Deploy to GitHub (optional)
5. Verify everything works

Just run this file and follow the prompts!

Author: POS Automation Team
Version: 1.0
Last Updated: 2024
"""

import os
import sys
import subprocess
import platform
import shutil
import json
from pathlib import Path
from datetime import datetime

class MasterInstaller:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.project_name = "pos-automation-framework"
        self.log_file = self.script_dir / "logs" / f"master_install_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.ensure_logs_dir()
        
    def ensure_logs_dir(self):
        """Ensure logs directory exists"""
        logs_dir = self.script_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
    def log(self, message, level="INFO"):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def print_banner(self):
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║           🚀 POS AUTOMATION FRAMEWORK INSTALLER 🚀           ║
║                                                              ║
║  This installer will set up everything you need to run      ║
║  automated POS testing with pywinauto and pytest.          ║
║                                                              ║
║  Features:                                                   ║
║  ✅ Offline package installation                            ║
║  ✅ Project environment setup                               ║
║  ✅ GitHub integration                                       ║
║  ✅ CI/CD pipeline configuration                            ║
║  ✅ Error handling and recovery                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.log("Master installer started")
    
    def check_system(self):
        """Check system requirements"""
        self.log("Checking system requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
            self.log("ERROR: Python 3.7+ required. Current version: " + sys.version, "ERROR")
            return False
            
        self.log(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check OS
        os_name = platform.system()
        self.log(f"✅ Operating System: {os_name}")
        
        if os_name != "Windows":
            self.log("WARNING: This framework is optimized for Windows", "WARNING")
        
        # Check if we're in the right directory
        required_files = ["requirements.txt", "config", "tests", "data"]
        missing_files = []
        
        for file in required_files:
            if not (self.script_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.log(f"ERROR: Missing required files/folders: {missing_files}", "ERROR")
            self.log("Make sure you're running this from the pywinauto project directory", "ERROR")
            return False
        
        self.log("✅ All required project files found")
        return True
    
    def check_internet_connection(self):
        """Check if internet connection is available"""
        self.log("Checking internet connection...")
        
        try:
            import urllib.request
            urllib.request.urlopen('https://pypi.org', timeout=10)
            self.log("✅ Internet connection available")
            return True
        except Exception as e:
            self.log(f"❌ No internet connection: {e}", "WARNING")
            return False
    
    def install_offline_packages(self):
        """Install packages from offline cache if available"""
        self.log("Attempting offline package installation...")
        
        offline_script = self.script_dir / "1_setup_offline_machine.py"
        if not offline_script.exists():
            self.log("❌ Offline installer not found", "ERROR")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, str(offline_script)
            ], capture_output=True, text=True, cwd=str(self.script_dir))
            
            if result.returncode == 0:
                self.log("✅ Offline packages installed successfully")
                return True
            else:
                self.log(f"❌ Offline installation failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error running offline installer: {e}", "ERROR")
            return False
    
    def setup_environment(self):
        """Set up the project environment"""
        self.log("Setting up project environment...")
        
        setup_script = self.script_dir / "2_setup_new_machine_enhanced.py"
        if not setup_script.exists():
            self.log("❌ Environment setup script not found", "ERROR")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, str(setup_script)
            ], capture_output=True, text=True, cwd=str(self.script_dir))
            
            if result.returncode == 0:
                self.log("✅ Environment setup completed successfully")
                return True
            else:
                self.log(f"❌ Environment setup failed: {result.stderr}", "ERROR")
                self.log(f"Output: {result.stdout}", "INFO")
                return False
                
        except Exception as e:
            self.log(f"❌ Error running environment setup: {e}", "ERROR")
            return False
    
    def setup_github(self):
        """Optionally set up GitHub integration"""
        self.log("GitHub setup (optional)")
        
        response = input("\n🤔 Do you want to set up GitHub integration? (y/N): ").strip().lower()
        
        if response not in ['y', 'yes']:
            self.log("⏭️ Skipping GitHub setup")
            return True
        
        github_script = self.script_dir / "3_deploy_to_github.py"
        if not github_script.exists():
            self.log("❌ GitHub deployment script not found", "ERROR")
            return False
        
        try:
            # Run GitHub setup interactively
            result = subprocess.run([
                sys.executable, str(github_script)
            ], cwd=str(self.script_dir))
            
            if result.returncode == 0:
                self.log("✅ GitHub setup completed successfully")
                return True
            else:
                self.log("❌ GitHub setup failed", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"❌ Error running GitHub setup: {e}", "ERROR")
            return False
    
    def verify_installation(self):
        """Verify that everything is working"""
        self.log("Verifying installation...")
        
        # Check if key packages are importable
        packages_to_test = [
            "pywinauto",
            "pytest", 
            "selenium",
            "pandas",
            "configparser"
        ]
        
        failed_imports = []
        
        for package in packages_to_test:
            try:
                __import__(package)
                self.log(f"✅ {package} imported successfully")
            except ImportError as e:
                self.log(f"❌ Failed to import {package}: {e}", "ERROR")
                failed_imports.append(package)
        
        if failed_imports:
            self.log(f"❌ Some packages failed to import: {failed_imports}", "ERROR")
            return False
        
        # Try to run a simple test
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", "--version"
            ], capture_output=True, text=True, cwd=str(self.script_dir))
            
            if result.returncode == 0:
                self.log("✅ pytest is working correctly")
            else:
                self.log("❌ pytest test failed", "WARNING")
                
        except Exception as e:
            self.log(f"❌ Error testing pytest: {e}", "WARNING")
        
        self.log("✅ Installation verification completed")
        return True
    
    def print_summary(self, success_steps, failed_steps):
        """Print installation summary"""
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📋 INSTALLATION SUMMARY                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ Successful Steps: {len(success_steps):2d}                                ║
║  ❌ Failed Steps:     {len(failed_steps):2d}                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

✅ SUCCESSFUL STEPS:
"""
        for step in success_steps:
            summary += f"   • {step}\n"
            
        if failed_steps:
            summary += f"\n❌ FAILED STEPS:\n"
            for step in failed_steps:
                summary += f"   • {step}\n"
            
            summary += f"\n📋 NEXT STEPS:\n"
            summary += f"   1. Check the log file: {self.log_file}\n"
            summary += f"   2. Try running the failed steps manually\n"
            summary += f"   3. See README.md for troubleshooting\n"
        else:
            summary += f"\n🎉 ALL STEPS COMPLETED SUCCESSFULLY!\n"
            summary += f"\n📋 NEXT STEPS:\n"
            summary += f"   1. Run: python -m pytest tests/ -v\n"
            summary += f"   2. Check out the test reports in reports/\n"
            summary += f"   3. Read EXECUTION_GUIDE.md for usage instructions\n"
        
        summary += f"\n📁 Log file: {self.log_file}\n"
        
        print(summary)
        self.log("Installation summary printed")
    
    def run(self):
        """Run the complete installation process"""
        self.print_banner()
        
        success_steps = []
        failed_steps = []
        
        # Step 1: System check
        if self.check_system():
            success_steps.append("System requirements check")
        else:
            failed_steps.append("System requirements check")
            self.print_summary(success_steps, failed_steps)
            return False
        
        # Step 2: Check internet
        has_internet = self.check_internet_connection()
        if has_internet:
            success_steps.append("Internet connection check")
        else:
            failed_steps.append("Internet connection check")
        
        # Step 3: Try offline packages if no internet
        if not has_internet:
            if self.install_offline_packages():
                success_steps.append("Offline package installation")
            else:
                failed_steps.append("Offline package installation")
        
        # Step 4: Environment setup
        if self.setup_environment():
            success_steps.append("Environment setup")
        else:
            failed_steps.append("Environment setup")
        
        # Step 5: GitHub setup (optional)
        if self.setup_github():
            success_steps.append("GitHub setup")
        else:
            # GitHub setup failure is not critical
            pass
        
        # Step 6: Verification
        if self.verify_installation():
            success_steps.append("Installation verification")
        else:
            failed_steps.append("Installation verification")
        
        # Print summary
        self.print_summary(success_steps, failed_steps)
        
        # Return success if critical steps passed
        critical_failures = [step for step in failed_steps if step in [
            "System requirements check",
            "Environment setup"
        ]]
        
        return len(critical_failures) == 0

def main():
    """Main entry point"""
    try:
        installer = MasterInstaller()
        success = installer.run()
        
        if success:
            print("\n🎉 Installation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Installation completed with errors.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
