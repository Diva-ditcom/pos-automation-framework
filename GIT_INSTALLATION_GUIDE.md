# Git Installation and GitHub Setup Guide

## Your Current Situation:
- ✅ POS Framework installed successfully
- ❌ Git not installed ("'git' is not recognized")
- ❌ SSH directory missing
- ❌ Some Unicode characters still in old scripts

## Quick Fix: Install Git

### Option 1: Use Windows Package Manager (Recommended)
```batch
# Run as Administrator
winget install --id Git.Git -e --source winget
```

### Option 2: Manual Download
1. Go to: https://git-scm.com/download/windows
2. Download "64-bit Git for Windows Setup"
3. Run installer with default settings
4. **Important**: Make sure "Git from the command line" is selected

### Option 3: Use our automated installer
```batch
install_git_auto.bat
```

## After Git Installation:

### Step 1: Restart Command Prompt
Close your current terminal and open a new one to refresh PATH.

### Step 2: Configure Git
```batch
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Create SSH Directory (Fix SSH Error)
```batch
mkdir %USERPROFILE%\.ssh
```

### Step 4: Generate SSH Key
```batch
ssh-keygen -t rsa -b 4096 -C "your.email@example.com" -f "%USERPROFILE%\.ssh\id_rsa"
```
(Press Enter for all prompts to use defaults)

### Step 5: Add SSH Key to GitHub
```batch
# Display your public key
type %USERPROFILE%\.ssh\id_rsa.pub
```
1. Copy the entire output
2. Go to: https://github.com/settings/keys
3. Click "New SSH key"
4. Paste the key and give it a title
5. Click "Add SSH key"

### Step 6: Initialize Repository (if needed)
```batch
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
```

### Step 7: Push to GitHub
```batch
# First try normal push
git push -u origin main

# If SSL issues (corporate network):
git config http.sslVerify false
git push -u origin main
git config http.sslVerify true
```

## Troubleshooting Common Issues:

### Issue 1: "git not recognized" after installation
**Solution**: Restart command prompt or add to PATH:
```batch
set PATH=%PATH%;C:\Program Files\Git\bin;C:\Program Files\Git\cmd
```

### Issue 2: SSL certificate errors
**Solution**: Temporarily disable SSL verification:
```batch
git config http.sslVerify false
git push origin main
git config http.sslVerify true
```

### Issue 3: SSH key generation fails
**Solution**: Create .ssh directory first:
```batch
mkdir %USERPROFILE%\.ssh
```

### Issue 4: Push requires authentication
**Solutions**:
- Use SSH keys (recommended)
- Use Personal Access Token instead of password
- Configure Git credential manager

## Quick Commands for Your Machine:

```batch
# 1. Install Git (choose one method above)
# 2. Restart command prompt
# 3. Run these commands:

git --version
git config --global user.name "Diva-ditcom"
git config --global user.email "mbabu1@cogz.woolworths.com.au"
mkdir %USERPROFILE%\.ssh
ssh-keygen -t rsa -b 4096 -C "mbabu1@cogz.woolworths.com.au" -f "%USERPROFILE%\.ssh\id_rsa"
type %USERPROFILE%\.ssh\id_rsa.pub

# Copy the SSH key output to GitHub settings
# Then:
git add .
git commit -m "Setup complete"
git push origin main
```

## Alternative: Use HTTPS with Token

If SSH is blocked by your corporate network:

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: repo, workflow
4. Copy the token
5. Use token as password when pushing:
```batch
git remote set-url origin https://yourusername:YOUR_TOKEN@github.com/yourusername/your-repo.git
git push origin main
```

## Success Indicators:

✅ `git --version` shows version number  
✅ `git config --global user.name` shows your name  
✅ SSH key exists in `%USERPROFILE%\.ssh\id_rsa.pub`  
✅ `git push origin main` works without errors  

Run `install_git_complete.bat` after Git installation for automated setup!
