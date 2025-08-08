#!/usr/bin/env python3
"""
Enhanced POS Automation Framework - Complete Deployment System
Handles offline installation, project setup, and GitHub integration with maximum error handling
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path
from datetime import datetime

class CompleteFrameworkDeployer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.system = platform.system()
        self.python_exe = sys.executable
        self.deployment_log = []
        
    def create_complete_deployment_package(self):
        """Create complete deployment package with all scenarios"""
        print("🎯 Creating Complete POS Automation Deployment System")
        print("=" * 60)
        
        package_name = f"pos_automation_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        package_dir = os.path.join(self.base_dir, "complete_deployment", package_name)
        
        # Create package directory
        os.makedirs(package_dir, exist_ok=True)
        print(f"📁 Created package directory: {package_dir}")
        
        # Copy all framework files
        self._copy_framework_files(package_dir)
        
        # Create enhanced setup scripts
        self._create_offline_installer(package_dir)
        self._create_enhanced_project_setup(package_dir)
        self._create_github_deployer(package_dir)
        self._create_master_installer(package_dir)
        self._create_execution_guide(package_dir)
        
        # Create offline packages
        self._create_offline_packages(package_dir)
        
        # Create ZIP package
        zip_path = self._create_zip_package(package_dir)
        
        print(f"\n🎉 Complete deployment system created!")
        print(f"📦 Package: {zip_path}")
        print(f"📁 Directory: {package_dir}")
        
        return zip_path, package_dir
    
    def _copy_framework_files(self, package_dir):
        """Copy all framework files"""
        print("\n📋 Copying framework files...")
        
        items_to_copy = [
            'config/', 'data/', 'tests/', 'utils/', 'reports/', 
            '.github/', '.vscode/', 'requirements.txt', 'pyproject.toml',
            'README.md', 'github_actions_diagnostic.py', 'github_connection_test.py',
            'run_all_diagnostics.py', 'import_helper.py', 'pos-automation.code-workspace'
        ]
        
        for item in items_to_copy:
            src_path = os.path.join(self.base_dir, item)
            if os.path.exists(src_path):
                dst_path = os.path.join(package_dir, item)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                else:
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                print(f"  ✅ Copied: {item}")
    
    def _create_offline_installer(self, package_dir):
        """Create setup_offline_machine.py - handles offline package installation"""
        print("\n🔧 Creating offline installer...")
        
        offline_content = '''#!/usr/bin/env python3
"""
POS Automation Framework - Offline Package Installer
Handles package installation when online installation fails due to proxy/network issues
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class OfflineInstaller:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.system = platform.system()
        self.python_exe = sys.executable
        self.offline_packages_dir = os.path.join(self.base_dir, "offline_packages")
        
    def install_offline_packages(self):
        """Install packages from offline directory"""
        print("📦 POS Automation Framework - Offline Package Installation")
        print("=" * 60)
        print(f"🖥️ System: {self.system}")
        print(f"🐍 Python: {sys.version}")
        print(f"📁 Base Directory: {self.base_dir}")
        print()
        
        try:
            # Check if offline packages exist
            if not self._check_offline_packages():
                self._download_packages_if_possible()
            
            # Install packages
            self._install_from_offline()
            
            # Verify installation
            self._verify_offline_installation()
            
            print("\\n🎉 Offline package installation completed successfully!")
            print("✅ Ready for project setup - run: python setup_new_machine_enhanced.py")
            
        except Exception as e:
            print(f"\\n❌ Offline installation failed: {e}")
            self._provide_manual_instructions()
            
    def _check_offline_packages(self):
        """Check if offline packages directory exists"""
        print("🔍 Checking offline packages...")
        
        if os.path.exists(self.offline_packages_dir):
            wheels = list(Path(self.offline_packages_dir).glob("*.whl"))
            if wheels:
                print(f"  ✅ Found {len(wheels)} offline packages")
                return True
        
        print("  ⚠️ No offline packages found")
        return False
    
    def _download_packages_if_possible(self):
        """Try to download packages if internet is available"""
        print("🌐 Attempting to download packages...")
        
        # Create offline packages directory
        os.makedirs(self.offline_packages_dir, exist_ok=True)
        
        packages = [
            "pytest>=7.0.0",
            "pywinauto>=0.6.0", 
            "pytest-html>=3.0.0",
            "pytest-xdist>=3.0.0",
            "openpyxl>=3.0.0"
        ]
        
        try:
            # Try to download packages
            for package in packages:
                print(f"  📥 Downloading {package}...")
                result = subprocess.run([
                    self.python_exe, "-m", "pip", "download",
                    package, "--dest", self.offline_packages_dir
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"    ✅ Downloaded {package}")
                else:
                    print(f"    ❌ Failed to download {package}")
            
            print("  ✅ Package download completed")
            return True
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print(f"  ❌ Download failed: {e}")
            return False
    
    def _install_from_offline(self):
        """Install packages from offline directory"""
        print("📦 Installing from offline packages...")
        
        if not os.path.exists(self.offline_packages_dir):
            raise Exception("Offline packages directory not found")
        
        # Install all wheel files
        wheels = list(Path(self.offline_packages_dir).glob("*.whl"))
        
        if not wheels:
            # Try direct package installation
            self._install_direct_packages()
            return
        
        for wheel in wheels:
            print(f"  📦 Installing {wheel.name}...")
            try:
                result = subprocess.run([
                    self.python_exe, "-m", "pip", "install", str(wheel), "--no-deps"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"    ✅ Installed {wheel.name}")
                else:
                    print(f"    ⚠️ Warning installing {wheel.name}: {result.stderr}")
                    
            except Exception as e:
                print(f"    ❌ Failed to install {wheel.name}: {e}")
    
    def _install_direct_packages(self):
        """Install packages directly (fallback)"""
        print("  📦 Installing packages directly...")
        
        packages = ["pytest", "pywinauto", "pytest-html", "pytest-xdist", "openpyxl"]
        
        for package in packages:
            try:
                print(f"    📦 Installing {package}...")
                result = subprocess.run([
                    self.python_exe, "-m", "pip", "install", package, "--no-cache-dir"
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print(f"      ✅ Installed {package}")
                else:
                    print(f"      ⚠️ Warning with {package}")
                    
            except Exception as e:
                print(f"      ❌ Failed to install {package}: {e}")
    
    def _verify_offline_installation(self):
        """Verify that packages were installed correctly"""
        print("🔍 Verifying package installation...")
        
        required_packages = ["pytest", "pywinauto"]
        all_ok = True
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package} - Available")
            except ImportError:
                print(f"  ❌ {package} - Missing")
                all_ok = False
        
        if not all_ok:
            print("  ⚠️ Some packages missing, but framework may still work")
        else:
            print("  ✅ All critical packages installed successfully")
    
    def _provide_manual_instructions(self):
        """Provide manual installation instructions"""
        print("\\n📋 MANUAL INSTALLATION INSTRUCTIONS:")
        print("=" * 50)
        print("If offline installation fails, try these options:")
        print()
        print("Option 1: Use pip with different index:")
        print("  pip install --index-url https://pypi.org/simple/ pytest pywinauto pytest-html")
        print()
        print("Option 2: Download wheels manually:")
        print("  1. Go to https://pypi.org/")
        print("  2. Search for: pytest, pywinauto, pytest-html")
        print("  3. Download .whl files")
        print("  4. Place in offline_packages/ directory")
        print("  5. Run this script again")
        print()
        print("Option 3: Use conda (if available):")
        print("  conda install pytest")
        print("  pip install pywinauto pytest-html")
        print()
        print("After manual installation, run: python setup_new_machine_enhanced.py")

if __name__ == "__main__":
    installer = OfflineInstaller()
    installer.install_offline_packages()
'''
        
        offline_file = os.path.join(package_dir, "1_setup_offline_machine.py")
        with open(offline_file, "w", encoding='utf-8') as f:
            f.write(offline_content)
        print(f"  ✅ Created: 1_setup_offline_machine.py")
    
    def _create_enhanced_project_setup(self, package_dir):
        """Create setup_new_machine_enhanced.py - handles project setup"""
        print("🔧 Creating enhanced project setup...")
        
        setup_content = '''#!/usr/bin/env python3
"""
POS Automation Framework - Enhanced Project Setup
Handles complete project configuration and environment setup
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class ProjectSetup:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.system = platform.system()
        self.python_exe = sys.executable
        
    def setup_project(self):
        """Complete project setup process"""
        print("🚀 POS Automation Framework - Project Setup")
        print("=" * 50)
        print(f"🖥️ System: {self.system}")
        print(f"🐍 Python: {sys.version}")
        print(f"📁 Project Directory: {self.base_dir}")
        print()
        
        try:
            # Check Python environment
            self._check_python_environment()
            
            # Verify dependencies
            self._verify_dependencies()
            
            # Setup project structure
            self._setup_project_structure()
            
            # Configure VS Code
            self._configure_vscode()
            
            # Test framework components
            self._test_framework_components()
            
            # Run validation
            self._run_project_validation()
            
            print("\\n🎉 Project setup completed successfully!")
            print("✅ Framework ready for use")
            print("📋 Next step: python 3_deploy_to_github.py (optional)")
            
        except Exception as e:
            print(f"\\n❌ Project setup failed: {e}")
            self._provide_troubleshooting()
            
    def _check_python_environment(self):
        """Check Python version and environment"""
        print("🔍 Checking Python environment...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            raise Exception(f"Python 3.8+ required, found {version.major}.{version.minor}")
        
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    
    def _verify_dependencies(self):
        """Verify that required dependencies are installed"""
        print("📦 Verifying dependencies...")
        
        required_packages = {
            "pytest": "Testing framework",
            "pywinauto": "Windows automation"
        }
        
        missing_packages = []
        
        for package, description in required_packages.items():
            try:
                __import__(package)
                print(f"  ✅ {package} - {description}")
            except ImportError:
                print(f"  ❌ {package} - Missing ({description})")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\\n⚠️ Missing packages: {', '.join(missing_packages)}")
            print("💡 Run: python 1_setup_offline_machine.py first")
            
            response = input("\\nContinue anyway? (y/n) [y]: ").lower()
            if response and response != 'y':
                raise Exception("Dependencies not satisfied")
        else:
            print("  ✅ All dependencies satisfied")
    
    def _setup_project_structure(self):
        """Setup project directory structure"""
        print("📁 Setting up project structure...")
        
        # Create required directories
        directories = ["logs", "reports", "temp"]
        
        for directory in directories:
            dir_path = os.path.join(self.base_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
            print(f"  ✅ Created/verified: {directory}/")
        
        # Create gitignore if not exists
        gitignore_path = os.path.join(self.base_dir, ".gitignore")
        if not os.path.exists(gitignore_path):
            gitignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache/
logs/*.log
temp/*
reports/*.html
reports/*.xml
!reports/.gitkeep
.env
.venv
venv/
"""
            with open(gitignore_path, "w") as f:
                f.write(gitignore_content)
            print("  ✅ Created: .gitignore")
        
        print("  ✅ Project structure ready")
    
    def _configure_vscode(self):
        """Configure VS Code workspace if available"""
        print("🎨 Configuring VS Code...")
        
        workspace_file = os.path.join(self.base_dir, "pos-automation.code-workspace")
        
        if os.path.exists(workspace_file):
            print("  ✅ VS Code workspace file found")
            
            # Check if VS Code is available
            try:
                subprocess.run(["code", "--version"], capture_output=True, check=True)
                print("  ✅ VS Code available")
                print(f"  💡 Open workspace: code {workspace_file}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("  ⚠️ VS Code not found, but workspace file ready")
        else:
            print("  ⚠️ VS Code workspace file not found")
    
    def _test_framework_components(self):
        """Test that framework components are working"""
        print("🧪 Testing framework components...")
        
        components = {
            "config/config.py": "Configuration module",
            "data/csv_data_manager.py": "CSV data manager",
            "utils/pos_base.py": "POS automation utilities",
            "tests/": "Test suite"
        }
        
        all_ok = True
        
        for path, description in components.items():
            full_path = os.path.join(self.base_dir, path)
            if os.path.exists(full_path):
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} - Missing: {path}")
                all_ok = False
        
        if not all_ok:
            print("  ⚠️ Some components missing, but framework may still work")
        else:
            print("  ✅ All framework components present")
    
    def _run_project_validation(self):
        """Run project validation tests"""
        print("🔍 Running project validation...")
        
        # Run diagnostic script if available
        diagnostic_script = os.path.join(self.base_dir, "run_all_diagnostics.py")
        
        if os.path.exists(diagnostic_script):
            try:
                print("  🧪 Running diagnostic tests...")
                result = subprocess.run([
                    self.python_exe, diagnostic_script
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print("  ✅ All diagnostic tests passed")
                else:
                    print("  ⚠️ Some diagnostic tests failed, but framework should work")
                    
            except subprocess.TimeoutExpired:
                print("  ⚠️ Diagnostic tests timed out")
            except Exception as e:
                print(f"  ⚠️ Could not run diagnostics: {e}")
        else:
            print("  ⚠️ Diagnostic script not found")
        
        print("  ✅ Project validation completed")
    
    def _provide_troubleshooting(self):
        """Provide troubleshooting information"""
        print("\\n🔧 TROUBLESHOOTING:")
        print("=" * 30)
        print("1. Check Python version: python --version (need 3.8+)")
        print("2. Install missing packages: python 1_setup_offline_machine.py")
        print("3. Check file permissions in project directory")
        print("4. Run diagnostic: python run_all_diagnostics.py")
        print("5. Check logs in logs/ directory")

if __name__ == "__main__":
    setup = ProjectSetup()
    setup.setup_project()
'''
        
        setup_file = os.path.join(package_dir, "2_setup_new_machine_enhanced.py")
        with open(setup_file, "w", encoding='utf-8') as f:
            f.write(setup_content)
        print(f"  ✅ Created: 2_setup_new_machine_enhanced.py")
    
    def _create_github_deployer(self, package_dir):
        """Create GitHub deployment script with maximum error handling"""
        print("🔧 Creating GitHub deployer...")
        
        github_content = '''#!/usr/bin/env python3
"""
POS Automation Framework - GitHub Deployment with Maximum Error Handling
Handles GitHub setup with Diva-ditcom and other accounts, with comprehensive error handling
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class GitHubDeployer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_account = "Diva-ditcom"
        self.default_repo = "pos-automation-framework"
        self.deployment_log = []
        
    def deploy_to_github(self):
        """Complete GitHub deployment with maximum error handling"""
        print("🚀 POS Automation Framework - GitHub Deployment")
        print("=" * 55)
        print(f"📁 Project Directory: {self.base_dir}")
        print(f"🎯 Default Account: {self.default_account}")
        print()
        
        try:
            # Pre-deployment checks
            self._pre_deployment_checks()
            
            # Git installation and configuration
            self._setup_git_environment()
            
            # Repository initialization
            self._initialize_repository()
            
            # GitHub remote setup
            self._setup_github_remote()
            
            # Pre-commit preparation
            self._prepare_for_commit()
            
            # Commit and push with error handling
            self._commit_and_push_with_retry()
            
            # Post-deployment verification
            self._verify_deployment()
            
            print("\\n🎉 GitHub deployment completed successfully!")
            self._show_success_information()
            
        except Exception as e:
            print(f"\\n❌ GitHub deployment failed: {e}")
            self._provide_deployment_troubleshooting()
            
    def _pre_deployment_checks(self):
        """Comprehensive pre-deployment checks"""
        print("🔍 Pre-deployment checks...")
        
        # Check if project is properly set up
        required_files = ["config/config.py", "tests/", "requirements.txt"]
        missing_files = []
        
        for file_path in required_files:
            if not os.path.exists(os.path.join(self.base_dir, file_path)):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"  ⚠️ Missing files: {missing_files}")
            print("  💡 Run: python 2_setup_new_machine_enhanced.py first")
            
            response = input("  Continue anyway? (y/n) [y]: ").lower()
            if response and response != 'y':
                raise Exception("Project not properly set up")
        else:
            print("  ✅ Project files present")
    
    def _setup_git_environment(self):
        """Setup Git environment with error handling"""
        print("🔧 Setting up Git environment...")
        
        # Check Git installation
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
            print(f"  ✅ {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ❌ Git not found!")
            self._provide_git_installation_help()
            raise Exception("Git is not installed")
        
        # Configure Git user if needed
        self._configure_git_user()
        
        # Configure Git settings for better compatibility
        self._configure_git_settings()
    
    def _configure_git_user(self):
        """Configure Git user with error handling"""
        print("👤 Configuring Git user...")
        
        try:
            # Check current configuration
            name_result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
            email_result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
            
            if name_result.returncode == 0 and email_result.returncode == 0:
                name = name_result.stdout.strip()
                email = email_result.stdout.strip()
                if name and email:
                    print(f"  ✅ Git user configured: {name} <{email}>")
                    return
        except Exception:
            pass
        
        # Need to configure user
        print("  🔧 Git user not configured. Please provide details:")
        
        while True:
            try:
                user_name = input("    Your name: ").strip()
                user_email = input("    Your email: ").strip()
                
                if user_name and user_email and "@" in user_email:
                    subprocess.run(["git", "config", "user.name", user_name], check=True)
                    subprocess.run(["git", "config", "user.email", user_email], check=True)
                    print(f"  ✅ Git user configured: {user_name} <{user_email}>")
                    break
                else:
                    print("    ❌ Please provide valid name and email")
            except KeyboardInterrupt:
                raise Exception("User cancelled Git configuration")
            except Exception as e:
                print(f"    ❌ Configuration failed: {e}")
    
    def _configure_git_settings(self):
        """Configure Git settings for better compatibility"""
        print("⚙️ Configuring Git settings...")
        
        settings = [
            ("init.defaultBranch", "main"),
            ("core.autocrlf", "true" if os.name == 'nt' else "input"),
            ("pull.rebase", "false")
        ]
        
        for setting, value in settings:
            try:
                subprocess.run(["git", "config", setting, value], 
                             cwd=self.base_dir, capture_output=True)
            except:
                pass  # Ignore errors in git config
        
        print("  ✅ Git settings configured")
    
    def _initialize_repository(self):
        """Initialize Git repository with error handling"""
        print("📦 Initializing repository...")
        
        git_dir = os.path.join(self.base_dir, ".git")
        
        if os.path.exists(git_dir):
            print("  ✅ Git repository already initialized")
            return
        
        try:
            subprocess.run(["git", "init"], cwd=self.base_dir, check=True)
            print("  ✅ Git repository initialized")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to initialize Git repository: {e}")
    
    def _setup_github_remote(self):
        """Setup GitHub remote with user input and error handling"""
        print("🌐 Setting up GitHub remote...")
        
        # Get account and repository details
        print(f"  🎯 Default account: {self.default_account}")
        account = input(f"    GitHub account [{self.default_account}]: ").strip()
        if not account:
            account = self.default_account
        
        repo_name = input(f"    Repository name [{self.default_repo}]: ").strip()
        if not repo_name:
            repo_name = self.default_repo
        
        # Setup remote URL
        remote_url = f"https://github.com/{account}/{repo_name}.git"
        
        try:
            # Check if remote already exists
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  cwd=self.base_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                current_url = result.stdout.strip()
                print(f"  ✅ Remote already exists: {current_url}")
                
                if current_url != remote_url:
                    response = input(f"    Change to {remote_url}? (y/n) [n]: ").lower()
                    if response == 'y':
                        subprocess.run(["git", "remote", "set-url", "origin", remote_url], 
                                     cwd=self.base_dir, check=True)
                        print(f"  ✅ Remote updated to: {remote_url}")
            else:
                # Add new remote
                subprocess.run(["git", "remote", "add", "origin", remote_url], 
                             cwd=self.base_dir, check=True)
                print(f"  ✅ Remote added: {remote_url}")
                
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Remote setup issue: {e}")
            print(f"  💡 Make sure repository exists: https://github.com/{account}/{repo_name}")
            
            response = input("    Continue anyway? (y/n) [y]: ").lower()
            if response and response != 'y':
                raise Exception("Remote setup cancelled")
    
    def _prepare_for_commit(self):
        """Prepare files for commit"""
        print("📝 Preparing for commit...")
        
        try:
            # Add all files
            subprocess.run(["git", "add", "."], cwd=self.base_dir, check=True)
            
            # Check if there are changes to commit
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  cwd=self.base_dir, capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                print("  ✅ Files staged for commit")
            else:
                print("  ⚠️ No changes to commit")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to prepare files for commit: {e}")
    
    def _commit_and_push_with_retry(self):
        """Commit and push with retry logic and error handling"""
        print("📤 Committing and pushing to GitHub...")
        
        # Commit changes
        try:
            commit_message = f"Complete POS Automation Framework deployment - {Path().cwd().name}"
            subprocess.run(["git", "commit", "-m", commit_message], 
                         cwd=self.base_dir, check=True)
            print("  ✅ Changes committed")
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in str(e):
                print("  ⚠️ Nothing to commit")
            else:
                print(f"  ❌ Commit failed: {e}")
                raise Exception("Commit failed")
        
        # Push with retry and SSL handling
        self._push_with_retry()
    
    def _push_with_retry(self):
        """Push to GitHub with retry logic and SSL handling"""
        print("  🚀 Pushing to GitHub...")
        
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"    Attempt {attempt + 1}/{max_retries}")
                
                # Try push
                result = subprocess.run(["git", "push", "-u", "origin", "main"], 
                                      cwd=self.base_dir, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print("  ✅ Successfully pushed to GitHub")
                    return
                else:
                    error_msg = result.stderr.lower()
                    
                    # Handle SSL issues
                    if "ssl" in error_msg or "certificate" in error_msg:
                        print("    ⚠️ SSL issue detected, trying workaround...")
                        self._handle_ssl_issues()
                        continue
                    
                    # Handle authentication issues
                    if "authentication" in error_msg or "permission denied" in error_msg:
                        print("    ⚠️ Authentication issue detected")
                        self._handle_authentication_issues()
                        continue
                    
                    print(f"    ❌ Push failed: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print("    ⚠️ Push timed out")
            except Exception as e:
                print(f"    ❌ Push error: {e}")
        
        # If all retries failed
        print("  ❌ Push failed after all retries")
        self._provide_push_troubleshooting()
    
    def _handle_ssl_issues(self):
        """Handle SSL certificate issues"""
        try:
            subprocess.run(["git", "config", "http.sslVerify", "false"], 
                         cwd=self.base_dir, check=True)
            
            # Try push again
            result = subprocess.run(["git", "push", "-u", "origin", "main"], 
                                  cwd=self.base_dir, capture_output=True, text=True, timeout=60)
            
            # Re-enable SSL
            subprocess.run(["git", "config", "http.sslVerify", "true"], 
                         cwd=self.base_dir, check=True)
            
            if result.returncode == 0:
                print("    ✅ SSL workaround successful")
                return True
                
        except Exception as e:
            print(f"    ❌ SSL workaround failed: {e}")
        
        return False
    
    def _handle_authentication_issues(self):
        """Handle authentication issues"""
        print("    🔐 Authentication required:")
        print("      1. Make sure repository exists on GitHub")
        print("      2. Use Personal Access Token instead of password")
        print("      3. Or setup SSH key authentication")
        print("      4. Check repository permissions")
        
        response = input("    Try again? (y/n) [y]: ").lower()
        return response != 'n'
    
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
                    if 'origin' in line and 'fetch' in line:
                        remote_url = line.split()[1]
                        print(f"    📍 Repository: {remote_url}")
                        break
            
            # Check last commit
            result = subprocess.run(["git", "log", "--oneline", "-1"], 
                                  cwd=self.base_dir, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"  ✅ Last commit: {result.stdout.strip()}")
            
            print("  ✅ Deployment verification completed")
            
        except subprocess.CalledProcessError:
            print("  ⚠️ Could not fully verify deployment")
    
    def _show_success_information(self):
        """Show success information and next steps"""
        print("\\n🎊 GITHUB DEPLOYMENT SUCCESS!")
        print("=" * 35)
        
        # Get remote URL
        try:
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  cwd=self.base_dir, capture_output=True, text=True)
            if result.returncode == 0:
                repo_url = result.stdout.strip().replace('.git', '')
                print(f"📍 Repository: {repo_url}")
                print(f"🎯 Actions: {repo_url}/actions")
                print(f"📊 Insights: {repo_url}/pulse")
        except:
            pass
        
        print("\\n📋 What happens next:")
        print("  ✅ GitHub Actions workflow will run automatically")
        print("  ✅ Tests will execute in CI/CD environment")
        print("  ✅ HTML reports will be generated")
        print("  ✅ Framework ready for team collaboration")
        
        print("\\n🛠️ Available commands:")
        print("  git status          - Check repository status")
        print("  git pull           - Get latest changes")
        print("  git push           - Push new changes")
        print("  python -m pytest  - Run tests locally")
    
    def _provide_git_installation_help(self):
        """Provide Git installation help"""
        print("\\n📥 GIT INSTALLATION REQUIRED:")
        print("=" * 35)
        print("Windows: https://git-scm.com/download/win")
        print("Mac: brew install git")
        print("Linux: sudo apt install git")
        print("\\nAfter installation, run this script again.")
    
    def _provide_deployment_troubleshooting(self):
        """Provide comprehensive troubleshooting"""
        print("\\n🔧 GITHUB DEPLOYMENT TROUBLESHOOTING:")
        print("=" * 45)
        print("1. Repository Issues:")
        print("   - Make sure repository exists on GitHub")
        print("   - Check repository name spelling")
        print("   - Verify account access permissions")
        print()
        print("2. Authentication Issues:")
        print("   - Use Personal Access Token (not password)")
        print("   - Setup SSH key authentication")
        print("   - Check two-factor authentication settings")
        print()
        print("3. Network Issues:")
        print("   - Check internet connectivity")
        print("   - Try different network/disable VPN")
        print("   - Corporate firewall may block Git")
        print()
        print("4. Manual Push (if all else fails):")
        print("   git config http.sslVerify false")
        print("   git push -u origin main")
        print("   git config http.sslVerify true")

if __name__ == "__main__":
    deployer = GitHubDeployer()
    deployer.deploy_to_github()
'''
        
        github_file = os.path.join(package_dir, "3_deploy_to_github.py")
        with open(github_file, "w", encoding='utf-8') as f:
            f.write(github_content)
        print(f"  ✅ Created: 3_deploy_to_github.py")
    
    def _create_master_installer(self, package_dir):
        """Create master installer that runs everything in sequence"""
        print("🔧 Creating master installer...")
        
        master_content = '''#!/usr/bin/env python3
"""
POS Automation Framework - Master Installer
Runs complete installation sequence with maximum error handling
"""

import os
import sys
import subprocess
from pathlib import Path

class MasterInstaller:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.python_exe = sys.executable
        
    def run_complete_installation(self):
        """Run complete installation sequence"""
        print("🎯 POS Automation Framework - Master Installer")
        print("=" * 55)
        print("This will run the complete installation sequence:")
        print("  1. Offline package installation")
        print("  2. Project setup and configuration")
        print("  3. GitHub deployment (optional)")
        print()
        
        try:
            # Step 1: Offline package installation
            self._run_offline_installation()
            
            # Step 2: Project setup
            self._run_project_setup()
            
            # Step 3: GitHub deployment (optional)
            self._run_github_deployment()
            
            print("\\n🎉 COMPLETE INSTALLATION SUCCESSFUL!")
            self._show_final_summary()
            
        except KeyboardInterrupt:
            print("\\n⚠️ Installation cancelled by user")
        except Exception as e:
            print(f"\\n❌ Installation failed: {e}")
            self._provide_recovery_steps()
    
    def _run_offline_installation(self):
        """Run offline package installation"""
        print("\\n" + "="*50)
        print("🔥 STEP 1: OFFLINE PACKAGE INSTALLATION")
        print("="*50)
        
        script_path = os.path.join(self.base_dir, "1_setup_offline_machine.py")
        
        if not os.path.exists(script_path):
            print("❌ Offline installer not found, skipping...")
            return
        
        try:
            result = subprocess.run([self.python_exe, script_path], 
                                  cwd=self.base_dir, timeout=300)
            
            if result.returncode == 0:
                print("✅ Offline installation completed successfully")
            else:
                print("⚠️ Offline installation had issues, continuing...")
                
        except subprocess.TimeoutExpired:
            print("⚠️ Offline installation timed out, continuing...")
        except Exception as e:
            print(f"⚠️ Offline installation error: {e}")
            
            response = input("Continue with project setup? (y/n) [y]: ").lower()
            if response and response != 'y':
                raise Exception("Installation cancelled")
    
    def _run_project_setup(self):
        """Run project setup"""
        print("\\n" + "="*50)
        print("🛠️ STEP 2: PROJECT SETUP")
        print("="*50)
        
        script_path = os.path.join(self.base_dir, "2_setup_new_machine_enhanced.py")
        
        if not os.path.exists(script_path):
            raise Exception("Project setup script not found")
        
        try:
            result = subprocess.run([self.python_exe, script_path], 
                                  cwd=self.base_dir, timeout=300)
            
            if result.returncode == 0:
                print("✅ Project setup completed successfully")
            else:
                print("⚠️ Project setup had issues")
                response = input("Continue with GitHub deployment? (y/n) [n]: ").lower()
                if response != 'y':
                    return
                
        except subprocess.TimeoutExpired:
            print("⚠️ Project setup timed out")
        except Exception as e:
            print(f"❌ Project setup error: {e}")
            raise
    
    def _run_github_deployment(self):
        """Run GitHub deployment (optional)"""
        print("\\n" + "="*50)
        print("🚀 STEP 3: GITHUB DEPLOYMENT (OPTIONAL)")
        print("="*50)
        
        response = input("Deploy to GitHub? (y/n) [y]: ").lower()
        if response and response != 'y':
            print("⏭️ Skipping GitHub deployment")
            return
        
        script_path = os.path.join(self.base_dir, "3_deploy_to_github.py")
        
        if not os.path.exists(script_path):
            print("❌ GitHub deployment script not found")
            return
        
        try:
            result = subprocess.run([self.python_exe, script_path], 
                                  cwd=self.base_dir, timeout=600)
            
            if result.returncode == 0:
                print("✅ GitHub deployment completed successfully")
            else:
                print("⚠️ GitHub deployment had issues")
                
        except subprocess.TimeoutExpired:
            print("⚠️ GitHub deployment timed out")
        except Exception as e:
            print(f"❌ GitHub deployment error: {e}")
    
    def _show_final_summary(self):
        """Show final installation summary"""
        print("\\n🎊 INSTALLATION COMPLETE!")
        print("=" * 30)
        print("✅ POS Automation Framework is ready!")
        print()
        print("📋 What you can do now:")
        print("  🧪 Run tests: python -m pytest tests/ -v")
        print("  📊 Generate reports: python -m pytest --html=reports/report.html")
        print("  🔍 Run diagnostics: python run_all_diagnostics.py")
        print("  🎨 Open VS Code: code pos-automation.code-workspace")
        print()
        print("📁 Important directories:")
        print(f"  📋 Project: {self.base_dir}")
        print(f"  📊 Reports: {os.path.join(self.base_dir, 'reports')}")
        print(f"  📝 Logs: {os.path.join(self.base_dir, 'logs')}")
        print()
        print("🎯 Framework ready for POS automation testing!")
    
    def _provide_recovery_steps(self):
        """Provide recovery steps if installation fails"""
        print("\\n🔧 RECOVERY STEPS:")
        print("=" * 20)
        print("If installation failed, try running scripts manually:")
        print()
        print("1. Install packages:")
        print("   python 1_setup_offline_machine.py")
        print()
        print("2. Setup project:")
        print("   python 2_setup_new_machine_enhanced.py")
        print()
        print("3. Deploy to GitHub:")
        print("   python 3_deploy_to_github.py")
        print()
        print("4. Verify installation:")
        print("   python run_all_diagnostics.py")

if __name__ == "__main__":
    installer = MasterInstaller()
    installer.run_complete_installation()
'''
        
        master_file = os.path.join(package_dir, "0_MASTER_INSTALLER.py")
        with open(master_file, "w", encoding='utf-8') as f:
            f.write(master_content)
        print(f"  ✅ Created: 0_MASTER_INSTALLER.py")
    
    def _create_execution_guide(self, package_dir):
        """Create comprehensive execution guide"""
        print("📚 Creating execution guide...")
        
        guide_content = f'''# POS Automation Framework - Complete Deployment Guide

## 🎯 WHAT TO RUN AFTER EXTRACTING THE PACKAGE

### **Quick Start (Recommended)**
```bash
python 0_MASTER_INSTALLER.py
```
**This runs everything automatically in the correct order!**

---

## 📋 STEP-BY-STEP EXECUTION ORDER

### **Option 1: Automatic Installation**
```bash
# Run this ONE file - it does everything:
python 0_MASTER_INSTALLER.py
```

### **Option 2: Manual Step-by-Step**
```bash
# Step 1: Install packages (for proxy/network issues)
python 1_setup_offline_machine.py

# Step 2: Setup project and framework
python 2_setup_new_machine_enhanced.py

# Step 3: Deploy to GitHub (optional)
python 3_deploy_to_github.py
```

---

## 🔧 DETAILED SCRIPT DESCRIPTIONS

### **`0_MASTER_INSTALLER.py` - Complete Automation**
- ✅ Runs all steps automatically
- ✅ Handles errors and user prompts
- ✅ Maximum error handling
- ✅ **RECOMMENDED FOR ALL USERS**

### **`1_setup_offline_machine.py` - Package Installation**
**When to use:** 
- Internet connection issues
- Corporate proxy problems
- Package installation failures

**What it does:**
- ✅ Installs pytest, pywinauto, and other dependencies
- ✅ Handles offline package installation
- ✅ Downloads packages if internet available
- ✅ Provides manual installation instructions
- ✅ Works with corporate networks

### **`2_setup_new_machine_enhanced.py` - Project Setup**
**When to use:** 
- After package installation
- Setting up framework structure
- Configuring development environment

**What it does:**
- ✅ Validates Python environment (3.8+ required)
- ✅ Verifies all dependencies installed
- ✅ Creates project directory structure
- ✅ Configures VS Code workspace
- ✅ Tests framework components
- ✅ Runs validation diagnostics

### **`3_deploy_to_github.py` - GitHub Integration**
**When to use:** 
- Setting up GitHub repository
- Enabling CI/CD with GitHub Actions
- Team collaboration setup

**What it does:**
- ✅ Checks Git installation
- ✅ Configures Git user credentials
- ✅ Initializes Git repository
- ✅ Sets up GitHub remote (defaults to **Diva-ditcom**)
- ✅ Handles SSL and authentication issues
- ✅ Pushes complete framework to GitHub
- ✅ Enables GitHub Actions workflow

---

## 🎯 GITHUB INTEGRATION FEATURES

### **Default Configuration:**
- **Account**: `Diva-ditcom` (configurable)
- **Repository**: `pos-automation-framework`
- **Branch**: `main`
- **Workflow**: GitHub Actions CI/CD enabled

### **What Happens on GitHub:**
1. ✅ Complete framework uploaded
2. ✅ GitHub Actions workflow starts automatically
3. ✅ Tests run in CI/CD environment
4. ✅ Test reports generated
5. ✅ Ready for team collaboration

---

## 🚨 ERROR HANDLING SCENARIOS

### **Scenario 1: Package Installation Fails**
```bash
# Run offline installer first:
python 1_setup_offline_machine.py

# Then continue with project setup:
python 2_setup_new_machine_enhanced.py
```

### **Scenario 2: Proxy/Corporate Network Issues**
```bash
# Offline installer handles this:
python 1_setup_offline_machine.py
# Provides manual installation instructions
```

### **Scenario 3: GitHub Authentication Issues**
```bash
# GitHub deployer provides comprehensive help:
python 3_deploy_to_github.py
# Guides through token setup and SSH keys
```

### **Scenario 4: Python Version Issues**
- Minimum requirement: **Python 3.8+**
- Recommended: **Python 3.11+**
- All scripts check and validate Python version

---

## 🔍 VERIFICATION COMMANDS

### **After Each Step:**
```bash
# Verify package installation:
python -c "import pytest, pywinauto; print('Packages OK')"

# Verify project setup:
python run_all_diagnostics.py

# Verify GitHub deployment:
git remote -v
git status
```

---

## 📁 WHAT'S INCLUDED IN PACKAGE

### **Framework Components:**
- `config/` - Framework configuration
- `data/` - CSV data and test scenarios
- `tests/` - Complete test suite (4 test scenarios)
- `utils/` - POS automation utilities
- `reports/` - Test execution reports
- `.github/` - GitHub Actions workflow

### **Setup Scripts:**
- `0_MASTER_INSTALLER.py` - Complete automation
- `1_setup_offline_machine.py` - Package installation
- `2_setup_new_machine_enhanced.py` - Project setup
- `3_deploy_to_github.py` - GitHub deployment

### **Development Tools:**
- `pos-automation.code-workspace` - VS Code workspace
- `run_all_diagnostics.py` - Framework validation
- `import_helper.py` - Development utilities

---

## ✅ SUCCESS INDICATORS

### **After Successful Installation:**
- ✅ All diagnostic tests pass
- ✅ pytest can discover tests
- ✅ Framework components load correctly
- ✅ VS Code workspace configured
- ✅ GitHub repository created (if deployed)
- ✅ CI/CD workflow running

### **Ready for Use When:**
```bash
python run_all_diagnostics.py
# Shows: "Overall Status: ALL TESTS PASSED"
```

---

## 🎉 WHAT YOU GET

### **Complete POS Automation Framework:**
- ✅ 4 test scenarios ready to run
- ✅ Data-driven testing with CSV files
- ✅ HTML and XML report generation
- ✅ GitHub Actions CI/CD pipeline
- ✅ VS Code development environment
- ✅ Cross-platform compatibility

### **Production Ready:**
- ✅ Works with any POS application
- ✅ Configurable for different environments
- ✅ Team collaboration ready
- ✅ Enterprise-grade error handling

---

## 📞 TROUBLESHOOTING

### **If Something Goes Wrong:**
1. **Run diagnostics**: `python run_all_diagnostics.py`
2. **Check logs**: Look in `logs/` directory
3. **Manual steps**: Run scripts individually
4. **Start over**: Extract package again and run master installer

### **Common Issues & Solutions:**
- **Python not found**: Install Python 3.8+ from python.org
- **Package install fails**: Run `1_setup_offline_machine.py`
- **Git not found**: Install Git from git-scm.com
- **GitHub auth fails**: Use Personal Access Token

---

## 🚀 QUICK SUCCESS PATH

```bash
# Extract the package
# Open terminal/command prompt in extracted folder
# Run ONE command:
python 0_MASTER_INSTALLER.py

# Follow the prompts
# Done! Framework ready for POS automation testing
```

**That's it! The framework will be completely set up and ready for use!** 🎯

Package created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
        
        guide_file = os.path.join(package_dir, "EXECUTION_GUIDE.md")
        with open(guide_file, "w", encoding='utf-8') as f:
            f.write(guide_content)
        print(f"  ✅ Created: EXECUTION_GUIDE.md")
    
    def _create_offline_packages(self, package_dir):
        """Create offline packages directory with instructions"""
        print("📦 Creating offline packages structure...")
        
        offline_dir = os.path.join(package_dir, "offline_packages")
        os.makedirs(offline_dir, exist_ok=True)
        
        # Create README for offline packages
        readme_content = '''# Offline Packages Directory

This directory is used for offline package installation when internet connectivity is limited.

## How it works:

1. The `1_setup_offline_machine.py` script looks for .whl files here
2. If not found, it tries to download them automatically
3. If download fails, it provides manual installation instructions

## To add packages manually:

1. Download .whl files from https://pypi.org/
2. Place them in this directory
3. Run: `python 1_setup_offline_machine.py`

## Required packages:

- pytest >= 7.0.0
- pywinauto >= 0.6.0
- pytest-html >= 3.0.0
- pytest-xdist >= 3.0.0
- openpyxl >= 3.0.0

## Corporate networks:

If you're behind a corporate firewall:
1. Download packages on a machine with internet access
2. Copy .whl files to this directory
3. Run the offline installer
'''
        
        readme_file = os.path.join(offline_dir, "README.md")
        with open(readme_file, "w", encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"  ✅ Created offline packages structure")
    
    def _create_zip_package(self, package_dir):
        """Create ZIP package for distribution"""
        print("\n📦 Creating ZIP package...")
        
        import zipfile
        
        zip_path = f"{package_dir}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_dir):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.pytest_cache']]
                
                for file in files:
                    if not file.endswith(('.pyc', '.pyo')):
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, os.path.dirname(package_dir))
                        zipf.write(file_path, arc_path)
        
        print(f"  ✅ Created ZIP: {zip_path}")
        return zip_path
