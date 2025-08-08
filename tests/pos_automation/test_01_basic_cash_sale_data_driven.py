"""
Test Case 1: Basic Item Addition and Cash Sale (Data-Driven)
This test uses CSV data for the basic flow of adding a single item and completing with cash payment.
"""

import pytest
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import modules (IDE may show import error but it works at runtime)
from config.config import Config  # type: ignore


@pytest.mark.scenario(name='basic_cash_sale')
class TestBasicCashSaleDataDriven:
    """Test class for basic cash sale scenario using CSV data"""
    
    def test_add_single_item_complete_with_cash_data_driven(self, pos_automation_with_scenario):
        """
        Test Case: Add single item and complete transaction with cash (Data-Driven)
        
        Steps:
        1. Load data from CSV for 'basic_cash_sale' scenario
        2. Login using credentials from CSV
        3. Add product using EAN from CSV
        4. Verify product in basket
        5. Handle loyalty popup (cancel)
        6. Complete transaction with cash tender from CSV
        7. Handle receipt confirmation
        
        Expected Result: Transaction completed successfully using CSV data
        """
        pos = pos_automation_with_scenario
        
        # Verify scenario data is loaded
        assert pos.scenario_data is not None, "Scenario data not loaded"
        
        # Get data from CSV for this scenario
        user_data = pos.get_user_credentials()
        item_data = pos.get_item_data()
        payment_data = pos.get_payment_data()
        
        print(f"\n[TARGET] Executing Basic Cash Sale with CSV data:")
        print(f"   User: {user_data['username']}")
        print(f"   EAN: {item_data['ean_code']}")
        print(f"   Item: {item_data['item_name']}")
        print(f"   Cash Amount: ${payment_data['cash_tender_amount']}")
        
        # Step 1: Launch POS application
        print("\n[LAUNCH] Step 1: Launching POS application...")
        success = pos.launch_pos()
        assert success, "Failed to launch POS application"
        
        # Step 2: Connect to POS
        print("\n[CONNECT] Step 2: Connecting to POS...")
        success = pos.connect_to_pos()
        assert success, "Failed to connect to POS application"
        
        # Step 3: Login with CSV credentials
        print(f"\n🔐 Step 3: Logging in with user {user_data['username']}...")
        success = pos.execute_scenario_login()
        assert success, f"Failed to login with user {user_data['username']}"
        
        # Step 4: Add item using CSV data
        print(f"\n🛒 Step 4: Adding item {item_data['item_name']} (EAN: {item_data['ean_code']})...")
        success = pos.execute_scenario_add_item()
        assert success, f"Failed to add item {item_data['ean_code']}"
        
        # Step 5: Complete payment using CSV data
        print(f"\n💰 Step 5: Completing cash payment of ${payment_data['cash_tender_amount']}...")
        success = pos.execute_scenario_payment()
        assert success, f"Failed to complete cash payment"
        
        print("\n[SUCCESS] Basic Cash Sale test completed successfully with CSV data!")
