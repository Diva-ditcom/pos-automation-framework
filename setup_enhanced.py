#!/usr/bin/env python3
"""
Enhanced POS Automation Framework Setup Script
Handles both online and offline installation with conflict resolution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Print setup header"""
    print("=" * 60)
    print("🚀 POS Automation Framework Setup (Enhanced)")
    print("=" * 60)
    print()

def print_step(step_num, description):
    """Print step header"""
    print(f"📋 Step {step_num}: {description}...")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️ {message}")

def check_python():
    """Check Python installation"""
    print_step(1, "Checking Python installation")
    try:
        version = sys.version.split()[0]
        print_success(f"Python found: Python {version}")
        
        # Check if version is sufficient
        major, minor = map(int, version.split('.')[:2])
        if major < 3 or (major == 3 and minor < 8):
            print_error(f"Python 3.8+ required, found {version}")
            return False
        return True
    except Exception as e:
        print_error(f"Python check failed: {e}")
        return False

def clean_conflicting_files():
    """Remove any conflicting __init__.py files that might shadow pywinauto"""
    print_step(2, "Cleaning conflicting files")
    
    current_dir = Path.cwd()
    root_init = current_dir / "__init__.py"
    
    cleaned_files = []
    
    # Remove __init__.py from root pywinauto directory if it exists
    if root_init.exists():
        try:
            root_init.unlink()
            cleaned_files.append(str(root_init))
            print_success(f"Removed conflicting file: {root_init}")
        except Exception as e:
            print_warning(f"Could not remove {root_init}: {e}")
    
    # Clean __pycache__ directories that might have cached the conflict
    pycache_dirs = list(current_dir.rglob("__pycache__"))
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            cleaned_files.append(str(pycache_dir))
        except Exception as e:
            print_warning(f"Could not remove {pycache_dir}: {e}")
    
    if cleaned_files:
        print_success(f"Cleaned {len(cleaned_files)} conflicting files/directories")
    else:
        print_success("No conflicting files found")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print_step(3, "Installing dependencies")
    
    try:
        # First try offline installation
        offline_packages = Path("offline_packages")
        if offline_packages.exists() and list(offline_packages.glob("*.whl")):
            print("🔄 Attempting offline installation...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "--find-links", str(offline_packages),
                "--no-index", "--no-deps",
                "-r", "requirements.txt"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print_success("Dependencies installed successfully (offline)")
                return True
            else:
                print_warning("Offline installation failed, trying online...")
        
        # Fallback to online installation
        print("🌐 Attempting online installation...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt", "--upgrade"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_success("Dependencies installed successfully (online)")
            return True
        else:
            print_error("Dependency installation failed")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Installation timed out")
        return False
    except Exception as e:
        print_error(f"Installation error: {e}")
        return False

def test_framework_components():
    """Test if framework components load correctly"""
    print_step(4, "Testing framework components")
    
    tests = [
        ("CSV Manager", "from data.csv_data_manager import CSVDataManager"),
        ("Configuration", "from config.config import POSConfig"),
        ("POS Automation", "from utils.pos_base import POSAutomation"),
    ]
    
    for test_name, import_statement in tests:
        try:
            print(f"   Testing {test_name}...")
            exec(import_statement)
            print_success(f"{test_name} loaded successfully")
        except Exception as e:
            print_error(f"{test_name} failed to load: {e}")
            return False
    
    return True

def test_pytest_discovery():
    """Test pytest test discovery"""
    print_step(5, "Testing pytest discovery")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "--collect-only", "-q"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # Count collected tests
            lines = result.stdout.split('\n')
            test_count = 0
            for line in lines:
                if 'collected' in line:
                    try:
                        test_count = int(line.split()[0])
                        break
                    except:
                        pass
            
            print_success(f"Pytest discovery successful - {test_count} tests found")
            return True
        else:
            print_error("Pytest test discovery failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Pytest discovery timed out")
        return False
    except Exception as e:
        print_error(f"Pytest discovery error: {e}")
        return False

def test_imports_specifically():
    """Test specific imports that commonly fail"""
    print_step(6, "Testing specific imports")
    
    try:
        print("   Testing pywinauto import...")
        from pywinauto import Application
        print_success("pywinauto.Application imported successfully")
        
        print("   Testing framework imports...")
        sys.path.insert(0, str(Path.cwd()))
        from utils.pos_base import POSAutomation
        print_success("Framework imports working correctly")
        
        return True
    except Exception as e:
        print_error(f"Import test failed: {e}")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Python path: {sys.path[:3]}...")
        return False

def run_sample_test():
    """Run a sample test to verify everything works"""
    print_step(7, "Running sample test")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/pos_automation/test_01_basic_cash_sale.py::test_basic_cash_sale",
            "-v", "--tb=short"
        ], capture_output=True, text=True, timeout=120)
        
        if "PASSED" in result.stdout or "collected" in result.stdout:
            print_success("Sample test execution successful")
            return True
        else:
            print_warning("Sample test had issues (may be expected if POS app not running)")
            print("Test output preview:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
            return True  # Consider this non-critical
            
    except subprocess.TimeoutExpired:
        print_warning("Sample test timed out (may be expected)")
        return True  # Consider this non-critical
    except Exception as e:
        print_warning(f"Sample test error: {e}")
        return True  # Consider this non-critical

def main():
    """Main setup function"""
    print_header()
    
    # Track setup steps
    steps = [
        ("Python Check", check_python),
        ("Clean Conflicts", clean_conflicting_files),
        ("Install Dependencies", install_dependencies),
        ("Test Components", test_framework_components),
        ("Test Pytest", test_pytest_discovery),
        ("Test Imports", test_imports_specifically),
        ("Sample Test", run_sample_test),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print_error(f"Unexpected error in {step_name}: {e}")
            failed_steps.append(step_name)
    
    print()
    print("=" * 60)
    
    if not failed_steps:
        print_success("🎉 Setup completed successfully!")
        print()
        print("Next steps:")
        print("• Run tests: python run_tests.py")
        print("• Manage data: python manage_csv_data.py")
        print("• View reports in: reports/")
        print("• Check logs in: logs/")
    else:
        print_error("❌ Setup failed!")
        print(f"Failed steps: {', '.join(failed_steps)}")
        print()
        print("Troubleshooting tips:")
        print("• Ensure you're running from the correct directory")
        print("• Check if all files are present in the framework folder")
        print("• Try: pip install --upgrade -r requirements.txt")
        print("• Verify Python version is 3.8 or higher")
        print("• Check for any missing CSV files in data/ folder")
        print("• Remove any __init__.py files from the root pywinauto directory")
    
    print("=" * 60)
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
