#!/usr/bin/env python3
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
    print("\n1. 🐍 Python Environment:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        results["python_environment"] = True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Incompatible (need 3.8+)")
    
    # Check dependencies
    print("\n2. 📦 Dependencies:")
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
    print("\n3. 🔧 Framework Components:")
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
    print("\n4. ⚙️ Configuration:")
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
    print("\n5. 🧪 Test Discovery:")
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
    print("\n6. 📊 Reports Generation:")
    reports_dir = os.path.join(base_dir, "reports")
    if os.path.exists(reports_dir):
        print("   ✅ Reports directory exists")
        results["reports_generation"] = True
    else:
        print("   ❌ Reports directory missing")
    
    # Summary
    print("\n" + "=" * 45)
    print("📋 VERIFICATION SUMMARY:")
    
    passed = sum(results.values())
    total = len(results)
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {check.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Framework verification PASSED! Ready for use.")
        return True
    else:
        print("⚠️ Framework verification FAILED! Please check missing components.")
        return False

if __name__ == "__main__":
    success = verify_framework()
    sys.exit(0 if success else 1)
