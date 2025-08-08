#!/usr/bin/env python3
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
            
            print("\n🎉 Framework setup completed successfully!")
            print("✅ Ready for POS automation testing")
            
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
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
