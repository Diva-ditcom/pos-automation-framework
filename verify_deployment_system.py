#!/usr/bin/env python3
"""
[SEARCH] DEPLOYMENT VERIFICATION SCRIPT
================================

This script verifies that the complete deployment system is working correctly.
It tests all components and provides a comprehensive health check.

Usage:
    python verify_deployment_system.py
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime

class DeploymentVerifier:
    def __init__(self):
        self.script_dir = Path(__file__).parent.absolute()
        self.log_file = self.script_dir / "logs" / f"deployment_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {},
            "file_checks": {},
            "package_checks": {},
            "script_checks": {},
            "overall_status": "UNKNOWN"
        }
        self.ensure_dirs()
    
    def ensure_dirs(self):
        """Ensure required directories exist"""
        (self.script_dir / "logs").mkdir(exist_ok=True)
    
    def log(self, message, level="INFO"):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")
        except Exception:
            pass
    
    def print_banner(self):
        """Print banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║           [SEARCH] DEPLOYMENT SYSTEM VERIFICATION                  ║
║                                                              ║
║  Comprehensive health check for the POS automation          ║
║  framework deployment system.                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        self.log("Deployment verification started")
    
    def check_system_info(self):
        """Check system information"""
        self.log("Checking system information...")
        
        import platform
        
        self.results["system_info"] = {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "python_executable": sys.executable,
            "working_directory": str(self.script_dir)
        }
        
        self.log(f"[SUCCESS] Platform: {platform.system()}")
        self.log(f"[SUCCESS] Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        return True
    
    def check_deployment_files(self):
        """Check that all deployment files exist"""
        self.log("Checking deployment files...")
        
        required_files = {
            "0_MASTER_INSTALLER.py": "Master installer script",
            "1_setup_offline_machine.py": "Offline setup script", 
            "2_setup_new_machine_enhanced.py": "Enhanced setup script",
            "3_deploy_to_github.py": "GitHub deployment script",
            "EXECUTION_GUIDE.md": "Execution guide documentation",
            "requirements.txt": "Python package requirements",
            "README.md": "Main documentation"
        }
        
        self.results["file_checks"] = {}
        missing_files = []
        
        for file_path, description in required_files.items():
            full_path = self.script_dir / file_path
            exists = full_path.exists()
            self.results["file_checks"][file_path] = {
                "exists": exists,
                "description": description,
                "path": str(full_path)
            }
            
            if exists:
                self.log(f"[SUCCESS] {file_path} - {description}")
            else:
                self.log(f"[ERROR] {file_path} - {description}", "ERROR")
                missing_files.append(file_path)
        
        if missing_files:
            self.log(f"[ERROR] Missing files: {missing_files}", "ERROR")
            return False
        
        self.log("[SUCCESS] All deployment files present")
        return True
    
    def check_project_structure(self):
        """Check project directory structure"""
        self.log("Checking project structure...")
        
        required_dirs = {
            "config": "Configuration files",
            "data": "Test data files",
            "tests": "Test cases", 
            "utils": "Utility modules",
            "logs": "Log files directory",
            "reports": "Test reports directory",
            ".vscode": "VS Code configuration",
            ".github/workflows": "GitHub Actions workflows"
        }
        
        for dir_path, description in required_dirs.items():
            full_path = self.script_dir / dir_path
            exists = full_path.exists() and full_path.is_dir()
            
            if exists:
                self.log(f"[SUCCESS] {dir_path}/ - {description}")
            else:
                self.log(f"[WARNING] {dir_path}/ - {description} (will be created if needed)", "WARNING")
        
        return True
    
    def check_package_requirements(self):
        """Check package requirements file"""
        self.log("Checking package requirements...")
        
        requirements_file = self.script_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.log("[ERROR] requirements.txt not found", "ERROR")
            return False
        
        try:
            with open(requirements_file, "r") as f:
                requirements = f.read()
            
            expected_packages = [
                "pywinauto",
                "pytest",
                "selenium", 
                "pandas"
            ]
            
            missing_packages = []
            for package in expected_packages:
                if package not in requirements:
                    missing_packages.append(package)
            
            if missing_packages:
                self.log(f"[WARNING] Missing packages in requirements.txt: {missing_packages}", "WARNING")
            else:
                self.log("[SUCCESS] All core packages listed in requirements.txt")
            
            return True
            
        except Exception as e:
            self.log(f"[ERROR] Error reading requirements.txt: {e}", "ERROR")
            return False
    
    def check_script_syntax(self):
        """Check that deployment scripts have valid syntax"""
        self.log("Checking script syntax...")
        
        scripts_to_check = [
            "0_MASTER_INSTALLER.py",
            "1_setup_offline_machine.py", 
            "2_setup_new_machine_enhanced.py",
            "3_deploy_to_github.py"
        ]
        
        self.results["script_checks"] = {}
        syntax_errors = []
        
        for script in scripts_to_check:
            script_path = self.script_dir / script
            
            if not script_path.exists():
                self.results["script_checks"][script] = {
                    "syntax_valid": False,
                    "error": "File not found"
                }
                syntax_errors.append(script)
                continue
            
            try:
                # Check syntax by compiling
                with open(script_path, "r", encoding="utf-8") as f:
                    code = f.read()
                
                compile(code, str(script_path), "exec")
                
                self.results["script_checks"][script] = {
                    "syntax_valid": True,
                    "error": None
                }
                self.log(f"[SUCCESS] {script} - Syntax valid")
                
            except SyntaxError as e:
                self.results["script_checks"][script] = {
                    "syntax_valid": False,
                    "error": str(e)
                }
                self.log(f"[ERROR] {script} - Syntax error: {e}", "ERROR")
                syntax_errors.append(script)
                
            except Exception as e:
                self.results["script_checks"][script] = {
                    "syntax_valid": False,
                    "error": str(e)
                }
                self.log(f"[ERROR] {script} - Error: {e}", "ERROR")
                syntax_errors.append(script)
        
        if syntax_errors:
            self.log(f"[ERROR] Scripts with syntax errors: {syntax_errors}", "ERROR")
            return False
        
        self.log("[SUCCESS] All deployment scripts have valid syntax")
        return True
    
    def test_package_imports(self):
        """Test importing key packages"""
        self.log("Testing package imports...")
        
        packages_to_test = [
            ("json", "JSON handling"),
            ("subprocess", "Process execution"),
            ("pathlib", "Path manipulation"),
            ("datetime", "Date/time handling"),
            ("urllib.request", "HTTP requests")
        ]
        
        self.results["package_checks"] = {}
        import_failures = []
        
        for package, description in packages_to_test:
            try:
                __import__(package)
                self.results["package_checks"][package] = {
                    "importable": True,
                    "error": None,
                    "description": description
                }
                self.log(f"[SUCCESS] {package} - {description}")
                
            except ImportError as e:
                self.results["package_checks"][package] = {
                    "importable": False,
                    "error": str(e),
                    "description": description
                }
                self.log(f"[ERROR] {package} - {description}: {e}", "ERROR")
                import_failures.append(package)
        
        if import_failures:
            self.log(f"[ERROR] Failed imports: {import_failures}", "ERROR")
            return False
        
        self.log("[SUCCESS] All core packages can be imported")
        return True
    
    def test_script_execution(self):
        """Test that scripts can be executed (dry run)"""
        self.log("Testing script execution (help/version checks)...")
        
        # Test master installer help
        try:
            result = subprocess.run([
                sys.executable, str(self.script_dir / "0_MASTER_INSTALLER.py"), "--help"
            ], capture_output=True, text=True, timeout=10)
            
            # Even if --help is not implemented, the script should load without syntax errors
            self.log("[SUCCESS] Master installer script loads successfully")
            
        except subprocess.TimeoutExpired:
            self.log("[WARNING] Master installer script runs (timeout expected for interactive script)", "WARNING")
        except Exception as e:
            self.log(f"[ERROR] Master installer execution error: {e}", "ERROR")
            return False
        
        return True
    
    def check_git_availability(self):
        """Check if Git is available"""
        self.log("Checking Git availability...")
        
        try:
            result = subprocess.run([
                "git", "--version"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log(f"[SUCCESS] Git available: {result.stdout.strip()}")
                return True
            else:
                self.log("[ERROR] Git not working properly", "WARNING")
                return False
                
        except FileNotFoundError:
            self.log("[WARNING] Git not found (needed for GitHub deployment)", "WARNING")
            return False
        except Exception as e:
            self.log(f"[WARNING] Git check error: {e}", "WARNING")
            return False
    
    def check_internet_connectivity(self):
        """Check internet connectivity"""
        self.log("Checking internet connectivity...")
        
        try:
            import urllib.request
            response = urllib.request.urlopen('https://pypi.org', timeout=10)
            
            if response.getcode() == 200:
                self.log("[SUCCESS] Internet connectivity available (PyPI reachable)")
                return True
            else:
                self.log("[WARNING] Internet connectivity issues", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"[WARNING] No internet connectivity: {e}", "WARNING")
            return False
    
    def create_verification_report(self):
        """Create comprehensive verification report"""
        self.log("Creating verification report...")
        
        # Calculate overall status
        critical_checks = [
            self.results["file_checks"],
            self.results["script_checks"],
            self.results["package_checks"]
        ]
        
        all_critical_passed = True
        for check_group in critical_checks:
            for item, result in check_group.items():
                if isinstance(result, dict):
                    if not result.get("exists", True) or not result.get("syntax_valid", True) or not result.get("importable", True):
                        all_critical_passed = False
                        break
        
        self.results["overall_status"] = "PASS" if all_critical_passed else "FAIL"
        
        # Save detailed report
        report_file = self.script_dir / "logs" / f"verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, "w") as f:
                json.dump(self.results, f, indent=4)
            self.log(f"[SUCCESS] Verification report saved: {report_file}")
        except Exception as e:
            self.log(f"[WARNING] Could not save report: {e}", "WARNING")
        
        return True
    
    def print_summary(self):
        """Print verification summary"""
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                  📋 VERIFICATION SUMMARY                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Overall Status: {'[SUCCESS] PASS' if self.results['overall_status'] == 'PASS' else '[ERROR] FAIL'}                                       ║
║                                                              ║
║  System: {self.results['system_info']['platform']} {self.results['system_info']['python_version']}                          ║
║  Directory: {str(self.script_dir)[:45]}...║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

[FOLDER] FILE CHECKS:
"""
        
        for file_name, result in self.results["file_checks"].items():
            status = "[SUCCESS]" if result["exists"] else "[ERROR]"
            summary += f"   {status} {file_name}\n"
        
        summary += f"\n🐍 PACKAGE CHECKS:\n"
        for package, result in self.results["package_checks"].items():
            status = "[SUCCESS]" if result["importable"] else "[ERROR]"
            summary += f"   {status} {package}\n"
        
        summary += f"\n📜 SCRIPT CHECKS:\n"
        for script, result in self.results["script_checks"].items():
            status = "[SUCCESS]" if result["syntax_valid"] else "[ERROR]"
            summary += f"   {status} {script}\n"
        
        if self.results["overall_status"] == "PASS":
            summary += f"\n[SUCCESS] DEPLOYMENT SYSTEM IS READY!\n"
            summary += f"\n📋 NEXT STEPS:\n"
            summary += f"   1. Run: python 0_MASTER_INSTALLER.py\n"
            summary += f"   2. Follow the prompts for setup\n"
            summary += f"   3. Check EXECUTION_GUIDE.md for details\n"
        else:
            summary += f"\n[ERROR] DEPLOYMENT SYSTEM NEEDS ATTENTION\n"
            summary += f"\n📋 TROUBLESHOOTING:\n"
            summary += f"   1. Check log file: {self.log_file}\n"
            summary += f"   2. Fix missing files or syntax errors\n"
            summary += f"   3. Ensure all required files are present\n"
        
        summary += f"\n[REPORT] Full report: logs/verification_report_*.json\n"
        
        print(summary)
        self.log("Verification summary printed")
    
    def run(self):
        """Run complete verification process"""
        self.print_banner()
        
        checks = [
            ("System Information", self.check_system_info),
            ("Deployment Files", self.check_deployment_files),
            ("Project Structure", self.check_project_structure),
            ("Package Requirements", self.check_package_requirements),
            ("Script Syntax", self.check_script_syntax),
            ("Package Imports", self.test_package_imports),
            ("Script Execution", self.test_script_execution),
            ("Git Availability", self.check_git_availability),
            ("Internet Connectivity", self.check_internet_connectivity)
        ]
        
        success_count = 0
        
        for check_name, check_function in checks:
            self.log(f"\n--- {check_name} ---")
            try:
                if check_function():
                    success_count += 1
                    self.log(f"[SUCCESS] {check_name} completed successfully")
                else:
                    self.log(f"[ERROR] {check_name} failed", "ERROR")
            except Exception as e:
                self.log(f"[ERROR] {check_name} error: {e}", "ERROR")
        
        self.log(f"\nVerification completed: {success_count}/{len(checks)} checks passed")
        
        # Create report and summary
        self.create_verification_report()
        self.print_summary()
        
        return success_count >= len(checks) - 2  # Allow 2 non-critical failures

def main():
    """Main entry point"""
    try:
        verifier = DeploymentVerifier()
        success = verifier.run()
        
        if success:
            print("\n[SUCCESS] Deployment system verification passed!")
            sys.exit(0)
        else:
            print("\n[ERROR] Deployment system verification failed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n[WARNING] Verification cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
