#!/usr/bin/env python3
"""
Simple GitHub Actions Connection Test
Tests basic framework functionality without requiring POS application
"""
import sys
import os
import json
from datetime import datetime

def test_basic_imports():
    """Test that all basic imports work"""
    print("Testing basic imports...")
    try:
        import pytest
        import pywinauto
        print("Core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"Import failed: {e}")
        return False

def test_framework_components():
    """Test framework components"""
    print("Testing framework components...")
    try:
        from data.csv_data_manager import csv_data_manager
        from config.config import Config
        from utils.pos_base import POSAutomation
        
        print("All framework components imported successfully")
        return True
    except ImportError as e:
        print(f"Framework import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        from config.config import Config
        config = Config()
        scenarios = config.list_available_scenarios()
        print(f"Configuration loaded: {len(scenarios)} scenarios found")
        return True
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
