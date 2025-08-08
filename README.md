# POS Automation Test Suite

A comprehensive automated testing framework for POS (Point of Sale) system operations using pytest and pywinauto.

## 🏗️ Project Structure

```
automation/Scripts/pywinauto/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── config.py          # Test configuration and settings
├── utils/                  # Utility modules
│   ├── __init__.py
│   └── pos_base.py        # Base POS automation class
├── tests/                  # Test files
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and configuration
│   └── pos_automation/    # POS automation test cases
│       ├── __init__.py
│       ├── test_01_basic_cash_sale.py       # Basic item addition and cash sale
│       ├── test_02_promotion_cash_sale.py   # Multiple items with promotion
│       └── test_03_loyalty_cash_sale.py     # Loyalty integration testing
├── reports/               # Generated HTML and XML reports
├── logs/                 # Test execution logs
├── pyproject.toml        # Pytest configuration
├── requirements.txt      # Python dependencies
├── run_tests.py         # Test runner script
├── run_tests.bat        # Windows batch runner
├── README.md           # This file
├── 01_additem_completewithCash.py      # Original automation script 1
├── 02_addtems_promotion_cashSale.py    # Original automation script 2
└── 03_additem_Withloyalty_cashSal.py  # Original automation script 3
```

## 🧪 Test Scenarios

### Test Case 1: Basic Cash Sale (`test_01_basic_cash_sale.py`)
- **Scenario**: Add single item and complete with cash payment
- **Original Script**: Based on `01_additem_completewithCash.py`
- **Steps**: Add product → Verify basket → Handle loyalty popup → Complete cash tender
- **Markers**: `@pytest.mark.smoke`, `@pytest.mark.cash_flow`

### Test Case 2: Promotion Cash Sale (`test_02_promotion_cash_sale.py`)
- **Scenario**: Add multiple items with promotion analysis
- **Original Script**: Based on `02_addtems_promotion_cashSale.py`
- **Steps**: Add promotion items (x2) → Analyze promotions → Complete cash tender
- **Markers**: `@pytest.mark.regression`, `@pytest.mark.promotion`, `@pytest.mark.cash_flow`

### Test Case 3: Loyalty Cash Sale (`test_03_loyalty_cash_sale.py`)
- **Scenario**: Item addition with loyalty program integration
- **Original Script**: Based on `03_additem_Withloyalty_cashSal.py`
- **Steps**: Add product → Loyalty integration → Complete cash tender
- **Markers**: `@pytest.mark.regression`, `@pytest.mark.loyalty`, `@pytest.mark.cash_flow`

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Windows OS
- POS application (R10PosClient)
- Virtual environment at `C:\Myapps\wow\vibecoding\automation`

### Installation
1. Navigate to pywinauto directory:
   ```bash
   cd C:\Myapps\wow\vibecoding\automation\Scripts\pywinauto
   ```

2. Install dependencies (if not already installed in virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

#### Run All Tests
```bash
python run_tests.py
```

#### Run Specific Test
```bash
python run_tests.py test_01_basic_cash_sale
python run_tests.py test_02_promotion_cash_sale
python run_tests.py test_03_loyalty_cash_sale
```

#### Run Tests by Markers
```bash
python -m pytest -m smoke                    # Run only smoke tests
python -m pytest -m "cash_flow and promotion" # Run promotion cash flow tests
python -m pytest -m regression               # Run regression tests
```

#### Direct Pytest Commands
```bash
# Run with HTML report
python -m pytest tests/pos_automation/ --html=reports/report.html --self-contained-html

# Run with verbose output
python -m pytest tests/pos_automation/ -v

# Run specific test file
python -m pytest tests/pos_automation/test_01_basic_cash_sale.py -v
```

#### Using Batch Script (Windows)
```bash
# Interactive menu
run_tests.bat
```

## 📊 Reports

### HTML Reports
- Generated in `reports/` directory
- Timestamped filenames for historical tracking
- Self-contained HTML with embedded CSS/JS
- Detailed test results, logs, and screenshots

### XML Reports
- JUnit XML format for CI/CD integration
- Generated alongside HTML reports

### Example Report Files
```
reports/
├── pos_automation_report_20250803_143022.html
├── junit_report_20250803_143022.xml
├── test_01_basic_cash_sale_report_20250803_143530.html
└── ...
```

## ⚙️ Configuration

### Test Configuration (`config/config.py`)
- POS application settings
- Login credentials
- Test data (EAN codes)
- Timeout values
- Report directories

### Pytest Configuration (`pyproject.toml`)
- HTML report settings
- Test discovery patterns
- Markers definition
- Default options

## 🔧 Key Features

### Robust Error Handling
- Comprehensive timeout mechanisms
- Screen saver and overlay detection
- Fallback strategies for UI interactions

### Detailed Logging
- Emoji-enhanced console output
- Step-by-step execution tracking
- Performance timing information

### Modular Architecture
- Reusable POS automation base class
- Configurable test parameters
- Separated concerns (config, utils, tests)

### Advanced Reporting
- Rich HTML reports with test details
- Promotion analysis and calculations
- Loyalty integration tracking
- Execution timing and performance metrics

## 🎯 Test Markers

- `smoke`: Quick validation tests
- `regression`: Comprehensive feature tests
- `cash_flow`: Cash payment scenarios
- `promotion`: Promotion and discount testing
- `loyalty`: Loyalty program integration

## 📁 Original Scripts Integration

The new pytest framework is built on top of your original automation scripts:

- **`01_additem_completewithCash.py`** → `test_01_basic_cash_sale.py`
- **`02_addtems_promotion_cashSale.py`** → `test_02_promotion_cash_sale.py`
- **`03_additem_Withloyalty_cashSal.py`** → `test_03_loyalty_cash_sale.py`

All original functionality is preserved but enhanced with:
- Professional test structure
- Better error handling
- Detailed reporting
- Modular design

## 🛠️ Troubleshooting

### Common Issues
1. **POS Not Found**: Ensure R10PosClient is running
2. **Login Failed**: Check credentials in config.py
3. **Element Not Found**: Verify UI element IDs and timeouts
4. **Permission Error**: Run with appropriate Windows permissions

### Debug Mode
```bash
python -m pytest tests/pos_automation/ -v -s --tb=long
```

## 📝 Contributing

1. Follow the existing code structure
2. Add appropriate pytest markers
3. Include detailed docstrings
4. Update configuration as needed
5. Test thoroughly before committing

## 📄 License

Internal automation testing framework for POS system validation.
