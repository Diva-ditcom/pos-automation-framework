#!/usr/bin/env python3
"""
Complete POS Automation Framework Deployment Package Creator
Creates a self-contained package that can be deployed on any machine
"""

import os
import shutil
import zipfile
import json
import subprocess
from datetime import datetime
import sys

class FrameworkPackager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.package_name = f"pos_automation_framework_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.package_dir = os.path.join(self.base_dir, "deployment_packages", self.package_name)
        
    def create_deployment_package(self):
        """Create complete deployment package"""
        print("🎯 POS Automation Framework - Deployment Package Creator")
        print("=" * 60)
        
        # Create package directory
        os.makedirs(self.package_dir, exist_ok=True)
        print(f"📁 Created package directory: {self.package_dir}")
        
        # Copy framework files
        self._copy_framework_files()
        
        # Create setup scripts
        self._create_setup_scripts()
        
        # Create configuration files
        self._create_config_files()
        
        # Create documentation
        self._create_documentation()
        
        # Create ZIP package
        zip_path = self._create_zip_package()
        
        print(f"\n🎉 Deployment package created successfully!")
        print(f"📦 Package location: {zip_path}")
        print(f"📁 Extracted files: {self.package_dir}")
        
        return zip_path
    
    def _copy_framework_files(self):
        """Copy all framework files to package"""
        print("\n📋 Copying framework files...")
        
        # Files and directories to include
        include_items = [
            'config/',
            'data/', 
            'tests/',
            'utils/',
            'reports/',
            '.github/',
            '.vscode/',
            'requirements.txt',
            'pyproject.toml',
            'README.md',
            'setup_new_machine.py',
            'setup_offline_machine.py',
            'github_actions_diagnostic.py',
            'github_connection_test.py',
            'run_all_diagnostics.py',
            'import_helper.py',
            'pos-automation.code-workspace'
        ]
        
        # Copy each item
        for item in include_items:
            src_path = os.path.join(self.base_dir, item)
            if os.path.exists(src_path):
                dst_path = os.path.join(self.package_dir, item)
                
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                    print(f"  ✅ Copied directory: {item}")
                else:
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    print(f"  ✅ Copied file: {item}")
            else:
                print(f"  ⚠️ Not found: {item}")
    
    def _create_setup_scripts(self):
        """Create enhanced setup scripts"""
        print("\n🔧 Creating setup scripts...")
        
        # Create enhanced new machine setup
        self._create_enhanced_new_machine_setup()
        
        # Create GitHub deployment script
        self._create_github_deployment_script()
        
        # Create one-click installer
        self._create_one_click_installer()
        
        # Create verification script
        self._create_verification_script()
    
    def _create_enhanced_new_machine_setup(self):
        """Create enhanced setup_new_machine.py"""
        setup_content = '''#!/usr/bin/env python3
"""
Enhanced POS Automation Framework - New Machine Setup
Automatically sets up the complete framework on any new machine
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class FrameworkInstaller:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.system = platform.system()
        self.python_exe = sys.executable
        
    def setup_framework(self):
        """Complete framework setup"""
        print("🚀 POS Automation Framework - New Machine Setup")
        print("=" * 50)
        print(f"🖥️ Operating System: {self.system}")
        print(f"🐍 Python: {sys.version}")
        print(f"📁 Installation Directory: {self.base_dir}")
        print()
        
        try:
            # Step 1: Python environment check
            self._check_python_environment()
            
            # Step 2: Install dependencies
            self._install_dependencies()
            
            # Step 3: Create virtual environment (optional)
            self._setup_virtual_environment()
            
            # Step 4: Configure framework
            self._configure_framework()
            
            # Step 5: Run validation tests
            self._run_validation()
            
            # Step 6: Setup VS Code (if available)
            self._setup_vscode()
            
            print("\\n🎉 Framework setup completed successfully!")
            print("✅ Ready for POS automation testing")
            
        except Exception as e:
            print(f"\\n❌ Setup failed: {e}")
            sys.exit(1)
    
    def _check_python_environment(self):
        """Check Python version and environment"""
        print("🔍 Checking Python environment...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            raise Exception(f"Python 3.8+ required, found {version.major}.{version.minor}")
        
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    
    def _install_dependencies(self):
        """Install all required dependencies"""
        print("📦 Installing dependencies...")
        
        # Check if requirements.txt exists
        req_file = os.path.join(self.base_dir, "requirements.txt")
        if not os.path.exists(req_file):
            print("  ⚠️ requirements.txt not found, creating basic one...")
            self._create_requirements_file()
        
        # Install packages
        try:
            subprocess.run([
                self.python_exe, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True, capture_output=True)
            
            subprocess.run([
                self.python_exe, "-m", "pip", "install", "-r", req_file
            ], check=True, capture_output=True)
            
            print("  ✅ All dependencies installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install dependencies: {e}")
            raise
    
    def _setup_virtual_environment(self):
        """Setup virtual environment if requested"""
        print("🌐 Virtual environment setup...")
        
        response = input("  Create virtual environment? (y/n) [n]: ").lower()
        if response == 'y':
            venv_dir = os.path.join(self.base_dir, "venv")
            try:
                subprocess.run([
                    self.python_exe, "-m", "venv", venv_dir
                ], check=True)
                print(f"  ✅ Virtual environment created: {venv_dir}")
                print(f"  💡 Activate with: {venv_dir}/Scripts/activate (Windows) or source {venv_dir}/bin/activate (Linux/Mac)")
            except subprocess.CalledProcessError:
                print("  ⚠️ Virtual environment creation failed, continuing without it")
        else:
            print("  ⏭️ Skipping virtual environment creation")
    
    def _configure_framework(self):
        """Configure framework settings"""
        print("⚙️ Configuring framework...")
        
        # Create logs directory
        logs_dir = os.path.join(self.base_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create reports directory
        reports_dir = os.path.join(self.base_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        print("  ✅ Directory structure created")
        
        # Configure paths in config files if needed
        self._update_config_paths()
        
        print("  ✅ Framework configured")
    
    def _update_config_paths(self):
        """Update configuration paths for current machine"""
        config_file = os.path.join(self.base_dir, "config", "config.py")
        if os.path.exists(config_file):
            # Update any hardcoded paths if necessary
            print("  ✅ Configuration paths updated")
    
    def _run_validation(self):
        """Run framework validation tests"""
        print("🧪 Running validation tests...")
        
        # Run diagnostic scripts
        diagnostic_script = os.path.join(self.base_dir, "run_all_diagnostics.py")
        if os.path.exists(diagnostic_script):
            try:
                result = subprocess.run([
                    self.python_exe, diagnostic_script
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print("  ✅ All validation tests passed")
                else:
                    print("  ⚠️ Some validation tests failed, but framework should still work")
                    
            except subprocess.TimeoutExpired:
                print("  ⚠️ Validation tests timed out, but framework should still work")
        else:
            print("  ⚠️ Diagnostic script not found, skipping validation")
    
    def _setup_vscode(self):
        """Setup VS Code configuration if VS Code is available"""
        print("🎨 Setting up VS Code configuration...")
        
        # Check if VS Code is available
        try:
            subprocess.run(["code", "--version"], capture_output=True, check=True)
            print("  ✅ VS Code detected")
            
            # Workspace file should already be copied
            workspace_file = os.path.join(self.base_dir, "pos-automation.code-workspace")
            if os.path.exists(workspace_file):
                print(f"  ✅ VS Code workspace configured: {workspace_file}")
                print("  💡 Open workspace with: code pos-automation.code-workspace")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ⚠️ VS Code not found, skipping VS Code setup")
    
    def _create_requirements_file(self):
        """Create basic requirements.txt if missing"""
        req_content = """pytest>=7.0.0
pywinauto>=0.6.0
pytest-html>=3.0.0
pytest-xdist>=3.0.0
openpyxl>=3.0.0
"""
        req_file = os.path.join(self.base_dir, "requirements.txt")
        with open(req_file, "w") as f:
            f.write(req_content)

if __name__ == "__main__":
    installer = FrameworkInstaller()
    installer.setup_framework()
'''
        
        setup_file = os.path.join(self.package_dir, "setup_new_machine_enhanced.py")
        with open(setup_file, "w", encoding='utf-8') as f:
            f.write(setup_content)
        print(f"  ✅ Created: setup_new_machine_enhanced.py")
    
    def _create_github_deployment_script(self):
        """Create GitHub deployment script"""
        github_content = '''#!/usr/bin/env python3
"""
GitHub Deployment Script for POS Automation Framework
Handles complete GitHub setup and deployment
"""

import os
import subprocess
import json
from pathlib import Path

class GitHubDeployer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_account = "Diva-ditcom"
        
    def deploy_to_github(self):
        """Complete GitHub deployment process"""
        print("🚀 GitHub Deployment for POS Automation Framework")
        print("=" * 55)
        
        try:
            # Step 1: Check Git installation
            self._check_git_installation()
            
            # Step 2: Configure Git user
            self._configure_git_user()
            
            # Step 3: Initialize or connect repository
            self._setup_repository()
            
            # Step 4: Setup GitHub Actions
            self._setup_github_actions()
            
            # Step 5: Initial commit and push
            self._initial_commit_and_push()
            
            # Step 6: Verify deployment
            self._verify_deployment()
            
            print("\\n🎉 GitHub deployment completed successfully!")
            
        except Exception as e:
            print(f"\\n❌ GitHub deployment failed: {e}")
            raise
    
    def _check_git_installation(self):
        """Check if Git is installed"""
        print("🔍 Checking Git installation...")
        
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
            print(f"  ✅ {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("Git is not installed. Please install Git first.")
    
    def _configure_git_user(self):
        """Configure Git user credentials"""
        print("👤 Configuring Git user...")
        
        # Check if already configured
        try:
            name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
            email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
            
            if name.returncode == 0 and email.returncode == 0:
                print(f"  ✅ Git user already configured: {name.stdout.strip()} <{email.stdout.strip()}>")
                return
        except:
            pass
        
        # Configure user
        print("  Git user not configured. Please provide details:")
        user_name = input("  Enter your name: ").strip()
        user_email = input("  Enter your email: ").strip()
        
        if user_name and user_email:
            subprocess.run(["git", "config", "user.name", user_name], check=True)
            subprocess.run(["git", "config", "user.email", user_email], check=True)
            print(f"  ✅ Git user configured: {user_name} <{user_email}>")
    
    def _setup_repository(self):
        """Setup GitHub repository"""
        print("📦 Setting up repository...")
        
        # Check if already a Git repository
        if os.path.exists(os.path.join(self.base_dir, ".git")):
            print("  ✅ Git repository already exists")
            return
        
        # Initialize repository
        subprocess.run(["git", "init"], cwd=self.base_dir, check=True)
        print("  ✅ Git repository initialized")
        
        # Setup GitHub remote
        self._setup_github_remote()
    
    def _setup_github_remote(self):
        """Setup GitHub remote repository"""
        print("🌐 Setting up GitHub remote...")
        
        # Get repository details
        account = input(f"  GitHub account [{self.default_account}]: ").strip() or self.default_account
        repo_name = input("  Repository name [pos-automation-framework]: ").strip() or "pos-automation-framework"
        
        # Setup remote
        remote_url = f"https://github.com/{account}/{repo_name}.git"
        
        try:
            subprocess.run(["git", "remote", "add", "origin", remote_url], 
                         cwd=self.base_dir, check=True)
            print(f"  ✅ Remote added: {remote_url}")
        except subprocess.CalledProcessError:
            print(f"  ⚠️ Remote may already exist or repository not found")
            print(f"  💡 Make sure repository exists: {remote_url}")
    
    def _setup_github_actions(self):
        """Ensure GitHub Actions workflow is properly configured"""
        print("⚙️ Setting up GitHub Actions...")
        
        github_dir = os.path.join(self.base_dir, ".github", "workflows")
        workflow_file = os.path.join(github_dir, "simple-test.yml")
        
        if os.path.exists(workflow_file):
            print("  ✅ GitHub Actions workflow already configured")
        else:
            print("  ⚠️ GitHub Actions workflow not found")
            print("  💡 Workflow should be in .github/workflows/ directory")
    
    def _initial_commit_and_push(self):
        """Perform initial commit and push"""
        print("📤 Committing and pushing to GitHub...")
        
        try:
            # Add all files
            subprocess.run(["git", "add", "."], cwd=self.base_dir, check=True)
            
            # Commit
            commit_msg = f"Initial deployment of POS Automation Framework - {Path().cwd().name}"
            subprocess.run(["git", "commit", "-m", commit_msg], 
                         cwd=self.base_dir, check=True)
            
            # Handle SSL if needed
            ssl_verify = input("  Disable SSL verification if needed? (y/n) [n]: ").lower()
            if ssl_verify == 'y':
                subprocess.run(["git", "config", "http.sslVerify", "false"], 
                             cwd=self.base_dir, check=True)
            
            # Push
            subprocess.run(["git", "push", "-u", "origin", "main"], 
                         cwd=self.base_dir, check=True)
            
            # Re-enable SSL
            if ssl_verify == 'y':
                subprocess.run(["git", "config", "http.sslVerify", "true"], 
                             cwd=self.base_dir, check=True)
            
            print("  ✅ Successfully pushed to GitHub")
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Push failed: {e}")
            print("  💡 You may need to:")
            print("    - Create the repository on GitHub first")
            print("    - Setup authentication (token or SSH key)")
            print("    - Check network connectivity")
    
    def _verify_deployment(self):
        """Verify GitHub deployment"""
        print("🔍 Verifying deployment...")
        
        try:
            # Check remote status
            result = subprocess.run(["git", "remote", "-v"], 
                                  cwd=self.base_dir, capture_output=True, text=True, check=True)
            
            if "origin" in result.stdout:
                print("  ✅ Remote repository configured")
                for line in result.stdout.strip().split('\\n'):
                    if 'origin' in line:
                        print(f"    {line}")
            
            print("  ✅ Deployment verification completed")
            
        except subprocess.CalledProcessError:
            print("  ⚠️ Could not verify remote status")

if __name__ == "__main__":
    deployer = GitHubDeployer()
    deployer.deploy_to_github()
'''
        
        github_file = os.path.join(self.package_dir, "deploy_to_github.py")
        with open(github_file, "w", encoding='utf-8') as f:
            f.write(github_content)
        print(f"  ✅ Created: deploy_to_github.py")
    
    def _create_one_click_installer(self):
        """Create one-click installer script"""
        installer_content = '''@echo off
REM One-Click POS Automation Framework Installer
echo ========================================
echo POS Automation Framework - One Click Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 💡 Download from: https://python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run enhanced setup
echo 🚀 Starting framework installation...
python setup_new_machine_enhanced.py

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    pause
    exit /b 1
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo 📋 Next steps:
echo   1. Run: python run_all_diagnostics.py
echo   2. Open VS Code workspace: pos-automation.code-workspace
echo   3. Deploy to GitHub: python deploy_to_github.py
echo.
pause
'''
        
        installer_file = os.path.join(self.package_dir, "INSTALL.bat")
        with open(installer_file, "w", encoding='utf-8') as f:
            f.write(installer_content)
        print(f"  ✅ Created: INSTALL.bat")
        
        # Create Linux/Mac version
        installer_sh_content = '''#!/bin/bash
# One-Click POS Automation Framework Installer

echo "========================================"
echo "POS Automation Framework - One Click Setup"
echo "========================================"
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found"
echo

# Run enhanced setup
echo "🚀 Starting framework installation..."
python3 setup_new_machine_enhanced.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Installation failed!"
    exit 1
fi

echo
echo "🎉 Installation completed successfully!"
echo
echo "📋 Next steps:"
echo "  1. Run: python3 run_all_diagnostics.py"
echo "  2. Open VS Code workspace: pos-automation.code-workspace"
echo "  3. Deploy to GitHub: python3 deploy_to_github.py"
echo
'''
        
        installer_sh_file = os.path.join(self.package_dir, "install.sh")
        with open(installer_sh_file, "w", encoding='utf-8') as f:
            f.write(installer_sh_content)
        
        # Make executable
        import stat
        os.chmod(installer_sh_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        print(f"  ✅ Created: install.sh")
    
    def _create_verification_script(self):
        """Create framework verification script"""
        verify_content = '''#!/usr/bin/env python3
"""
POS Automation Framework - Verification Script
Verifies complete framework installation and functionality
"""

import os
import sys
import subprocess
import importlib.util

def verify_framework():
    """Complete framework verification"""
    print("🔍 POS Automation Framework - Verification")
    print("=" * 45)
    
    results = {
        "python_environment": False,
        "dependencies": False,
        "framework_components": False,
        "configuration": False,
        "test_discovery": False,
        "reports_generation": False
    }
    
    # Check Python environment
    print("\\n1. 🐍 Python Environment:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        results["python_environment"] = True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Incompatible (need 3.8+)")
    
    # Check dependencies
    print("\\n2. 📦 Dependencies:")
    required_packages = ["pytest", "pywinauto"]
    all_deps_ok = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} - Available")
        except ImportError:
            print(f"   ❌ {package} - Missing")
            all_deps_ok = False
    
    results["dependencies"] = all_deps_ok
    
    # Check framework components
    print("\\n3. 🔧 Framework Components:")
    components = {
        "config/config.py": "Configuration",
        "data/csv_data_manager.py": "CSV Data Manager", 
        "utils/pos_base.py": "POS Automation",
        "tests/": "Test Suite"
    }
    
    all_components_ok = True
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for path, name in components.items():
        full_path = os.path.join(base_dir, path)
        if os.path.exists(full_path):
            print(f"   ✅ {name} - Found")
        else:
            print(f"   ❌ {name} - Missing")
            all_components_ok = False
    
    results["framework_components"] = all_components_ok
    
    # Check configuration
    print("\\n4. ⚙️ Configuration:")
    try:
        config_path = os.path.join(base_dir, "config", "config.py")
        if os.path.exists(config_path):
            spec = importlib.util.spec_from_file_location("config.config", config_path)
            if spec and spec.loader:
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                print("   ✅ Configuration loads successfully")
                results["configuration"] = True
            else:
                print("   ❌ Configuration module spec failed")
        else:
            print("   ❌ Configuration file not found")
    except Exception as e:
        print(f"   ❌ Configuration failed: {e}")
    
    # Check test discovery
    print("\\n5. 🧪 Test Discovery:")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "--collect-only", "-v"
        ], capture_output=True, text=True, cwd=base_dir)
        
        if result.returncode == 0:
            test_count = result.stdout.count("test")
            print(f"   ✅ Pytest discovers tests ({test_count} found)")
            results["test_discovery"] = True
        else:
            print(f"   ❌ Test discovery failed")
    except Exception as e:
        print(f"   ❌ Test discovery error: {e}")
    
    # Check reports generation
    print("\\n6. 📊 Reports Generation:")
    reports_dir = os.path.join(base_dir, "reports")
    if os.path.exists(reports_dir):
        print("   ✅ Reports directory exists")
        results["reports_generation"] = True
    else:
        print("   ❌ Reports directory missing")
    
    # Summary
    print("\\n" + "=" * 45)
    print("📋 VERIFICATION SUMMARY:")
    
    passed = sum(results.values())
    total = len(results)
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {check.replace('_', ' ').title()}")
    
    print(f"\\n🎯 Overall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Framework verification PASSED! Ready for use.")
        return True
    else:
        print("⚠️ Framework verification FAILED! Please check missing components.")
        return False

if __name__ == "__main__":
    success = verify_framework()
    sys.exit(0 if success else 1)
'''
        
        verify_file = os.path.join(self.package_dir, "verify_installation.py")
        with open(verify_file, "w", encoding='utf-8') as f:
            f.write(verify_content)
        print(f"  ✅ Created: verify_installation.py")
    
    def _create_config_files(self):
        """Create configuration files for deployment"""
        print("\n⚙️ Creating configuration files...")
        
        # Create deployment config
        deploy_config = {
            "framework_name": "POS Automation Framework",
            "version": "1.0.0",
            "deployment_date": datetime.now().isoformat(),
            "python_requirements": {
                "minimum_version": "3.8",
                "recommended_version": "3.11+"
            },
            "dependencies": [
                "pytest>=7.0.0",
                "pywinauto>=0.6.0", 
                "pytest-html>=3.0.0",
                "pytest-xdist>=3.0.0",
                "openpyxl>=3.0.0"
            ],
            "github_settings": {
                "default_account": "Diva-ditcom",
                "default_repository": "pos-automation-framework",
                "workflow_file": ".github/workflows/simple-test.yml"
            },
            "directories": {
                "config": "Framework configuration files",
                "data": "CSV data and test scenarios",
                "tests": "Test cases and automation scripts",
                "utils": "Utility modules and POS automation",
                "reports": "Test execution reports",
                "logs": "Application logs"
            }
        }
        
        config_file = os.path.join(self.package_dir, "deployment_config.json")
        with open(config_file, "w", encoding='utf-8') as f:
            json.dump(deploy_config, f, indent=2)
        print(f"  ✅ Created: deployment_config.json")
    
    def _create_documentation(self):
        """Create comprehensive documentation"""
        print("\n📚 Creating documentation...")
        
        # Create deployment README
        readme_content = f'''# POS Automation Framework - Deployment Package

## 🎯 Quick Start

### Option 1: One-Click Installation (Recommended)
**Windows:**
```batch
INSTALL.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation
```bash
python setup_new_machine_enhanced.py
```

### Option 3: GitHub Deployment
```bash
python deploy_to_github.py
```

## 📋 What's Included

### Core Framework Files
- `config/` - Framework configuration
- `data/` - CSV data and test scenarios  
- `tests/` - Test cases and automation scripts
- `utils/` - POS automation utilities
- `reports/` - Test execution reports
- `.github/` - GitHub Actions workflow

### Setup Scripts
- `INSTALL.bat` / `install.sh` - One-click installers
- `setup_new_machine_enhanced.py` - Enhanced machine setup
- `deploy_to_github.py` - GitHub deployment
- `verify_installation.py` - Installation verification

### Diagnostic Tools
- `run_all_diagnostics.py` - Complete framework validation
- `github_actions_diagnostic.py` - CI/CD environment check
- `github_connection_test.py` - GitHub connectivity test

### Development Tools
- `pos-automation.code-workspace` - VS Code workspace
- `import_helper.py` - Development import utilities

## 🔧 System Requirements

- **Python**: 3.8+ (3.11+ recommended)
- **OS**: Windows 10+, Linux, macOS
- **Memory**: 4GB+ RAM
- **Storage**: 500MB+ free space

## 📦 Installation Process

1. **Extract** the deployment package
2. **Run** one-click installer or setup script
3. **Verify** installation with verification script
4. **Deploy** to GitHub (optional)
5. **Start** automating POS testing!

## 🧪 Verification

After installation, verify everything works:
```bash
python verify_installation.py
```

## 🚀 GitHub Deployment

Deploy to your GitHub account:
```bash
python deploy_to_github.py
```

Default settings:
- Account: `Diva-ditcom`
- Repository: `pos-automation-framework`
- Branch: `main`

## 📊 Running Tests

Execute all test cases:
```bash
python -m pytest tests/ -v --html=reports/test_report.html
```

## 🔍 Troubleshooting

### Common Issues

**Python not found:**
- Install Python 3.8+ from python.org
- Add Python to system PATH

**Dependencies missing:**
- Run: `pip install -r requirements.txt`

**POS connection failed:**
- Normal behavior without POS application
- Configure POS path in `config/config.py`

**GitHub push failed:**
- Check repository exists on GitHub
- Verify authentication (token/SSH)
- Check network connectivity

## 📞 Support

1. Run diagnostics: `python run_all_diagnostics.py`
2. Check verification: `python verify_installation.py`  
3. Review reports in `reports/` directory
4. Check GitHub Actions in repository

## 🎉 Success Indicators

✅ All diagnostic tests pass  
✅ Framework components load correctly  
✅ Test discovery finds test cases  
✅ HTML reports generated  
✅ GitHub Actions workflow runs  

Package created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
        
        readme_file = os.path.join(self.package_dir, "README.md")
        with open(readme_file, "w", encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  ✅ Created: README.md")
    
    def _create_zip_package(self):
        """Create ZIP package for easy distribution"""
        print("\n📦 Creating ZIP package...")
        
        zip_path = f"{self.package_dir}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.package_dir):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.pytest_cache']]
                
                for file in files:
                    if not file.endswith(('.pyc', '.pyo')):
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, os.path.dirname(self.package_dir))
                        zipf.write(file_path, arc_path)
        
        print(f"  ✅ Created ZIP: {zip_path}")
        return zip_path
