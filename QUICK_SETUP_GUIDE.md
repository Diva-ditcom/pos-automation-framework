# 🚀 POS Automation Framework - Quick Setup Commands

## 📦 **OFFLINE MACHINE SETUP (Firewall/Corporate Environment)**

### **Step 1: Prepare Offline Packages (Run on internet machine)**
```bash
cd C:\path\to\pywinauto
python download_offline_packages.py
```

### **Step 2: Copy Framework to Target Machine**
```bash
# Copy entire pywinauto folder to new machine
# Ensure offline_packages/ folder is included (16 wheel files)
```

### **Step 3: Setup on Target Machine (No Internet Required)**
```bash
cd C:\new\path\to\pywinauto
python setup_offline_machine.py
# Select option 1: Offline installation
```

### **Step 4: Configure for Your Environment**
```bash
# Edit CSV files (no Python code changes needed)
notepad data\app_settings.csv    # Update POS application path
notepad data\test_scenarios.csv  # Update test data if needed
```

### **Step 5: Verify Installation**
```bash
python run_tests.py
```

---

## 🌐 **ONLINE MACHINE SETUP (Internet Available)**

### **Step 1: Copy Framework to Target Machine**
```bash
# Copy pywinauto folder to new machine
```

### **Step 2: Run Setup (Downloads packages automatically)**
```bash
cd C:\new\path\to\pywinauto
python setup_new_machine.py
```

### **Step 3: Configure for Your Environment**
```bash
# Edit CSV files (no Python code changes needed)
notepad data\app_settings.csv    # Update POS application path
notepad data\test_scenarios.csv  # Update test data if needed
```

### **Step 4: Verify Installation**
```bash
python run_tests.py
```

---

## 📝 **CONFIGURATION CHANGES REQUIRED**

### **🎯 File 1: data\app_settings.csv**
```csv
setting_name,setting_value,description
POS_LAUNCH_PATH,C:\YOUR_POS_PATH\launch.bat,← CHANGE THIS
POS_STARTUP_WAIT,10,← Adjust timing if needed
POS_APP_TITLE,Your POS Window Title,← CHANGE IF DIFFERENT
DEFAULT_TIMEOUT,30,← Adjust if needed
SCREENSHOT_ON_FAILURE,true,Keep as is
REPORT_TITLE,POS Automation Test Report,Keep as is
```

**Required Changes:**
- **POS_LAUNCH_PATH**: Change `C:\pos\bin\launch.bat` to your actual POS launcher path
- **POS_APP_TITLE**: Change `POS Application` to your actual POS window title

### **🎯 File 2: data\test_scenarios.csv (Optional)**
```csv
scenario_name,user_name,password,ean_code,item_name,expected_price,cash_tender_amount,loyalty_number,promotion_code,quantity
basic_cash_sale,YOUR_USERNAME,YOUR_PASSWORD,YOUR_EAN_CODE,Your Product,5.99,50.00,,,1
promotion_cash_sale,YOUR_USERNAME,YOUR_PASSWORD,YOUR_PROMO_EAN,Promo Product,12.99,50.00,,PROMO10,2
loyalty_cash_sale,YOUR_USERNAME,YOUR_PASSWORD,YOUR_EAN_CODE,Your Product,5.99,50.00,YOUR_LOYALTY_NUM,,1
```

**Optional Changes:**
- **user_name, password**: Update with your POS login credentials
- **ean_code**: Update with your actual product EAN codes
- **item_name**: Update with your actual product names
- **cash_tender_amount**: Update with your preferred test amounts

---

## ✅ **NO CODE CHANGES NEEDED!**

**Important**: You do NOT need to modify any Python (.py) files! All configuration is done through CSV files.

The framework automatically:
- ✅ Loads settings from CSV files
- ✅ Uses relative paths for imports
- ✅ Adapts to any folder location
- ✅ Works with your specific POS application

---

## 🧪 **Testing Your Setup**

### **Quick Validation Commands:**
```bash
# Test CSV data loading
python -c "from data.csv_data_manager import csv_data_manager; print('Scenarios:', csv_data_manager.list_available_scenarios())"

# Test configuration loading  
python -c "from config.config import Config; c=Config(); print('POS Path:', c.POS_LAUNCH_PATH)"

# Test framework components
python -c "from utils.pos_base import POSAutomation; print('Framework loaded successfully')"

# Run actual tests
python run_tests.py
```

---

## 🎯 **Summary: What You Need to Do**

### **For ANY new machine:**
1. **Copy** pywinauto folder to new location
2. **Run** appropriate setup script (offline or online)  
3. **Edit** data\app_settings.csv with your POS path
4. **Edit** data\test_scenarios.csv with your test data (optional)
5. **Test** with python run_tests.py

### **Files to Run:**
- **Offline**: `python setup_offline_machine.py`
- **Online**: `python setup_new_machine.py`  

### **Files to Edit:**
- **data\app_settings.csv** (required)
- **data\test_scenarios.csv** (optional)

**That's it! No Python code modifications needed!** 🚀
