# POS Automation Framework - Data-Driven Testing

A professional, scalable Python automation framework for POS systems using **pywinauto** and **pytest** with **CSV-based data management**.

## 🚀 **Key Features**

- ✅ **Data-Driven Testing**: All test data stored in CSV files for easy maintenance
- ✅ **Scenario-Based Execution**: Tests automatically load appropriate data based on scenario
- ✅ **Professional Structure**: Clean, maintainable code architecture
- ✅ **Flexible Configuration**: Easy to add new scenarios without touching Python code
- ✅ **HTML Reporting**: Professional test reports with detailed results
- ✅ **Cross-Environment**: Easy data management for different environments

## 📁 **Project Structure**

```
pywinauto/
├── config/
│   ├── __init__.py
│   └── config.py              # Data-driven configuration manager
├── data/                      # 📊 CSV Data Files (NEW!)
│   ├── __init__.py
│   ├── csv_data_manager.py    # CSV data management class
│   ├── test_scenarios.csv     # Test scenario data
│   └── app_settings.csv       # Application settings
├── utils/
│   ├── __init__.py
│   └── pos_base.py            # Enhanced POS automation framework
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Data-driven pytest fixtures
│   └── pos_automation/
│       ├── __init__.py
│       ├── test_01_basic_cash_sale.py              # Original tests
│       ├── test_02_promotion_cash_sale.py
│       ├── test_03_loyalty_cash_sale.py
│       └── test_01_basic_cash_sale_data_driven.py  # Data-driven version
├── reports/                   # Test execution reports
├── logs/                      # Test execution logs
├── .vscode/                   # IDE configuration
├── manage_csv_data.py         # 🛠️ Data management utility
├── run_tests.py              # Test runner
├── run_tests.bat             # Batch test runner
├── requirements.txt          # Dependencies
├── pyproject.toml           # Pytest configuration
└── README.md                # This file
```

## 🗂️ **CSV Data Management**

### **Scenario Data (test_scenarios.csv)**
```csv
scenario_name,user_name,password,ean_code,item_name,expected_price,cash_tender_amount,loyalty_number,promotion_code,quantity
basic_cash_sale,cashier01,pass123,9300675084147,Test Product 1,5.99,50.00,,,1
promotion_cash_sale,cashier01,pass123,9300675079686,Promotion Item,12.99,50.00,,PROMO10,2
loyalty_cash_sale,cashier01,pass123,9300675084147,Test Product 1,5.99,50.00,LOY123456789,,1
```

### **Application Settings (app_settings.csv)**
```csv
setting_name,setting_value,description
POS_LAUNCH_PATH,C:\pos\bin\launch.bat,Path to POS application launcher
POS_STARTUP_WAIT,10,Seconds to wait after launching POS
POS_APP_TITLE,POS Application,Title of the POS application window
```

## 🧪 **Test Scenarios**

### **1. Basic Cash Sale** (`basic_cash_sale`)
- Login with user credentials from CSV
- Add single item using EAN from CSV
- Complete transaction with cash amount from CSV

### **2. Promotion Cash Sale** (`promotion_cash_sale`)
- Add multiple promotion items
- Apply promotion code from CSV
- Verify discount calculations
- Complete with cash payment

### **3. Loyalty Cash Sale** (`loyalty_cash_sale`)
- Add item with loyalty integration
- Apply loyalty number from CSV
- Calculate loyalty benefits
- Complete transaction

## 🛠️ **Data Management Utility**

Use the interactive CSV data manager:

```bash
python manage_csv_data.py
```

**Features:**
- 📋 List all scenarios
- 👀 View scenario details
- ➕ Add new scenarios
- ⚙️ View application settings
- ✅ Validate data integrity
- 🧪 Test data loading

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Your Data**
Edit CSV files in the `data/` folder:
- `test_scenarios.csv` - Test data for each scenario
- `app_settings.csv` - Application configuration

### **3. Run Tests**

**All tests:**
```bash
python run_tests.py
```

**Specific scenario:**
```bash
pytest tests/pos_automation/test_01_basic_cash_sale_data_driven.py -v
```

**With HTML report:**
```bash
pytest --html=reports/report.html --self-contained-html
```

## 📈 **Scaling Your Tests**

### **Adding New Scenarios**

1. **Add data to CSV:**
   ```bash
   python manage_csv_data.py
   # Select option 3: Add new scenario
   ```

2. **Create test file (optional):**
   ```python
   @pytest.mark.scenario(name='your_new_scenario')
   def test_your_scenario(self, pos_automation_with_scenario):
       pos = pos_automation_with_scenario
       # Test automatically loads your CSV data
       success = pos.execute_scenario_login()
       success = pos.execute_scenario_add_item()
       success = pos.execute_scenario_payment()
   ```

### **Benefits of This Approach**

- ✅ **No Code Changes**: Add new test data without touching Python files
- ✅ **Environment Flexibility**: Different CSV files for DEV/TEST/PROD
- ✅ **Easy Maintenance**: Business users can update test data
- ✅ **Version Control**: Track data changes alongside code
- ✅ **Reusable Framework**: Same code works for all scenarios

## 🔧 **Configuration**

### **Data-Driven Config Class**
```python
config = Config()

# Automatically loads from CSV
launch_path = config.POS_LAUNCH_PATH
scenario_data = config.get_scenario_data('basic_cash_sale')
user_creds = config.get_user_credentials('basic_cash_sale')
```

### **Scenario-Based Automation**
```python
# Initialize with scenario
pos = POSAutomation('basic_cash_sale')

# Execute using CSV data
pos.execute_scenario_login()      # Uses CSV credentials
pos.execute_scenario_add_item()   # Uses CSV EAN/item data
pos.execute_scenario_payment()    # Uses CSV payment data
```

## 📊 **Reports & Logging**

- **HTML Reports**: `reports/report.html`
- **Execution Logs**: `logs/`
- **Screenshots**: Automatic on test failures

## 🤝 **Best Practices**

1. **Keep CSV files simple**: One row per scenario
2. **Use descriptive scenario names**: `basic_cash_sale`, `bulk_discount_sale`
3. **Validate data regularly**: Use `manage_csv_data.py` utility
4. **Version control CSV files**: Track data changes
5. **Environment-specific data**: Different CSV files per environment

---

**🎯 Result**: A truly scalable, data-driven POS automation framework where adding new test scenarios is as simple as adding a row to a CSV file!
