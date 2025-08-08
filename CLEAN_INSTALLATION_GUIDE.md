# POS Automation Framework - Clean Installation Guide

This guide provides Unicode-free, Windows-compatible installation instructions for machines with or without internet access.

## Quick Start (Choose Your Scenario)

### Scenario A: Machine with Internet Access

1. **Download/Clone the Framework**
   ```
   git clone <repository-url>
   cd pywinauto
   ```

2. **Run Clean Installer**
   ```
   install_clean.bat
   ```
   OR
   ```
   python install_framework_clean.py
   ```

3. **Verify Installation**
   ```
   python -m pytest tests/ --verbose
   ```

### Scenario B: Offline Machine (No Internet)

#### Step 1: Prepare Packages (on machine WITH internet)
1. Download/clone the framework
2. Run the package downloader:
   ```
   python prepare_offline_packages.py
   ```
3. Copy the entire `offline_packages/` directory

#### Step 2: Install on Offline Machine
1. Copy the framework and `offline_packages/` to the target machine
2. Run the offline installer:
   ```
   install_offline_clean.bat
   ```
   OR
   ```
   cd offline_packages
   python install_offline_packages.py
   ```

## Installation Files (Unicode-Free)

| File | Purpose | When to Use |
|------|---------|-------------|
| `install_clean.bat` | Main Windows installer | Machine with internet |
| `install_framework_clean.py` | Python installer script | Cross-platform |
| `prepare_offline_packages.py` | Download packages for offline use | Machine with internet |
| `install_offline_clean.bat` | Offline Windows installer | Machine without internet |

## Common Issues and Solutions

### Issue 1: Unicode/Encoding Errors
**Symptoms:** Characters like ✅, ❌, 🔧 cause crashes
**Solution:** Use the "clean" installers that only use ASCII characters

### Issue 2: Network Connection Failures
**Symptoms:** pip install fails with connection errors
**Solution:** Use offline installation method

### Issue 3: Permission Errors
**Symptoms:** Access denied when installing packages
**Solutions:**
- Run command prompt as Administrator
- Use `--user` flag: `python -m pip install --user -r requirements.txt`
- Use virtual environment

### Issue 4: Python Not Found
**Symptoms:** 'python' is not recognized
**Solutions:**
- Install Python from python.org
- Add Python to PATH environment variable
- Use `py` instead of `python` on Windows

## Verification Commands

After installation, verify with these commands:

```batch
# Check Python version
python --version

# Check pip
python -m pip --version

# Verify packages
python -c "import pytest; print('pytest: OK')"
python -c "import pywinauto; print('pywinauto: OK')"
python -c "import pandas; print('pandas: OK')"
python -c "import openpyxl; print('openpyxl: OK')"

# Run basic test
python -m pytest tests/ --verbose
```

## Project Structure

```
pywinauto/
├── install_clean.bat                 # Main Windows installer
├── install_framework_clean.py        # Cross-platform installer
├── prepare_offline_packages.py       # Offline package downloader
├── install_offline_clean.bat         # Offline installer
├── requirements.txt                  # Package dependencies
├── tests/                           # Test files
│   └── pos_automation/
├── config/                          # Configuration files
├── data/                           # Test data and CSV files
├── offline_packages/               # Downloaded packages (after running prepare_offline_packages.py)
└── README.md                       # Main documentation
```

## Advanced Installation Options

### Virtual Environment (Recommended)
```batch
# Create virtual environment
python -m venv pos_automation_env

# Activate virtual environment
pos_automation_env\Scripts\activate.bat

# Install framework
python install_framework_clean.py

# Deactivate when done
deactivate
```

### Manual Installation
```batch
# Install packages individually
python -m pip install pytest
python -m pip install pywinauto
python -m pip install pandas
python -m pip install openpyxl

# Verify
python -c "import pytest, pywinauto, pandas, openpyxl; print('All packages OK')"
```

## Running Tests

### Basic Test Run
```batch
python -m pytest tests/ --verbose
```

### Specific Test File
```batch
python -m pytest tests/pos_automation/test_01_basic_cash_sale.py --verbose
```

### Generate HTML Report
```batch
python -m pytest tests/ --html=reports/test_report.html --self-contained-html
```

## Configuration

1. **Edit Application Settings**
   - File: `data/app_settings.csv`
   - Configure POS application path and settings

2. **Edit Test Scenarios**
   - File: `data/test_scenarios.csv`
   - Modify test data as needed

3. **Update Configuration**
   - File: `config/config.py`
   - Adjust framework settings

## Troubleshooting

### Installation Logs
- Check `installation.log` for detailed installation steps
- Check `installation_report.json` for structured installation data

### Common Fixes

1. **Clear pip cache:**
   ```
   python -m pip cache purge
   ```

2. **Reinstall packages:**
   ```
   python -m pip install --force-reinstall -r requirements.txt
   ```

3. **Check Windows terminal encoding:**
   ```
   chcp 65001
   ```

4. **Update pip:**
   ```
   python -m pip install --upgrade pip
   ```

## Support

If you encounter issues:

1. Check the installation logs
2. Try the offline installation method
3. Use virtual environment
4. Run installation as Administrator
5. Check Python and pip versions

## Success Indicators

Installation is successful when:
- All verification commands pass
- `python -m pytest tests/ --verbose` runs without import errors
- Framework can locate and interact with the POS application
- Test reports are generated in the `reports/` directory

---

This guide ensures reliable installation across different Windows environments while avoiding Unicode/encoding issues.
