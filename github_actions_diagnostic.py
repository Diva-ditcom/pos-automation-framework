#!/usr/bin/env python3
"""
GitHub Actions Diagnostic Tool
Use this to understand what might be failing in GitHub Actions
"""
import sys
import subprocess

def diagnose_local_environment():
    """Check if the same issues might occur in GitHub Actions"""
    print("GitHub Actions Diagnostic Report")
    print("=" * 50)
    
    # Test 1: Python Version
    try:
        import sys
        python_version = sys.version
        print(f"Python Version: {python_version.split()[0]}")
        if sys.version_info >= (3, 8):
            print("   Python version compatible with GitHub Actions")
        else:
            print("   Python version too old for GitHub Actions")
    except Exception as e:
        print(f"Python check failed: {e}")
    
    # Test 2: Core Dependencies
    deps_status = {}
    core_deps = ['pytest', 'pywinauto']
    
    for dep in core_deps:
        try:
            __import__(dep)
            deps_status[dep] = "Available"
        except ImportError:
            deps_status[dep] = "Missing"
    
    print(f"\nDependencies Status:")
    for dep, status in deps_status.items():
        print(f"   {dep}: {status}")
    
    # Test 3: Framework Components
    print(f"\nFramework Components:")
    
    # Setup imports - add current directory to Python path
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Test Config module
    try:
        # Use importlib for dynamic imports to avoid static analysis issues
        import importlib.util
        
        config_path = os.path.join(current_dir, 'config', 'config.py')
        spec = importlib.util.spec_from_file_location("config.config", config_path)
        if spec and spec.loader:
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            Config = getattr(config_module, 'Config', None)
            if Config:
                print("   ✓ Config module loads")
            else:
                print("   ✗ Config class not found in module")
        else:
            print(f"   ✗ Config module spec failed")
    except Exception as e:
        print(f"   ✗ Config module failed: {e}")
    
    # Test CSV data manager
    try:
        csv_manager_path = os.path.join(current_dir, 'data', 'csv_data_manager.py')
        spec = importlib.util.spec_from_file_location("data.csv_data_manager", csv_manager_path)
        if spec and spec.loader:
            csv_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(csv_module)
            csv_data_manager = getattr(csv_module, 'csv_data_manager', None)
            if csv_data_manager and hasattr(csv_data_manager, 'list_available_scenarios'):
                scenarios = csv_data_manager.list_available_scenarios()
                print(f"   ✓ CSV Manager loads ({len(scenarios)} scenarios)")
            else:
                print("   ✗ csv_data_manager object not found or incomplete")
        else:
            print(f"   ✗ CSV Manager module spec failed")
    except Exception as e:
        print(f"   ✗ CSV Manager failed: {e}")
    
    # Test POS Automation module
    try:
        pos_base_path = os.path.join(current_dir, 'utils', 'pos_base.py')
        spec = importlib.util.spec_from_file_location("utils.pos_base", pos_base_path)
        if spec and spec.loader:
            pos_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pos_module)
            POSAutomation = getattr(pos_module, 'POSAutomation', None)
            if POSAutomation:
                print("   ✓ POS Automation module loads")
            else:
                print("   ✗ POSAutomation class not found in module")
        else:
            print(f"   ✗ POS Automation module spec failed")
    except Exception as e:
        print(f"   ✗ POS Automation failed: {e}")
    
    # Test 4: Pytest Discovery
    print(f"\nTest Discovery:")
    try:
        result = subprocess.run(['python', '-m', 'pytest', '--collect-only', '-q'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            test_count = result.stdout.count(' test ')
            print(f"   Pytest can discover tests ({test_count} found)")
        else:
            print(f"   Pytest discovery failed: {result.stderr}")
    except Exception as e:
        print(f"   Pytest test failed: {e}")
    
    print(f"\nSummary:")
    print("   This diagnostic helps identify issues that might occur in GitHub Actions")
    print("   If all items show success, then GitHub Actions should work perfectly")
    print("   If any show failures, those are likely to cause GitHub Actions failures")
    
    return True

if __name__ == "__main__":
    diagnose_local_environment()
    print(f"\nTo check GitHub Actions status:")
    print("   1. Go to: https://github.com/Diva-ditcom/pos-automation-framework")
    print("   2. Click 'Actions' tab")
    print("   3. Look for workflow runs and their status")
    input("\nPress Enter to continue...")
