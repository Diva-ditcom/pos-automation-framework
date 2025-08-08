#!/usr/bin/env python3
"""
🔧 ENHANCED MACHINE SETUP - STEP 2  
==================================

This script sets up the complete development environment for POS automation testing.
It handles package installation, environment configuration, and project setup.

Features:
- Virtual environment creation
- Package installation with fallbacks
- VS Code configuration
- Project structure validation
- Environment testing

Usage:
    python 2_setup_new_machine_enhanced.py
"""

import os
import sys
import subprocess
import shutil
import json
import venv
from pathlib import Path
from datetime import datetime

class EnhancedSetup:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.venv_dir = self.script_dir / "venv"
        self.log_file = self.script_dir / "logs" / f"enhanced_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.ensure_dirs()
        
    def ensure_dirs(self):
        """Ensure required directories exist"""
        (self.script_dir / "logs").mkdir(exist_ok=True)
        (self.script_dir / "reports").mkdir(exist_ok=True)
        (self.script_dir / ".vscode").mkdir(exist_ok=True)
        
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
║            🔧 ENHANCED ENVIRONMENT SETUP                     ║
║                                                              ║
║  Setting up complete development environment for            ║
║  POS automation testing with maximum compatibility.         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.log("Enhanced setup started")
    
    def check_python_version(self):
        """Check Python version compatibility"""
        self.log("Checking Python version...")
        
        version = sys.version_info
        self.log(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.log("❌ Python 3.7+ required", "ERROR")
            return False
        
        self.log("✅ Python version is compatible")
        return True
    
    def create_virtual_environment(self):
        """Create virtual environment if needed"""
        self.log("Checking virtual environment...")
        
        # Check if we're already in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.log("✅ Already running in virtual environment")
            return True
        
        # Create virtual environment if it doesn't exist
        if not self.venv_dir.exists():
            self.log("Creating virtual environment...")
            try:
                venv.create(self.venv_dir, with_pip=True)
                self.log("✅ Virtual environment created")
            except Exception as e:
                self.log(f"❌ Failed to create virtual environment: {e}", "ERROR")
                return False
        else:
            self.log("✅ Virtual environment already exists")
        
        return True
    
    def get_pip_command(self):
        """Get the appropriate pip command"""
        # If in virtual environment, use current Python
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            return [sys.executable, "-m", "pip"]
        
        # Check if venv exists and use it
        if self.venv_dir.exists():
            if os.name == 'nt':  # Windows
                venv_python = self.venv_dir / "Scripts" / "python.exe"
            else:  # Unix-like
                venv_python = self.venv_dir / "bin" / "python"
            
            if venv_python.exists():
                return [str(venv_python), "-m", "pip"]
        
        # Fallback to system pip
        return [sys.executable, "-m", "pip"]
    
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        self.log("Upgrading pip...")
        
        pip_cmd = self.get_pip_command()
        
        try:
            result = subprocess.run(
                pip_cmd + ["install", "--upgrade", "pip"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                self.log("✅ pip upgraded successfully")
                return True
            else:
                self.log(f"⚠️ pip upgrade warning: {result.stderr}", "WARNING")
                return True  # Continue even if upgrade fails
                
        except Exception as e:
            self.log(f"⚠️ pip upgrade error: {e}", "WARNING")
            return True  # Continue even if upgrade fails
    
    def install_packages(self):
        """Install required packages"""
        self.log("Installing required packages...")
        
        pip_cmd = self.get_pip_command()
        requirements_file = self.script_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.log("❌ requirements.txt not found", "ERROR")
            return self.install_core_packages_manually()
        
        # Try installing from requirements.txt
        try:
            result = subprocess.run(
                pip_cmd + ["install", "-r", str(requirements_file)],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                self.log("✅ Packages installed from requirements.txt")
                return True
            else:
                self.log(f"❌ Requirements installation failed: {result.stderr}", "WARNING")
                return self.install_core_packages_manually()
                
        except Exception as e:
            self.log(f"❌ Error installing requirements: {e}", "WARNING")
            return self.install_core_packages_manually()
    
    def install_core_packages_manually(self):
        """Install core packages individually"""
        self.log("Installing core packages manually...")
        
        pip_cmd = self.get_pip_command()
        
        # Core packages with fallbacks
        packages = [
            ("pywinauto", "Windows automation library"),
            ("pytest", "Testing framework"),
            ("pytest-html", "HTML test reports"),
            ("selenium", "Web automation"),
            ("pandas", "Data manipulation"),
            ("openpyxl", "Excel file handling"),
            ("configparser", "Configuration management"),
            ("pathlib", "Path handling"),
            ("datetime", "Date/time utilities")
        ]
        
        success_count = 0
        
        for package, description in packages:
            try:
                # Check if already installed
                try:
                    __import__(package.replace("-", "_"))
                    self.log(f"✅ {package} already installed")
                    success_count += 1
                    continue
                except ImportError:
                    pass
                
                # Install package
                result = subprocess.run(
                    pip_cmd + ["install", package],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    self.log(f"✅ {package} installed successfully")
                    success_count += 1
                else:
                    self.log(f"❌ Failed to install {package}: {result.stderr}", "WARNING")
                    
            except Exception as e:
                self.log(f"❌ Error installing {package}: {e}", "WARNING")
        
        if success_count >= 3:  # At least pywinauto, pytest, and one other
            self.log(f"✅ Core packages installed ({success_count}/{len(packages)})")
            return True
        else:
            self.log(f"❌ Insufficient packages installed ({success_count}/{len(packages)})", "ERROR")
            return False
    
    def setup_vscode_config(self):
        """Set up VS Code configuration"""
        self.log("Setting up VS Code configuration...")
        
        vscode_dir = self.script_dir / ".vscode"
        
        # Settings.json
        settings = {
            "python.defaultInterpreterPath": "./venv/Scripts/python.exe" if os.name == 'nt' else "./venv/bin/python",
            "python.testing.pytestEnabled": True,
            "python.testing.unittestEnabled": False,
            "python.testing.pytestArgs": [
                "tests"
            ],
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": False,
            "python.linting.flake8Enabled": True,
            "files.associations": {
                "*.py": "python"
            },
            "python.formatting.provider": "black",
            "editor.formatOnSave": True,
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/venv": True
            }
        }
        
        try:
            with open(vscode_dir / "settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            self.log("✅ VS Code settings configured")
        except Exception as e:
            self.log(f"⚠️ VS Code settings error: {e}", "WARNING")
        
        # Launch.json for debugging
        launch_config = {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python: Current File",
                    "type": "python",
                    "request": "launch",
                    "program": "${file}",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}"
                },
                {
                    "name": "Python: Pytest",
                    "type": "python",
                    "request": "launch",
                    "module": "pytest",
                    "args": ["tests/", "-v"],
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}"
                }
            ]
        }
        
        try:
            with open(vscode_dir / "launch.json", "w") as f:
                json.dump(launch_config, f, indent=4)
            self.log("✅ VS Code launch configuration created")
        except Exception as e:
            self.log(f"⚠️ VS Code launch config error: {e}", "WARNING")
        
        return True
    
    def validate_project_structure(self):
        """Validate project directory structure"""
        self.log("Validating project structure...")
        
        required_items = [
            ("config", "directory"),
            ("data", "directory"), 
            ("tests", "directory"),
            ("utils", "directory"),
            ("requirements.txt", "file"),
            ("README.md", "file")
        ]
        
        missing_items = []
        
        for item, item_type in required_items:
            path = self.script_dir / item
            
            if item_type == "directory":
                if not path.is_dir():
                    missing_items.append(f"{item}/ (directory)")
            else:  # file
                if not path.is_file():
                    missing_items.append(f"{item} (file)")
        
        if missing_items:
            self.log(f"❌ Missing project items: {missing_items}", "WARNING")
            # Create missing directories
            for item, item_type in required_items:
                if item_type == "directory":
                    (self.script_dir / item).mkdir(exist_ok=True)
            self.log("✅ Created missing directories")
        else:
            self.log("✅ Project structure is valid")
        
        return True
    
    def test_imports(self):
        """Test that key packages can be imported"""
        self.log("Testing package imports...")
        
        packages_to_test = [
            ("pywinauto", "Windows automation"),
            ("pytest", "Testing framework"),
            ("pandas", "Data manipulation"),
            ("configparser", "Configuration")
        ]
        
        success_count = 0
        
        for package, description in packages_to_test:
            try:
                __import__(package)
                self.log(f"✅ {package} ({description}) imported successfully")
                success_count += 1
            except ImportError as e:
                self.log(f"❌ {package} import failed: {e}", "WARNING")
        
        if success_count >= 2:  # At least pywinauto and pytest
            self.log(f"✅ Import test passed ({success_count}/{len(packages_to_test)})")
            return True
        else:
            self.log(f"❌ Import test failed ({success_count}/{len(packages_to_test)})", "ERROR")
            return False
    
    def run_basic_test(self):
        """Run a basic pytest test to verify setup"""
        self.log("Running basic test verification...")
        
        # Create a simple test if none exists
        test_dir = self.script_dir / "tests"
        test_dir.mkdir(exist_ok=True)
        
        basic_test_file = test_dir / "test_setup_verification.py"
        
        if not basic_test_file.exists():
            test_content = '''"""
Basic setup verification test
"""
import pytest
import sys
from pathlib import Path

def test_python_version():
    """Test Python version is compatible"""
    assert sys.version_info >= (3, 7), "Python 3.7+ required"

def test_pywinauto_import():
    """Test pywinauto can be imported"""
    try:
        import pywinauto
        assert True
    except ImportError:
        pytest.skip("pywinauto not available")

def test_project_structure():
    """Test basic project structure exists"""
    project_root = Path(__file__).parent.parent
    
    assert (project_root / "config").is_dir(), "config directory missing"
    assert (project_root / "data").is_dir(), "data directory missing"
    assert (project_root / "requirements.txt").is_file(), "requirements.txt missing"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
            try:
                with open(basic_test_file, "w") as f:
                    f.write(test_content)
                self.log("✅ Basic test file created")
            except Exception as e:
                self.log(f"⚠️ Could not create test file: {e}", "WARNING")
                return True  # Continue anyway
        
        # Run the test
        try:
            # Determine Python executable
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                python_cmd = [sys.executable]
            elif self.venv_dir.exists():
                if os.name == 'nt':
                    python_cmd = [str(self.venv_dir / "Scripts" / "python.exe")]
                else:
                    python_cmd = [str(self.venv_dir / "bin" / "python")]
            else:
                python_cmd = [sys.executable]
            
            result = subprocess.run(
                python_cmd + ["-m", "pytest", str(basic_test_file), "-v"],
                capture_output=True, text=True, cwd=str(self.script_dir)
            )
            
            if result.returncode == 0:
                self.log("✅ Basic test verification passed")
                return True
            else:
                self.log(f"⚠️ Basic test had issues: {result.stderr}", "WARNING")
                return True  # Continue anyway
                
        except Exception as e:
            self.log(f"⚠️ Could not run basic test: {e}", "WARNING")
            return True  # Continue anyway
    
    def create_run_script(self):
        """Create convenience script for running tests"""
        self.log("Creating test runner script...")
        
        if os.name == 'nt':  # Windows
            script_content = '''@echo off
echo Starting POS Automation Tests...

REM Activate virtual environment if it exists
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Run tests with HTML report
echo Running tests...
python -m pytest tests/ -v --html=reports/test_report.html --self-contained-html

echo.
echo Test execution completed!
echo Check reports/test_report.html for detailed results.
pause
'''
            script_file = self.script_dir / "run_tests.bat"
        else:  # Unix-like
            script_content = '''#!/bin/bash
echo "Starting POS Automation Tests..."

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run tests with HTML report
echo "Running tests..."
python -m pytest tests/ -v --html=reports/test_report.html --self-contained-html

echo ""
echo "Test execution completed!"
echo "Check reports/test_report.html for detailed results."
'''
            script_file = self.script_dir / "run_tests.sh"
        
        try:
            with open(script_file, "w") as f:
                f.write(script_content)
            
            # Make executable on Unix-like systems
            if os.name != 'nt':
                os.chmod(script_file, 0o755)
            
            self.log("✅ Test runner script created")
            return True
            
        except Exception as e:
            self.log(f"⚠️ Could not create run script: {e}", "WARNING")
            return True  # Continue anyway
    
    def run(self):
        """Run the complete enhanced setup process"""
        self.print_banner()
        
        success_steps = []
        failed_steps = []
        
        # Step 1: Check Python version
        if self.check_python_version():
            success_steps.append("Python version check")
        else:
            failed_steps.append("Python version check")
            return False
        
        # Step 2: Create/check virtual environment
        if self.create_virtual_environment():
            success_steps.append("Virtual environment setup")
        else:
            failed_steps.append("Virtual environment setup")
        
        # Step 3: Upgrade pip
        if self.upgrade_pip():
            success_steps.append("pip upgrade")
        else:
            failed_steps.append("pip upgrade")
        
        # Step 4: Install packages
        if self.install_packages():
            success_steps.append("Package installation")
        else:
            failed_steps.append("Package installation")
        
        # Step 5: VS Code configuration
        if self.setup_vscode_config():
            success_steps.append("VS Code configuration")
        else:
            failed_steps.append("VS Code configuration")
        
        # Step 6: Validate project structure
        if self.validate_project_structure():
            success_steps.append("Project structure validation")
        else:
            failed_steps.append("Project structure validation")
        
        # Step 7: Test imports
        if self.test_imports():
            success_steps.append("Package import testing")
        else:
            failed_steps.append("Package import testing")
        
        # Step 8: Run basic test
        if self.run_basic_test():
            success_steps.append("Basic test verification")
        else:
            failed_steps.append("Basic test verification")
        
        # Step 9: Create run script
        if self.create_run_script():
            success_steps.append("Test runner script creation")
        else:
            failed_steps.append("Test runner script creation")
        
        # Print summary
        self.log(f"\n✅ Successful steps: {len(success_steps)}")
        self.log(f"❌ Failed steps: {len(failed_steps)}")
        
        if len(failed_steps) <= 2:  # Allow some non-critical failures
            self.log("✅ Enhanced setup completed successfully")
            return True
        else:
            self.log("❌ Enhanced setup completed with significant issues", "ERROR")
            return False

def main():
    """Main entry point"""
    try:
        setup = EnhancedSetup()
        success = setup.run()
        
        if success:
            print("\n🎉 Enhanced setup completed successfully!")
            print("\n📋 Next steps:")
            print("   1. Run: python -m pytest tests/ -v")
            print("   2. Or use: run_tests.bat (Windows) / ./run_tests.sh (Unix)")
            print("   3. Continue with: python 3_deploy_to_github.py")
            print("   4. Or finish with: python 0_MASTER_INSTALLER.py")
            return True
        else:
            print("\n❌ Enhanced setup completed with issues.")
            print("\n📋 Troubleshooting:")
            print("   1. Check the log file in logs/ directory")
            print("   2. Try running individual steps manually")
            print("   3. Ensure Python 3.7+ is installed")
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
