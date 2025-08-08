"""
CSV Data Management Utility
Easy script to manage test data in CSV files
"""
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.csv_data_manager import csv_data_manager  # type: ignore


def display_menu():
    """Display the main menu options"""
    print("\n" + "="*60)
    print("🗂️  CSV Data Management Utility")
    print("="*60)
    print("1. 📋 List all available scenarios")
    print("2. 👀 View scenario data")
    print("3. ➕ Add new scenario")
    print("4. ⚙️  View application settings")
    print("5. ✅ Validate scenario data")
    print("6. 🧪 Test data loading")
    print("0. 🚪 Exit")
    print("="*60)


def list_scenarios():
    """List all available scenarios"""
    scenarios = csv_data_manager.list_available_scenarios()
    print(f"\n📋 Available Scenarios ({len(scenarios)}):")
    for i, scenario in enumerate(scenarios, 1):
        print(f"   {i}. {scenario}")


def view_scenario_data():
    """View data for a specific scenario"""
    scenarios = csv_data_manager.list_available_scenarios()
    
    if not scenarios:
        print("❌ No scenarios available")
        return
    
    print("\nSelect scenario to view:")
    list_scenarios()
    
    try:
        choice = int(input("\nEnter scenario number: ")) - 1
        if 0 <= choice < len(scenarios):
            scenario_name = scenarios[choice]
            data = csv_data_manager.get_scenario_data(scenario_name)
            
            if data:
                print(f"\n📄 Data for scenario '{scenario_name}':")
                print("-" * 40)
                for key, value in data.items():
                    print(f"   {key}: {value}")
            else:
                print(f"❌ No data found for scenario: {scenario_name}")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")


def add_new_scenario():
    """Add a new scenario interactively"""
    print("\n➕ Adding New Scenario")
    print("-" * 30)
    
    scenario_data = {}
    
    # Get required fields
    scenario_data['scenario_name'] = input("Scenario name: ").strip()
    scenario_data['user_name'] = input("Username: ").strip()
    scenario_data['password'] = input("Password: ").strip()
    scenario_data['ean_code'] = input("EAN code: ").strip()
    scenario_data['item_name'] = input("Item name: ").strip()
    
    # Get optional numeric fields
    try:
        price = input("Expected price (press Enter to skip): ").strip()
        scenario_data['expected_price'] = float(price) if price else ""
        
        cash = input("Cash tender amount: ").strip()
        scenario_data['cash_tender_amount'] = float(cash) if cash else ""
        
        qty = input("Quantity (default 1): ").strip()
        scenario_data['quantity'] = int(qty) if qty else 1
    except ValueError:
        print("❌ Invalid numeric input. Setting default values.")
        scenario_data['expected_price'] = ""
        scenario_data['cash_tender_amount'] = ""
        scenario_data['quantity'] = 1
    
    # Get optional fields
    scenario_data['loyalty_number'] = input("Loyalty number (optional): ").strip()
    scenario_data['promotion_code'] = input("Promotion code (optional): ").strip()
    
    # Add scenario
    success = csv_data_manager.add_scenario(scenario_data)
    if success:
        print(f"✅ Scenario '{scenario_data['scenario_name']}' added successfully!")
    else:
        print(f"❌ Failed to add scenario")


def view_settings():
    """View application settings"""
    settings = csv_data_manager.load_settings()
    print(f"\n⚙️ Application Settings ({len(settings)}):")
    print("-" * 40)
    for key, value in settings.items():
        print(f"   {key}: {value}")


def validate_scenario():
    """Validate scenario data"""
    scenarios = csv_data_manager.list_available_scenarios()
    
    if not scenarios:
        print("❌ No scenarios available")
        return
    
    print("\nSelect scenario to validate:")
    list_scenarios()
    
    try:
        choice = int(input("\nEnter scenario number: ")) - 1
        if 0 <= choice < len(scenarios):
            scenario_name = scenarios[choice]
            is_valid = csv_data_manager.validate_scenario_data(scenario_name)
            
            if is_valid:
                print(f"✅ Scenario '{scenario_name}' validation passed")
            else:
                print(f"❌ Scenario '{scenario_name}' validation failed")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")


def test_data_loading():
    """Test data loading functionality"""
    print("\n🧪 Testing Data Loading...")
    print("-" * 30)
    
    # Test scenarios loading
    scenarios = csv_data_manager.load_scenarios()
    print(f"✅ Loaded {len(scenarios)} scenarios")
    
    # Test settings loading
    settings = csv_data_manager.load_settings()
    print(f"✅ Loaded {len(settings)} settings")
    
    # Test individual scenario loading
    if scenarios:
        first_scenario = scenarios[0]['scenario_name']
        data = csv_data_manager.get_scenario_data(first_scenario)
        if data:
            print(f"✅ Successfully loaded data for '{first_scenario}'")
        else:
            print(f"❌ Failed to load data for '{first_scenario}'")


def main():
    """Main function to run the utility"""
    while True:
        display_menu()
        
        try:
            choice = input("\nSelect option (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye!")
                break
            elif choice == "1":
                list_scenarios()
            elif choice == "2":
                view_scenario_data()
            elif choice == "3":
                add_new_scenario()
            elif choice == "4":
                view_settings()
            elif choice == "5":
                validate_scenario()
            elif choice == "6":
                test_data_loading()
            else:
                print("❌ Invalid choice. Please select 0-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
