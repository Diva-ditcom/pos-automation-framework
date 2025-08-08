"""
POS Automation Configuration
Data-driven configuration using CSV files for flexibility and scalability
"""
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import CSV data manager
from data.csv_data_manager import csv_data_manager  # type: ignore


class Config:
    """Data-driven configuration class that loads settings from CSV files."""
    
    def __init__(self):
        """Initialize configuration by loading data from CSV files"""
        self.data_manager = csv_data_manager
        self.settings = self.data_manager.load_settings()
        print("✅ Configuration initialized with CSV data")
    
    # POS Application Settings (loaded from CSV)
    @property
    def POS_LAUNCH_PATH(self):
        return self.data_manager.get_setting('POS_LAUNCH_PATH', 'C:\\pos\\bin\\launch.bat')
    
    @property
    def POS_STARTUP_WAIT(self):
        return self.data_manager.get_setting('POS_STARTUP_WAIT', 10)
    
    @property
    def POS_APP_TITLE(self):
        return self.data_manager.get_setting('POS_APP_TITLE', 'POS Application')
    
    @property
    def DEFAULT_TIMEOUT(self):
        return self.data_manager.get_setting('DEFAULT_TIMEOUT', 30)
    
    @property
    def SCREENSHOT_ON_FAILURE(self):
        return self.data_manager.get_setting('SCREENSHOT_ON_FAILURE', True)
    
    @property
    def REPORT_TITLE(self):
        return self.data_manager.get_setting('REPORT_TITLE', 'POS Automation Test Report')
    
    @property
    def POS_TITLE_REGEX(self):
        return self.data_manager.get_setting('POS_TITLE_REGEX', '.*POS.*')
    
    # Dynamic data methods for scenarios
    def get_scenario_data(self, scenario_name: str):
        """Get all data for a specific test scenario"""
        return self.data_manager.get_scenario_data(scenario_name)
    
    def get_user_credentials(self, scenario_name: str):
        """Get user credentials for a scenario"""
        scenario = self.get_scenario_data(scenario_name)
        if scenario:
            return {
                'username': scenario.get('user_name'),
                'password': scenario.get('password')
            }
        return {'username': None, 'password': None}
    
    def get_item_data(self, scenario_name: str):
        """Get item data for a scenario"""
        scenario = self.get_scenario_data(scenario_name)
        if scenario:
            return {
                'ean_code': scenario.get('ean_code'),
                'item_name': scenario.get('item_name'),
                'expected_price': scenario.get('expected_price'),
                'quantity': scenario.get('quantity', 1)
            }
        return {}
    
    def get_payment_data(self, scenario_name: str):
        """Get payment data for a scenario"""
        scenario = self.get_scenario_data(scenario_name)
        if scenario:
            return {
                'cash_tender_amount': scenario.get('cash_tender_amount'),
                'loyalty_number': scenario.get('loyalty_number'),
                'promotion_code': scenario.get('promotion_code')
            }
        return {}
    
    def list_available_scenarios(self):
        """Get list of all available scenarios"""
        return self.data_manager.list_available_scenarios()
    
    def validate_scenario(self, scenario_name: str):
        """Validate that a scenario has all required data"""
        return self.data_manager.validate_scenario_data(scenario_name)
