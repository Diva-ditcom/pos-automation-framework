#!/usr/bin/env python3
"""
GitHub Deployment Script for POS Automation Framework
Handles complete GitHub setup and deployment
"""

import os
import subprocess
import json
from pathlib import Path

class GitHubDeployer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_account = "Diva-ditcom"
        
    def deploy_to_github(self):
        """Complete GitHub deployment process"""
        print("🚀 GitHub Deployment for POS Automation Framework")
        print("=" * 55)
        
        try:
            # Step 1: Check Git installation
            self._check_git_installation()
            
            # Step 2: Configure Git user
            self._configure_git_user()
            
            # Step 3: Initialize or connect repository
            self._setup_repository()
            
            # Step 4: Setup GitHub Actions
            self._setup_github_actions()
            
            # Step 5: Initial commit and push
            self._initial_commit_and_push()
            
            # Step 6: Verify deployment
            self._verify_deployment()
            
            print("\n🎉 GitHub deployment completed successfully!")
            
        except Exception as e:
            print(f"\n❌ GitHub deployment failed: {e}")
            raise
    
    def _check_git_installation(self):
        """Check if Git is installed"""
        print("🔍 Checking Git installation...")
        
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
            print(f"  ✅ {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("Git is not installed. Please install Git first.")
    
    def _configure_git_user(self):
        """Configure Git user credentials"""
        print("👤 Configuring Git user...")
        
        # Check if already configured
        try:
            name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
            email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
            
            if name.returncode == 0 and email.returncode == 0:
                print(f"  ✅ Git user already configured: {name.stdout.strip()} <{email.stdout.strip()}>")
                return
        except:
            pass
        
        # Configure user
        print("  Git user not configured. Please provide details:")
        user_name = input("  Enter your name: ").strip()
        user_email = input("  Enter your email: ").strip()
        
        if user_name and user_email:
            subprocess.run(["git", "config", "user.name", user_name], check=True)
            subprocess.run(["git", "config", "user.email", user_email], check=True)
            print(f"  ✅ Git user configured: {user_name} <{user_email}>")
    
    def _setup_repository(self):
        """Setup GitHub repository"""
        print("📦 Setting up repository...")
        
        # Check if already a Git repository
        if os.path.exists(os.path.join(self.base_dir, ".git")):
            print("  ✅ Git repository already exists")
            return
        
        # Initialize repository
        subprocess.run(["git", "init"], cwd=self.base_dir, check=True)
        print("  ✅ Git repository initialized")
        
        # Setup GitHub remote
        self._setup_github_remote()
    
    def _setup_github_remote(self):
        """Setup GitHub remote repository"""
        print("🌐 Setting up GitHub remote...")
        
        # Get repository details
        account = input(f"  GitHub account [{self.default_account}]: ").strip() or self.default_account
        repo_name = input("  Repository name [pos-automation-framework]: ").strip() or "pos-automation-framework"
        
        # Setup remote
        remote_url = f"https://github.com/{account}/{repo_name}.git"
        
        try:
            subprocess.run(["git", "remote", "add", "origin", remote_url], 
                         cwd=self.base_dir, check=True)
            print(f"  ✅ Remote added: {remote_url}")
        except subprocess.CalledProcessError:
            print(f"  ⚠️ Remote may already exist or repository not found")
            print(f"  💡 Make sure repository exists: {remote_url}")
    
    def _setup_github_actions(self):
        """Ensure GitHub Actions workflow is properly configured"""
        print("⚙️ Setting up GitHub Actions...")
        
        github_dir = os.path.join(self.base_dir, ".github", "workflows")
        workflow_file = os.path.join(github_dir, "simple-test.yml")
        
        if os.path.exists(workflow_file):
            print("  ✅ GitHub Actions workflow already configured")
        else:
            print("  ⚠️ GitHub Actions workflow not found")
            print("  💡 Workflow should be in .github/workflows/ directory")
    
    def _initial_commit_and_push(self):
        """Perform initial commit and push"""
        print("📤 Committing and pushing to GitHub...")
        
        try:
            # Add all files
            subprocess.run(["git", "add", "."], cwd=self.base_dir, check=True)
            
            # Commit
            commit_msg = f"Initial deployment of POS Automation Framework - {Path().cwd().name}"
            subprocess.run(["git", "commit", "-m", commit_msg], 
                         cwd=self.base_dir, check=True)
            
            # Handle SSL if needed
            ssl_verify = input("  Disable SSL verification if needed? (y/n) [n]: ").lower()
            if ssl_verify == 'y':
                subprocess.run(["git", "config", "http.sslVerify", "false"], 
                             cwd=self.base_dir, check=True)
            
            # Push
            subprocess.run(["git", "push", "-u", "origin", "main"], 
                         cwd=self.base_dir, check=True)
            
            # Re-enable SSL
            if ssl_verify == 'y':
                subprocess.run(["git", "config", "http.sslVerify", "true"], 
                             cwd=self.base_dir, check=True)
            
            print("  ✅ Successfully pushed to GitHub")
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Push failed: {e}")
            print("  💡 You may need to:")
            print("    - Create the repository on GitHub first")
            print("    - Setup authentication (token or SSH key)")
            print("    - Check network connectivity")
    
    def _verify_deployment(self):
        """Verify GitHub deployment"""
        print("🔍 Verifying deployment...")
        
        try:
            # Check remote status
            result = subprocess.run(["git", "remote", "-v"], 
                                  cwd=self.base_dir, capture_output=True, text=True, check=True)
            
            if "origin" in result.stdout:
                print("  ✅ Remote repository configured")
                for line in result.stdout.strip().split('\n'):
                    if 'origin' in line:
                        print(f"    {line}")
            
            print("  ✅ Deployment verification completed")
            
        except subprocess.CalledProcessError:
            print("  ⚠️ Could not verify remote status")

if __name__ == "__main__":
    deployer = GitHubDeployer()
    deployer.deploy_to_github()
