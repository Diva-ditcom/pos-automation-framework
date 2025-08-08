#!/usr/bin/env python3
"""
Download Offline Packages Script
Downloads all required packages and their dependencies as wheel files
"""
import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"📦 {text}")
    print("=" * 60)


def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {text}...")


def run_command(command, description=""):
    """Run a command and return success status"""
    try:
        print(f"   Running: {command}")
        result = subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Command failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False


def check_requirements_file():
    """Check if requirements.txt exists"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        print("Please ensure you're running this script from the framework root directory.")
        return False
    
    print("✅ requirements.txt found")
    
    # Display requirements
    with open("requirements.txt", "r") as f:
        requirements = f.read()
    print("📄 Current requirements:")
    for line in requirements.strip().split('\n'):
        if line.strip() and not line.startswith('#'):
            print(f"   • {line.strip()}")
    
    return True


def create_offline_directory():
    """Create offline packages directory"""
    offline_dir = Path("offline_packages")
    offline_dir.mkdir(exist_ok=True)
    print(f"✅ Offline packages directory ready: {offline_dir.absolute()}")
    return offline_dir


def download_packages(offline_dir):
    """Download packages as wheel files"""
    print_step(1, "Downloading packages and dependencies as wheel files")
    
    # Download command
    download_cmd = f'pip download -r requirements.txt -d "{offline_dir}" --prefer-binary'
    
    success = run_command(download_cmd)
    if success:
        print("✅ All packages downloaded successfully")
        return True
    else:
        print("❌ Failed to download packages")
        return False


def verify_downloaded_packages(offline_dir):
    """Verify downloaded packages"""
    print_step(2, "Verifying downloaded packages")
    
    wheel_files = list(offline_dir.glob("*.whl"))
    tar_files = list(offline_dir.glob("*.tar.gz"))
    
    print(f"✅ Downloaded {len(wheel_files)} wheel files")
    print(f"✅ Downloaded {len(tar_files)} source packages")
    print(f"📊 Total packages: {len(wheel_files) + len(tar_files)}")
    
    if wheel_files or tar_files:
        print("\n📦 Downloaded packages:")
        all_files = sorted(wheel_files + tar_files)
        for i, file in enumerate(all_files[:10]):  # Show first 10
            print(f"   {i+1:2d}. {file.name}")
        
        if len(all_files) > 10:
            print(f"   ... and {len(all_files) - 10} more packages")
        
        return True
    else:
        print("❌ No packages were downloaded")
        return False


def create_offline_requirements():
    """Create a requirements file with exact versions"""
    print_step(3, "Creating offline requirements file")
    
    try:
        # Get currently installed versions
        result = subprocess.run(
            "pip freeze", 
            shell=True, 
            capture_output=True, 
            text=True,
            check=True
        )
        
        installed_packages = result.stdout
        
        # Filter only our required packages
        with open("requirements.txt", "r") as f:
            required = [line.strip().split(">=")[0].split("==")[0].lower() 
                       for line in f if line.strip() and not line.startswith('#')]
        
        offline_requirements = []
        for line in installed_packages.split('\n'):
            if line.strip():
                package_name = line.split('==')[0].lower()
                if package_name in required:
                    offline_requirements.append(line.strip())
        
        # Write offline requirements file
        with open("offline_packages/requirements_offline.txt", "w") as f:
            f.write("# Offline Requirements - Exact Versions\n")
            f.write("# Generated for offline installation\n\n")
            for req in sorted(offline_requirements):
                f.write(f"{req}\n")
        
        print("✅ Created requirements_offline.txt with exact versions")
        print(f"📄 Pinned versions for {len(offline_requirements)} packages")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create offline requirements: {e}")
        return False


def create_offline_install_script():
    """Create installation script for offline packages"""
    print_step(4, "Creating offline installation script")
    
    install_script = '''#!/usr/bin/env python3
"""
Offline Package Installation Script
Installs packages from local wheel files without internet access
"""
import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\\n" + "=" * 60)
    print(f"📦 {text}")
    print("=" * 60)


def install_offline_packages():
    """Install packages from offline directory"""
    print_header("Offline Package Installation")
    
    offline_dir = Path("offline_packages")
    
    if not offline_dir.exists():
        print("❌ Offline packages directory not found!")
        return False
    
    # Check for packages
    wheel_files = list(offline_dir.glob("*.whl"))
    tar_files = list(offline_dir.glob("*.tar.gz"))
    
    if not (wheel_files or tar_files):
        print("❌ No packages found in offline_packages directory!")
        return False
    
    print(f"📦 Found {len(wheel_files)} wheel files and {len(tar_files)} source packages")
    
    # Install from offline packages
    try:
        print("\\n🔧 Installing packages from offline directory...")
        
        # Method 1: Install using --find-links (preferred)
        install_cmd = [
            sys.executable, "-m", "pip", "install",
            "--no-index",  # Don't use PyPI
            "--find-links", str(offline_dir),  # Look in offline directory
            "-r", "requirements.txt"
        ]
        
        result = subprocess.run(install_cmd, check=True)
        
        print("✅ All packages installed successfully from offline directory!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed with exit code {e.returncode}")
        
        # Fallback: Try installing wheel files directly
        print("\\n🔄 Trying fallback installation method...")
        try:
            for wheel_file in wheel_files:
                print(f"   Installing {wheel_file.name}...")
                subprocess.run([sys.executable, "-m", "pip", "install", str(wheel_file)], check=True)
            
            print("✅ Packages installed using fallback method!")
            return True
            
        except subprocess.CalledProcessError as e2:
            print(f"❌ Fallback installation also failed: {e2}")
            return False
    
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False


def verify_installation():
    """Verify that packages are installed correctly"""
    print("\\n🧪 Verifying installation...")
    
    # Test imports
    tests = [
        ("pywinauto", "import pywinauto; print(f'pywinauto {pywinauto.__version__}')"),
        ("pytest", "import pytest; print(f'pytest {pytest.__version__}')"),
        ("pytest-html", "import pytest_html; print('pytest-html available')"),
    ]
    
    for name, test_code in tests:
        try:
            result = subprocess.run([sys.executable, "-c", test_code], 
                                 capture_output=True, text=True, check=True)
            print(f"   ✅ {name}: {result.stdout.strip()}")
        except:
            print(f"   ❌ {name}: Failed to import")


if __name__ == "__main__":
    success = install_offline_packages()
    
    if success:
        verify_installation()
        print("\\n🎉 Offline installation completed successfully!")
        print("\\n📝 Next steps:")
        print("   1. Run: python setup_new_machine.py")
        print("   2. Or run: python run_tests.py")
    else:
        print("\\n❌ Offline installation failed!")
        print("\\n🔧 Troubleshooting:")
        print("   • Ensure offline_packages directory contains wheel files")
        print("   • Try: python download_offline_packages.py")
        print("   • Check Python version compatibility")
    
    input("\\nPress Enter to continue...")
'''
    
    try:
        with open("install_offline_packages.py", "w") as f:
            f.write(install_script)
        
        print("✅ Created install_offline_packages.py")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create installation script: {e}")
        return False


def create_batch_installer():
    """Create a batch file for Windows offline installation"""
    print_step(5, "Creating Windows batch installer")
    
    batch_script = '''@echo off
echo.
echo ================================================
echo 📦 POS Automation - Offline Package Installation
echo ================================================
echo.

echo 🔧 Installing packages from offline directory...
python install_offline_packages.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Offline installation failed!
    echo 🔧 Try running: python download_offline_packages.py
    pause
    exit /b 1
)

echo.
echo ✅ Offline installation completed!
echo.
echo 📝 Next steps:
echo    1. Run: python setup_new_machine.py
echo    2. Or run: python run_tests.py
echo.
pause
'''
    
    try:
        with open("install_offline_packages.bat", "w") as f:
            f.write(batch_script)
        
        print("✅ Created install_offline_packages.bat")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create batch installer: {e}")
        return False


def main():
    """Main function"""
    print_header("Download Offline Packages")
    
    # Check prerequisites
    if not check_requirements_file():
        return 1
    
    # Create offline directory
    offline_dir = create_offline_directory()
    
    # Download packages
    if not download_packages(offline_dir):
        return 1
    
    # Verify downloads
    if not verify_downloaded_packages(offline_dir):
        return 1
    
    # Create offline requirements
    if not create_offline_requirements():
        print("⚠️ Warning: Could not create offline requirements file")
    
    # Create installation scripts
    if not create_offline_install_script():
        return 1
    
    if not create_batch_installer():
        return 1
    
    # Success summary
    print_header("Download Complete!")
    print("✅ All packages downloaded successfully")
    print("✅ Offline installation scripts created")
    print("✅ Framework is now ready for offline deployment")
    
    print("\\n📦 Generated Files:")
    print("   • offline_packages/ - Directory with wheel files")
    print("   • install_offline_packages.py - Python installer")
    print("   • install_offline_packages.bat - Windows batch installer")
    print("   • offline_packages/requirements_offline.txt - Pinned versions")
    
    print("\\n🚀 Deployment Instructions:")
    print("   1. Copy entire framework folder to target machine")
    print("   2. Run: python install_offline_packages.py")
    print("   3. Run: python setup_new_machine.py")
    print("   4. Start testing: python run_tests.py")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to continue...")
    sys.exit(exit_code)
