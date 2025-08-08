#!/usr/bin/env python3
"""
Test Runner for Diagnostic Scripts
Runs both diagnostic scripts and provides a summary
"""
import subprocess
import sys

def run_script(script_name, description):
    """Run a diagnostic script and return result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                               capture_output=False, text=True)
        success = result.returncode == 0
        return success
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("POS Automation Framework - Diagnostic Test Suite")
    print("="*60)
    
    tests = [
        ("github_actions_diagnostic.py", "GitHub Actions Environment Check"),
        ("github_connection_test.py", "Framework Connection Test")
    ]
    
    results = {}
    
    for script, description in tests:
        print(f"\n[RUNNING] {description}...")
        success = run_script(script, description)
        results[description] = success
        status = "PASS" if success else "FAIL"
        print(f"[RESULT] {description}: {status}")
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL DIAGNOSTIC SUMMARY")
    print('='*60)
    
    all_passed = True
    for test, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test}: {status}")
        if not result:
            all_passed = False
    
    overall = "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED"
    print(f"\nOverall Status: {overall}")
    
    if all_passed:
        print("\nYour framework is ready for GitHub Actions!")
    else:
        print("\nSome issues detected. Check the output above for details.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to continue...")
    sys.exit(exit_code)
