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
    
    try:
        from config.config import Config
        print("   Config module loads")
    except Exception as e:
        print(f"   Config module failed: {e}")
    
    try:
        from data.csv_data_manager import csv_data_manager
        scenarios = csv_data_manager.list_available_scenarios()
        print(f"   CSV Manager loads ({len(scenarios)} scenarios)")
    except Exception as e:
        print(f"   CSV Manager failed: {e}")
    
    try:
        from utils.pos_base import POSAutomation
        print("   POS Automation module loads")
    except Exception as e:
        print(f"   POS Automation failed: {e}")
    
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
