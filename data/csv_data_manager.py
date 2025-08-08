"""
CSV Data Manager for POS Automation
Handles loading test data and configuration from CSV files
"""
import csv
import os
import sys
from typing import Dict, List, Any, Optional

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class CSVDataManager:
    """Manages test data and configuration from CSV files"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '.')
        self.scenarios_file = os.path.join(self.data_dir, 'test_scenarios.csv')
        self.settings_file = os.path.join(self.data_dir, 'app_settings.csv')
        
        # Cache for loaded data
        self._scenarios_cache = None
        self._settings_cache = None
    
    def load_scenarios(self) -> List[Dict[str, Any]]:
        """Load all test scenarios from CSV file"""
        if self._scenarios_cache is None:
            self._scenarios_cache = []
            try:
                with open(self.scenarios_file, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Convert numeric fields
                        if row['expected_price']:
                            row['expected_price'] = float(row['expected_price'])
                        if row['cash_tender_amount']:
                            row['cash_tender_amount'] = float(row['cash_tender_amount'])
                        if row['quantity']:
                            row['quantity'] = int(row['quantity'])
                        
                        self._scenarios_cache.append(row)
                print(f"Loaded {len(self._scenarios_cache)} scenarios from CSV")
            except FileNotFoundError:
                print(f"Scenarios file not found: {self.scenarios_file}")
                return []
            except Exception as e:
                print(f"Error loading scenarios: {str(e)}")
                return []
        
        return self._scenarios_cache
    
    def load_settings(self) -> Dict[str, Any]:
        """Load application settings from CSV file"""
        if self._settings_cache is None:
            self._settings_cache = {}
            try:
                with open(self.settings_file, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        setting_name = row['setting_name']
                        setting_value = row['setting_value']
                        
                        # Convert boolean and numeric values
                        if setting_value.lower() in ['true', 'false']:
                            setting_value = setting_value.lower() == 'true'
                        elif setting_value.isdigit():
                            setting_value = int(setting_value)
                        elif '.' in setting_value and setting_value.replace('.', '').isdigit():
                            setting_value = float(setting_value)
                        
                        self._settings_cache[setting_name] = setting_value
                
                print(f"[SUCCESS] Loaded {len(self._settings_cache)} settings from CSV")
            except FileNotFoundError:
                print(f"[ERROR] Settings file not found: {self.settings_file}")
                return {}
            except Exception as e:
                print(f"[ERROR] Error loading settings: {str(e)}")
                return {}
        
        return self._settings_cache
    
    def get_scenario_data(self, scenario_name: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific scenario"""
        scenarios = self.load_scenarios()
        for scenario in scenarios:
            if scenario['scenario_name'] == scenario_name:
                print(f"[SUCCESS] Found data for scenario: {scenario_name}")
                return scenario
        
        print(f"[ERROR] No data found for scenario: {scenario_name}")
        return None
    
    def get_setting(self, setting_name: str, default_value: Any = None) -> Any:
        """Get a specific setting value"""
        settings = self.load_settings()
        return settings.get(setting_name, default_value)
    
    def add_scenario(self, scenario_data: Dict[str, Any]) -> bool:
        """Add a new scenario to the CSV file"""
        try:
            # Check if scenario already exists
            existing_scenarios = self.load_scenarios()
            for scenario in existing_scenarios:
                if scenario['scenario_name'] == scenario_data['scenario_name']:
                    print(f"[ERROR] Scenario '{scenario_data['scenario_name']}' already exists")
                    return False
            
            # Append to CSV file
            with open(self.scenarios_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['scenario_name', 'user_name', 'password', 'ean_code', 
                             'item_name', 'expected_price', 'cash_tender_amount', 
                             'loyalty_number', 'promotion_code', 'quantity']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(scenario_data)
            
            # Clear cache to reload data
            self._scenarios_cache = None
            print(f"[SUCCESS] Added new scenario: {scenario_data['scenario_name']}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error adding scenario: {str(e)}")
            return False
    
    def list_available_scenarios(self) -> List[str]:
        """Get list of all available scenario names"""
        scenarios = self.load_scenarios()
        return [scenario['scenario_name'] for scenario in scenarios]
    
    def validate_scenario_data(self, scenario_name: str) -> bool:
        """Validate that a scenario has all required data"""
        scenario = self.get_scenario_data(scenario_name)
        if not scenario:
            return False
        
        required_fields = ['user_name', 'ean_code', 'cash_tender_amount']
        missing_fields = []
        
        for field in required_fields:
            if not scenario.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"[ERROR] Scenario '{scenario_name}' missing required fields: {missing_fields}")
            return False
        
        print(f"[SUCCESS] Scenario '{scenario_name}' data validation passed")
        return True


# Global instance for easy access
csv_data_manager = CSVDataManager()
