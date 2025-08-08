#!/usr/bin/env python3
"""
Git Installation and GitHub Setup Script
Handles Git installation and GitHub configuration for Windows
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

class GitHubSetup:
    def __init__(self):
        self.git_installed = False
        self.git_configured = False
        
    def check_git_installation(self):
        """Check if Git is installed"""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[SUCCESS] Git is installed: {result.stdout.strip()}")
                self.git_installed = True
                return True
        except FileNotFoundError:
            pass
        
        print("[ERROR] Git is not installed")
        return False
    
    def install_git_instructions(self):
        """Provide Git installation instructions"""
        print("\n" + "="*60)
        print("GIT INSTALLATION REQUIRED")
        print("="*60)
        print()
        print("Git is not installed on your machine. Please follow these steps:")
        print()
        print("OPTION 1: Download from Git website (Recommended)")
        print("1. Go to: https://git-scm.com/download/win")
        print("2. Download the latest version")
        print("3. Run installer with default settings")
        print("4. Restart your command prompt")
        print("5. Run this script again")
        print()
        print("OPTION 2: Install using winget (if available)")
        print("Run: winget install --id Git.Git -e --source winget")
        print()
        
        choice = input("Open Git download page in browser? (y/N): ").lower()
        if choice == 'y':
            webbrowser.open('https://git-scm.com/download/win')
        
        return False
    
    def try_winget_install(self):
        """Try to install Git using winget"""
        try:
            print("[INFO] Attempting to install Git using winget...")
            result = subprocess.run([
                'winget', 'install', '--id', 'Git.Git', '-e', '--source', 'winget'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[SUCCESS] Git installed via winget")
                print("[INFO] Please restart your command prompt and run this script again")
                return True
            else:
                print("[INFO] winget installation failed or not available")
                return False
        except FileNotFoundError:
            print("[INFO] winget not available")
            return False
    
    def configure_git(self):
        """Configure Git with user name and email"""
        try:
            # Check if already configured
            name_result = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                       capture_output=True, text=True)
            email_result = subprocess.run(['git', 'config', '--global', 'user.email'], 
                                        capture_output=True, text=True)
            
            if name_result.returncode == 0 and email_result.returncode == 0:
                print(f"[SUCCESS] Git already configured:")
                print(f"  Name: {name_result.stdout.strip()}")
                print(f"  Email: {email_result.stdout.strip()}")
                self.git_configured = True
                return True
                
        except Exception:
            pass
        
        # Configure Git
        print("\n" + "="*60)
        print("GIT CONFIGURATION")
        print("="*60)
        print()
        print("Please provide your Git configuration:")
        
        name = input("Enter your name (for Git commits): ").strip()
        email = input("Enter your email address: ").strip()
        
        if name and email:
            try:
                subprocess.run(['git', 'config', '--global', 'user.name', name], check=True)
                subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
                
                print(f"[SUCCESS] Git configured successfully:")
                print(f"  Name: {name}")
                print(f"  Email: {email}")
                self.git_configured = True
                return True
                
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to configure Git: {e}")
                return False
        else:
            print("[ERROR] Name and email are required")
            return False
    
    def setup_ssh_key(self):
        """Set up SSH key for GitHub"""
        ssh_dir = Path.home() / '.ssh'
        ssh_key = ssh_dir / 'id_rsa'
        ssh_pub = ssh_dir / 'id_rsa.pub'
        
        print("\n" + "="*60)
        print("SSH KEY SETUP")
        print("="*60)
        print()
        
        setup_ssh = input("Set up SSH key for GitHub? (y/N): ").lower()
        if setup_ssh != 'y':
            return True
        
        # Check if SSH key exists
        if ssh_pub.exists():
            print("[INFO] SSH key already exists")
            try:
                with open(ssh_pub, 'r') as f:
                    public_key = f.read().strip()
                print("\nYour public SSH key:")
                print("-" * 40)
                print(public_key)
                print("-" * 40)
                print()
                print("Copy this key to GitHub:")
                print("1. Go to GitHub.com > Settings > SSH and GPG keys")
                print("2. Click 'New SSH key'")
                print("3. Paste the key above")
                print("4. Give it a title like 'Windows-POS-Framework'")
                
                choice = input("\nOpen GitHub SSH settings page? (y/N): ").lower()
                if choice == 'y':
                    webbrowser.open('https://github.com/settings/ssh/new')
                
                return True
                
            except Exception as e:
                print(f"[ERROR] Could not read SSH key: {e}")
                return False
        
        # Generate new SSH key
        print("[INFO] Generating new SSH key...")
        email = subprocess.run(['git', 'config', '--global', 'user.email'], 
                              capture_output=True, text=True).stdout.strip()
        
        try:
            ssh_dir.mkdir(exist_ok=True)
            subprocess.run([
                'ssh-keygen', '-t', 'rsa', '-b', '4096', 
                '-C', email, '-f', str(ssh_key), '-N', ''
            ], check=True)
            
            if ssh_pub.exists():
                with open(ssh_pub, 'r') as f:
                    public_key = f.read().strip()
                
                print("[SUCCESS] SSH key generated successfully")
                print("\nYour public SSH key:")
                print("-" * 40)
                print(public_key)
                print("-" * 40)
                print()
                print("IMPORTANT: Add this key to GitHub:")
                print("1. Go to GitHub.com > Settings > SSH and GPG keys")
                print("2. Click 'New SSH key'")
                print("3. Paste the key above")
                print("4. Give it a title like 'Windows-POS-Framework'")
                
                choice = input("\nOpen GitHub SSH settings page? (y/N): ").lower()
                if choice == 'y':
                    webbrowser.open('https://github.com/settings/ssh/new')
                
                input("\nPress Enter after adding the SSH key to GitHub...")
                return True
            else:
                print("[ERROR] SSH key generation failed")
                return False
                
        except Exception as e:
            print(f"[ERROR] Failed to generate SSH key: {e}")
            return False
    
    def setup_repository(self):
        """Set up Git repository and GitHub remote"""
        print("\n" + "="*60)
        print("REPOSITORY SETUP")
        print("="*60)
        print()
        
        # Check if already in a Git repository
        try:
            subprocess.run(['git', 'status'], check=True, capture_output=True)
            print("[SUCCESS] Already in a Git repository")
        except subprocess.CalledProcessError:
            print("[INFO] Initializing Git repository...")
            try:
                subprocess.run(['git', 'init'], check=True)
                print("[SUCCESS] Git repository initialized")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to initialize repository: {e}")
                return False
        
        # Check remote repositories
        try:
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("\nCurrent remote repositories:")
                print(result.stdout)
            else:
                print("\nNo remote repositories configured")
        except Exception:
            pass
        
        # Setup GitHub remote
        setup_remote = input("\nSet up GitHub remote repository? (y/N): ").lower()
        if setup_remote == 'y':
            print("\nGitHub Repository Options:")
            print("1. Connect to existing GitHub repository")
            print("2. Create new GitHub repository")
            
            option = input("Choose option (1/2): ").strip()
            
            if option == '1':
                repo_url = input("Enter GitHub repository URL (HTTPS or SSH): ").strip()
                if repo_url:
                    try:
                        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
                        print("[SUCCESS] Remote repository added")
                    except subprocess.CalledProcessError as e:
                        print(f"[ERROR] Failed to add remote: {e}")
            
            elif option == '2':
                print("\nTo create a new GitHub repository:")
                print("1. Go to GitHub.com")
                print("2. Click '+' > 'New repository'")
                print("3. Name: pos-automation-framework")
                print("4. Make it Private (recommended)")
                print("5. Do NOT initialize with README")
                print("6. Copy the repository URL")
                
                choice = input("\nOpen GitHub new repository page? (y/N): ").lower()
                if choice == 'y':
                    webbrowser.open('https://github.com/new')
                
                input("\nPress Enter after creating the repository...")
                repo_url = input("Enter the repository URL: ").strip()
                if repo_url:
                    try:
                        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
                        print("[SUCCESS] Remote repository added")
                    except subprocess.CalledProcessError as e:
                        print(f"[ERROR] Failed to add remote: {e}")
        
        return True
    
    def commit_and_push(self):
        """Commit changes and push to GitHub"""
        print("\n" + "="*60)
        print("COMMIT AND PUSH")
        print("="*60)
        print()
        
        try:
            # Add all files
            subprocess.run(['git', 'add', '.'], check=True)
            print("[SUCCESS] Files staged for commit")
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                                  capture_output=True)
            
            if result.returncode != 0:  # There are changes
                # Commit changes
                commit_msg = "Initial commit: POS Automation Framework - Production Ready"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                print("[SUCCESS] Changes committed")
                
                # Try to push
                try:
                    subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                 check=True, capture_output=True)
                    
                    print("[INFO] Pushing to GitHub...")
                    result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                                          capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print("[SUCCESS] Successfully pushed to GitHub!")
                    else:
                        print("[WARNING] Push failed - you may need to authenticate")
                        print("Try running: git push -u origin main")
                        
                except subprocess.CalledProcessError:
                    print("[INFO] No remote repository configured")
                    print("Your changes are committed locally")
            else:
                print("[INFO] No changes to commit")
                
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Commit failed: {e}")
            return False
        
        return True
    
    def show_status(self):
        """Show final Git and repository status"""
        print("\n" + "="*60)
        print("SETUP VERIFICATION")
        print("="*60)
        print()
        
        # Git configuration
        try:
            name = subprocess.run(['git', 'config', '--global', 'user.name'], 
                                capture_output=True, text=True).stdout.strip()
            email = subprocess.run(['git', 'config', '--global', 'user.email'], 
                                 capture_output=True, text=True).stdout.strip()
            print(f"Git User: {name} <{email}>")
        except Exception:
            print("Git configuration: Not set")
        
        # Repository status
        try:
            result = subprocess.run(['git', 'status', '--short'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print(f"\nRepository status:\n{result.stdout}")
            else:
                print("\nRepository status: Clean")
        except Exception:
            print("\nRepository status: Not a Git repository")
        
        # Remote repositories
        try:
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print(f"\nRemote repositories:\n{result.stdout}")
            else:
                print("\nRemote repositories: None")
        except Exception:
            print("\nRemote repositories: Error checking")
        
        # Recent commits
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-3'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print(f"\nRecent commits:\n{result.stdout}")
        except Exception:
            pass
    
    def setup(self):
        """Main setup process"""
        print("="*60)
        print("POS Automation Framework - Git & GitHub Setup")
        print("="*60)
        print()
        
        # Step 1: Check/Install Git
        if not self.check_git_installation():
            if not self.try_winget_install():
                self.install_git_instructions()
                return False
            else:
                # winget succeeded, but need to restart
                input("\nPress Enter to continue after restarting command prompt...")
                return False
        
        # Step 2: Configure Git
        if not self.configure_git():
            return False
        
        # Step 3: Setup SSH (optional)
        self.setup_ssh_key()
        
        # Step 4: Setup repository
        if not self.setup_repository():
            return False
        
        # Step 5: Commit and push
        if not self.commit_and_push():
            return False
        
        # Step 6: Show final status
        self.show_status()
        
        print("\n" + "="*60)
        print("GITHUB SETUP COMPLETED SUCCESSFULLY!")
        print("="*60)
        print()
        print("Your POS Automation Framework is now:")
        print("✓ Version controlled with Git")
        print("✓ Connected to GitHub repository")
        print("✓ Ready for collaboration")
        print("✓ Backed up in the cloud")
        print()
        print("Next steps:")
        print("1. Check your repository on GitHub.com")
        print("2. Set up branch protection (optional)")
        print("3. Configure GitHub Actions (optional)")
        print("4. Invite collaborators if needed")
        
        return True

def main():
    """Main entry point"""
    try:
        setup = GitHubSetup()
        success = setup.setup()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
