#!/usr/bin/env python3
"""
POS Automation Framework Setup Script
Validates and sets up the framework on a new machine
"""
import subprocess
import sys
import os
import argparse
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"[LAUNCH] {text}")
    print("=" * 60)


def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {text}...")


def run_command(command, description=""):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def check_python():
    """Check if Python is installed and get version"""
    print_step(1, "Checking Python installation")
    
    success, output = run_command("python --version")
    if success:
        print(f"[SUCCESS] Python found: {output.strip()}")
        return True
    else:
        print("[ERROR] Python not found!")
        print("Please install Python 3.8+ from https://python.org")
        return False


def install_dependencies():
    """Install required packages"""
    print_step(3, "Installing dependencies")
    
    if not os.path.exists("requirements.txt"):
        print("[ERROR] requirements.txt not found!")
        return False
    
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("[SUCCESS] Dependencies installed successfully")
        return True
    else:
        print("[ERROR] Failed to install dependencies")
        print(f"Error: {output}")
        return False


def test_framework_components():
    """Test if framework components load correctly"""
    print_step(4, "Testing framework components")
    
    tests = [
        ("CSV Manager", "from data.csv_data_manager import csv_data_manager; print('CSV Manager loaded')"),
        ("Configuration", "from config.config import Config; print('Config loaded')"),
        ("POS Automation", "from utils.pos_base import POSAutomation; print('POS Automation loaded')")
    ]
    
    for name, test_code in tests:
        print(f"   Testing {name}...")
        success, output = run_command(f'python -c "{test_code}"')
        if success:
            print(f"   [SUCCESS] {name} loaded successfully")
        else:
            print(f"   [ERROR] {name} failed to load")
            print(f"   Error: {output}")
            return False
    
    return True


def test_pytest_discovery():
    """Test pytest test discovery"""
    print_step(4, "Testing pytest discovery")
    
    success, output = run_command("python -m pytest --collect-only")
    if success:
        # Count tests discovered
        test_count = output.count("<Function")
        print(f"[SUCCESS] Pytest discovered {test_count} tests successfully")
        return True
    else:
        print("[ERROR] Pytest test discovery failed")
        print(f"Error: {output}")
        return False


def test_csv_data():
    """Test CSV data loading"""
    print_step(5, "Testing CSV data loading")
    
    test_code = """
from data.csv_data_manager import csv_data_manager
scenarios = csv_data_manager.list_available_scenarios()
settings = csv_data_manager.load_settings()
print(f"Found {len(scenarios)} test scenarios")
print(f"Loaded {len(settings)} application settings")
print("Available scenarios:", scenarios)
"""
    
    success, output = run_command(f'python -c "{test_code}"')
    if success:
        print("[SUCCESS] CSV data loading successful")
        print("   " + output.replace("\n", "\n   "))
        return True
    else:
        print("[ERROR] CSV data loading failed")
        print(f"Error: {output}")
        return False


def clean_conflicting_files():
    """Remove any conflicting __init__.py files that might shadow pywinauto"""
    print_step(2, "Cleaning conflicting files")
    
    current_dir = Path.cwd()
    root_init = current_dir / "__init__.py"
    
    # Remove __init__.py from root pywinauto directory if it exists
    if root_init.exists():
        try:
            root_init.unlink()
            print(f"[SUCCESS] Removed conflicting file: {root_init}")
        except Exception as e:
            print(f"[WARNING] Could not remove {root_init}: {e}")
    
    # Clean __pycache__ directories
    try:
        import shutil
        pycache_dirs = list(current_dir.rglob("__pycache__"))
        for pycache_dir in pycache_dirs:
            try:
                shutil.rmtree(pycache_dir)
            except:
                pass
        if pycache_dirs:
            print(f"[SUCCESS] Cleaned {len(pycache_dirs)} cache directories")
    except:
        pass
    
    print("[SUCCESS] Conflict cleaning completed")
    return True


def display_next_steps():
    """Display next steps for the user"""
    print_header("Setup Completed Successfully!")
    
    print("\n📝 Next steps:")
    print("   1. Update data\\app_settings.csv with your POS application path")
    print("   2. Update data\\test_scenarios.csv with your test data")
    print("   3. Run tests: python run_tests.py")
    print("   4. Manage data: python manage_csv_data.py")
    
    print("\n[TARGET] Quick commands:")
    print("   • Test framework: python run_tests.py")
    print("   • Manage data: python manage_csv_data.py")
    print("   • View help: python -m pytest --help")
    
    print("\n[FOLDER] Important files to configure:")
    print("   • data\\app_settings.csv - Application configuration")
    print("   • data\\test_scenarios.csv - Test data")
    
    print("\n[CONFIG] Framework structure validated:")
    print("   [SUCCESS] All Python modules loading correctly")
    print("   [SUCCESS] All dependencies installed")
    print("   [SUCCESS] Pytest discovering tests")
    print("   [SUCCESS] CSV data management working")


def display_error_help():
    """Display troubleshooting help"""
    print("\n[ERROR] Setup failed! Troubleshooting tips:")
    print("   • Ensure you're running from the correct directory")
    print("   • Check if all files are present in the framework folder")
    print("   • Try: pip install --upgrade -r requirements.txt")
    print("   • Verify Python version is 3.8 or higher")
    print("   • Check for any missing CSV files in data/ folder")


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='POS Automation Framework Setup')
    parser.add_argument('--ci-mode', action='store_true', help='Run in CI mode (non-interactive)')
    args = parser.parse_args()
    
    if args.ci_mode:
        print_header("POS Automation Framework Setup (CI Mode)")
    else:
        print_header("POS Automation Framework Setup")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = True
    
    # Run all setup steps
    if not check_python():
        success = False
    elif not clean_conflicting_files():
        success = False
    elif not install_dependencies():
        success = False
    elif not test_framework_components():
        success = False
    elif not test_pytest_discovery():
        success = False
    elif not test_csv_data():
        success = False
    
    if success:
        display_next_steps()
        if not args.ci_mode:
            input("\nPress Enter to continue...")
        return 0
    else:
        display_error_help()
        if not args.ci_mode:
            input("\nPress Enter to continue...")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
