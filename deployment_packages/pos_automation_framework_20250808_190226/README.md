# POS Automation Framework - Deployment Package

## 🎯 Quick Start

### Option 1: One-Click Installation (Recommended)
**Windows:**
```batch
INSTALL.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation
```bash
python setup_new_machine_enhanced.py
```

### Option 3: GitHub Deployment
```bash
python deploy_to_github.py
```

## 📋 What's Included

### Core Framework Files
- `config/` - Framework configuration
- `data/` - CSV data and test scenarios  
- `tests/` - Test cases and automation scripts
- `utils/` - POS automation utilities
- `reports/` - Test execution reports
- `.github/` - GitHub Actions workflow

### Setup Scripts
- `INSTALL.bat` / `install.sh` - One-click installers
- `setup_new_machine_enhanced.py` - Enhanced machine setup
- `deploy_to_github.py` - GitHub deployment
- `verify_installation.py` - Installation verification

### Diagnostic Tools
- `run_all_diagnostics.py` - Complete framework validation
- `github_actions_diagnostic.py` - CI/CD environment check
- `github_connection_test.py` - GitHub connectivity test

### Development Tools
- `pos-automation.code-workspace` - VS Code workspace
- `import_helper.py` - Development import utilities

## 🔧 System Requirements

- **Python**: 3.8+ (3.11+ recommended)
- **OS**: Windows 10+, Linux, macOS
- **Memory**: 4GB+ RAM
- **Storage**: 500MB+ free space

## 📦 Installation Process

1. **Extract** the deployment package
2. **Run** one-click installer or setup script
3. **Verify** installation with verification script
4. **Deploy** to GitHub (optional)
5. **Start** automating POS testing!

## 🧪 Verification

After installation, verify everything works:
```bash
python verify_installation.py
```

## 🚀 GitHub Deployment

Deploy to your GitHub account:
```bash
python deploy_to_github.py
```

Default settings:
- Account: `Diva-ditcom`
- Repository: `pos-automation-framework`
- Branch: `main`

## 📊 Running Tests

Execute all test cases:
```bash
python -m pytest tests/ -v --html=reports/test_report.html
```

## 🔍 Troubleshooting

### Common Issues

**Python not found:**
- Install Python 3.8+ from python.org
- Add Python to system PATH

**Dependencies missing:**
- Run: `pip install -r requirements.txt`

**POS connection failed:**
- Normal behavior without POS application
- Configure POS path in `config/config.py`

**GitHub push failed:**
- Check repository exists on GitHub
- Verify authentication (token/SSH)
- Check network connectivity

## 📞 Support

1. Run diagnostics: `python run_all_diagnostics.py`
2. Check verification: `python verify_installation.py`  
3. Review reports in `reports/` directory
4. Check GitHub Actions in repository

## 🎉 Success Indicators

✅ All diagnostic tests pass  
✅ Framework components load correctly  
✅ Test discovery finds test cases  
✅ HTML reports generated  
✅ GitHub Actions workflow runs  

Package created: 2025-08-08 19:02:27
