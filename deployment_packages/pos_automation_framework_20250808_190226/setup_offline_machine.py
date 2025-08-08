#!/usr/bin/env python3
"""
Enhanced Setup Script for POS Automation Framework
Supports both online and offline installation
"""
import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {text}")
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
        print(f"✅ Python found: {output.strip()}")
        return True
    else:
        print("❌ Python not found!")
        print("Please install Python 3.8+ from https://python.org")
        return False


def check_offline_packages():
    """Check if offline packages are available"""
    offline_dir = Path("offline_packages")
    if offline_dir.exists():
        wheel_files = list(offline_dir.glob("*.whl"))
        if wheel_files:
            print(f"📦 Found offline packages directory with {len(wheel_files)} wheel files")
            return True
    return False


def install_dependencies_offline():
    """Install dependencies from offline packages"""
    print_step(2, "Installing dependencies from offline packages")
    
    try:
        # Run the offline installation script
        result = subprocess.run([sys.executable, "install_offline_packages.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Dependencies installed successfully from offline packages")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies from offline packages")
        print(f"Error: {e.stderr}")
        return False


def install_dependencies_online():
    """Install dependencies from PyPI"""
    print_step(2, "Installing dependencies from PyPI")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully from PyPI")
        return True
    else:
        print("❌ Failed to install dependencies from PyPI")
        print(f"Error: {output}")
        return False


def test_framework_components():
    """Test if framework components load correctly"""
    print_step(3, "Testing framework components")
    
    tests = [
        ("CSV Manager", "from data.csv_data_manager import csv_data_manager; print('CSV Manager loaded')"),
        ("Configuration", "from config.config import Config; print('Config loaded')"),
        ("POS Automation", "from utils.pos_base import POSAutomation; print('POS Automation loaded')")
    ]
    
    for name, test_code in tests:
        print(f"   Testing {name}...")
        success, output = run_command(f'python -c "{test_code}"')
        if success:
            print(f"   ✅ {name} loaded successfully")
        else:
            print(f"   ❌ {name} failed to load")
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
        print(f"✅ Pytest discovered {test_count} tests successfully")
        return True
    else:
        print("❌ Pytest test discovery failed")
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
        print("✅ CSV data loading successful")
        print("   " + output.replace("\n", "\n   "))
        return True
    else:
        print("❌ CSV data loading failed")
        print(f"Error: {output}")
        return False


def display_next_steps():
    """Display next steps for the user"""
    print_header("Setup Completed Successfully!")
    
    print("\n📝 Next steps:")
    print("   1. Update data\\app_settings.csv with your POS application path")
    print("   2. Update data\\test_scenarios.csv with your test data")
    print("   3. Run tests: python run_tests.py")
    print("   4. Manage data: python manage_csv_data.py")
    
    print("\n🎯 Quick commands:")
    print("   • Test framework: python run_tests.py")
    print("   • Manage data: python manage_csv_data.py")
    print("   • View help: python -m pytest --help")
    
    print("\n📁 Important files to configure:")
    print("   • data\\app_settings.csv - Application configuration")
    print("   • data\\test_scenarios.csv - Test data")
    
    print("\n🔧 Framework structure validated:")
    print("   ✅ All Python modules loading correctly")
    print("   ✅ All dependencies installed")
    print("   ✅ Pytest discovering tests")
    print("   ✅ CSV data management working")


def display_error_help():
    """Display troubleshooting help"""
    print("\n❌ Setup failed! Troubleshooting tips:")
    print("   • Ensure you're running from the correct directory")
    print("   • Check if all files are present in the framework folder")
    print("   • For online installation: pip install --upgrade -r requirements.txt")
    print("   • For offline installation: python download_offline_packages.py")
    print("   • Verify Python version is 3.8 or higher")
    print("   • Check for any missing CSV files in data/ folder")


def choose_installation_method():
    """Let user choose between online and offline installation"""
    offline_available = check_offline_packages()
    
    if offline_available:
        print("\n🔧 Installation Options Available:")
        print("   1. 📦 Offline installation (recommended for restricted networks)")
        print("   2. 🌐 Online installation (download from PyPI)")
        print("   3. 🔄 Auto-detect (try offline first, fallback to online)")
        
        while True:
            try:
                choice = input("\nSelect installation method (1-3): ").strip()
                if choice == "1":
                    return "offline"
                elif choice == "2":
                    return "online"
                elif choice == "3":
                    return "auto"
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\n\n👋 Setup cancelled by user")
                return None
    else:
        print("\n🌐 Only online installation available (no offline packages found)")
        return "online"


def main():
    """Main setup function"""
    print_header("POS Automation Framework - Enhanced Setup")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = True
    
    # Check Python first
    if not check_python():
        success = False
        display_error_help()
        return 1
    
    # Choose installation method
    install_method = choose_installation_method()
    if install_method is None:
        return 1
    
    # Install dependencies based on chosen method
    if install_method == "offline":
        if not install_dependencies_offline():
            success = False
    elif install_method == "online":
        if not install_dependencies_online():
            success = False
    elif install_method == "auto":
        # Try offline first, fallback to online
        print("\n🔄 Trying offline installation first...")
        if not install_dependencies_offline():
            print("\n🔄 Offline installation failed, trying online...")
            if not install_dependencies_online():
                success = False
    
    # Continue with framework testing if installation succeeded
    if success:
        if not test_framework_components():
            success = False
        elif not test_pytest_discovery():
            success = False
        elif not test_csv_data():
            success = False
    
    if success:
        display_next_steps()
        return 0
    else:
        display_error_help()
        return 1


if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to continue...")
    sys.exit(exit_code)
