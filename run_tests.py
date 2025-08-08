"""
Test Runner Script for POS Automation Tests
"""
import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """Run all POS automation tests with HTML reporting."""
    
    print("=" * 80)
    print("[LAUNCH] POS AUTOMATION TEST SUITE")
    print("=" * 80)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Ensure we're in the correct directory
    pywinauto_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pywinauto_dir)
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Generate timestamp for unique report names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"reports/pos_automation_report_{timestamp}.html"
    
    # Pytest command with all options
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        "tests/pos_automation/",
        f"--html={report_name}",
        "--self-contained-html",
        "--tb=short",
        "-v",
        "--capture=no",  # Show print statements in real-time
        f"--junitxml=reports/junit_report_{timestamp}.xml"
    ]
    
    print("🧪 Running POS automation test suite...")
    print(f"[REPORT] HTML Report will be saved to: {report_name}")
    print()
    
    try:
        # Run pytest
        result = subprocess.run(pytest_cmd, capture_output=False, text=True)
        
        print()
        print("=" * 80)
        print("[REPORT] TEST EXECUTION COMPLETED")
        print("=" * 80)
        print(f"📅 End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Exit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("[SUCCESS] All tests passed successfully!")
        else:
            print("[ERROR] Some tests failed. Check the report for details.")
        
        print(f"[REPORT] View detailed report: {os.path.abspath(report_name)}")
        
        return result.returncode
        
    except Exception as e:
        print(f"[ERROR] Error running tests: {e}")
        return 1

def run_specific_test(test_name):
    """Run a specific test by name."""
    
    print(f"[TARGET] Running specific test: {test_name}")
    
    # Ensure we're in the correct directory
    pywinauto_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pywinauto_dir)
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"reports/{test_name}_report_{timestamp}.html"
    
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        f"tests/pos_automation/{test_name}.py",
        f"--html={report_name}",
        "--self-contained-html",
        "--tb=short",
        "-v",
        "--capture=no"
    ]
    
    try:
        result = subprocess.run(pytest_cmd, capture_output=False, text=True)
        print(f"[REPORT] Report saved: {os.path.abspath(report_name)}")
        return result.returncode
    except Exception as e:
        print(f"[ERROR] Error running test: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        # Run all tests
        exit_code = run_tests()
    
    sys.exit(exit_code)
