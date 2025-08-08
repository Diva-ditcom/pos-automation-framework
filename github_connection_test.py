#!/usr/bin/env python3
"""
Simple GitHub Actions Connection Test
Tests basic framework functionality without requiring POS application
"""
import sys
import os
import json
from datetime import datetime
import importlib.util

# Setup Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def safe_import(module_name, package_name=None):
    """Safely import a module with error handling"""
    try:
        if package_name:
            # For local framework modules
            module_path = os.path.join(current_dir, package_name, f"{module_name}.py")
            if os.path.exists(module_path):
                spec = importlib.util.spec_from_file_location(f"{package_name}.{module_name}", module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return module
        else:
            # For external packages
            return __import__(module_name)
    except Exception:
        return None
    return None

def test_basic_imports():
    """Test that all basic imports work"""
    print("Testing basic imports...")
    try:
        # Test external dependencies
        pytest = safe_import('pytest')
        pywinauto = safe_import('pywinauto')
        
        if pytest and pywinauto:
            print("Core dependencies imported successfully")
            return True
        else:
            missing = []
            if not pytest: missing.append('pytest')
            if not pywinauto: missing.append('pywinauto')
            print(f"Missing dependencies: {', '.join(missing)}")
            return False
    except Exception as e:
        print(f"Import failed: {e}")
        return False

def test_framework_components():
    """Test framework components"""
    print("Testing framework components...")
    try:
        # Test framework imports using safe_import
        csv_module = safe_import('csv_data_manager', 'data')
        config_module = safe_import('config', 'config')
        pos_module = safe_import('pos_base', 'utils')
        
        if csv_module and config_module and pos_module:
            print("All framework components imported successfully")
            return True
        else:
            missing = []
            if not csv_module: missing.append('data.csv_data_manager')
            if not config_module: missing.append('config.config')
            if not pos_module: missing.append('utils.pos_base')
            print(f"Missing framework components: {', '.join(missing)}")
            return False
    except Exception as e:
        print(f"Framework import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        config_module = safe_import('config', 'config')
        if config_module and hasattr(config_module, 'Config'):
            Config = getattr(config_module, 'Config')
            config = Config()
            scenarios = config.list_available_scenarios()
            print(f"Configuration loaded: {len(scenarios)} scenarios found")
            return True
        else:
            print("Config class not found")
            return False
    except Exception as e:
        print(f"Configuration test failed: {e}")
        return False

def test_pytest_discovery():
    """Test pytest can discover tests"""
    print("Testing pytest discovery...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", "-q"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            test_count = result.stdout.count(" test ")
            print(f"Pytest discovered tests successfully")
            return True
        else:
            print(f"Pytest discovery failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Pytest test failed: {e}")
        return False

def generate_report(results):
    """Generate a simple test report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "platform": sys.platform,
        "test_results": results,
        "overall_status": "PASS" if all(results.values()) else "FAIL"
    }
    
    # Save JSON report
    with open("github_connection_test.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Save text report
    with open("github_connection_test.txt", "w", encoding='utf-8') as f:
        f.write("GitHub Actions Connection Test Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp: {report['timestamp']}\n")
        f.write(f"Python Version: {report['python_version']}\n")
        f.write(f"Platform: {report['platform']}\n")
        f.write(f"Overall Status: {report['overall_status']}\n")
        f.write("\nTest Results:\n")
        for test, result in results.items():
            status = "PASS" if result else "FAIL"
            f.write(f"  {test}: {status}\n")
    
    print(f"\nReport generated: Overall Status = {report['overall_status']}")
    return report

def main():
    """Main test function"""
    print("GitHub Actions Connection Test")
    print("=" * 50)
    
    # Run all tests
    results = {
        "basic_imports": test_basic_imports(),
        "framework_components": test_framework_components(),
        "configuration": test_configuration(),
        "pytest_discovery": test_pytest_discovery()
    }
    
    # Generate report
    report = generate_report(results)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    for test, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall Status: {report['overall_status']}")
    
    # Return appropriate exit code
    return 0 if report['overall_status'] == "PASS" else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
