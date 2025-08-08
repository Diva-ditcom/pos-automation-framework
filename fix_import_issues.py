#!/usr/bin/env python3
"""
Quick Fix for pywinauto Import Issues
Run this if you get "ImportError: cannot import name 'Application' from 'pywinauto'"
"""

import os
import shutil
from pathlib import Path

def main():
    print("🔧 Quick Fix for pywinauto Import Issues")
    print("=" * 50)
    
    current_dir = Path.cwd()
    print(f"Working directory: {current_dir}")
    
    # Check for conflicting __init__.py in root
    root_init = current_dir / "__init__.py"
    if root_init.exists():
        try:
            root_init.unlink()
            print(f"✅ Removed conflicting file: {root_init}")
        except Exception as e:
            print(f"❌ Could not remove {root_init}: {e}")
    else:
        print("✅ No conflicting __init__.py found in root")
    
    # Clean all __pycache__ directories
    pycache_dirs = list(current_dir.rglob("__pycache__"))
    removed_count = 0
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            removed_count += 1
        except Exception as e:
            print(f"⚠️ Could not remove {pycache_dir}: {e}")
    
    if removed_count > 0:
        print(f"✅ Cleaned {removed_count} __pycache__ directories")
    else:
        print("✅ No __pycache__ directories to clean")
    
    # Test the import
    print("\n🧪 Testing pywinauto import...")
    try:
        from pywinauto import Application
        print("✅ pywinauto.Application imported successfully!")
        print("🎉 Fix completed! You can now run the setup again.")
    except Exception as e:
        print(f"❌ Import still failing: {e}")
        print("\n💡 Additional troubleshooting:")
        print("1. Try: pip uninstall pywinauto && pip install pywinauto")
        print("2. Ensure you're in the correct directory")
        print("3. Check if there are any other __init__.py files in the pywinauto folder")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
