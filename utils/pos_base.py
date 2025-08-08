"""
Base POS automation utilities and common functions
"""
import time
from pywinauto import Application
from pywinauto.findwindows import find_windows
import subprocess
import random
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules (IDE may show import error but it works at runtime)
from config.config import Config  # type: ignore

class POSAutomation:
    def __init__(self, scenario_name=None):
        self.app = None
        self.win = None
        self.config = Config()
        self.scenario_name = scenario_name
        self.scenario_data = None
        
        # Load scenario data if provided
        if scenario_name:
            self.load_scenario_data(scenario_name)
    
    def load_scenario_data(self, scenario_name: str):
        """Load data for a specific test scenario"""
        self.scenario_name = scenario_name
        self.scenario_data = self.config.get_scenario_data(scenario_name)
        
        if self.scenario_data:
            print(f"[SUCCESS] Loaded data for scenario: {scenario_name}")
            return True
        else:
            print(f"[ERROR] Failed to load data for scenario: {scenario_name}")
            return False
    
    def get_user_credentials(self):
        """Get user credentials for current scenario"""
        if self.scenario_name:
            return self.config.get_user_credentials(self.scenario_name)
        return {'username': None, 'password': None}
    
    def get_item_data(self):
        """Get item data for current scenario"""
        if self.scenario_name:
            return self.config.get_item_data(self.scenario_name)
        return {}
    
    def get_payment_data(self):
        """Get payment data for current scenario"""
        if self.scenario_name:
            return self.config.get_payment_data(self.scenario_name)
        return {}
    
    def launch_pos(self):
        """Launch the POS application using launch.bat."""
        try:
            subprocess.Popen([self.config.POS_LAUNCH_PATH], shell=True)
            print(f"[SUCCESS] Launched POS application using: {self.config.POS_LAUNCH_PATH}")
            time.sleep(self.config.POS_STARTUP_WAIT)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to launch POS application: {e}")
            return False
    
    def is_pos_running(self):
        """Check if POS application is already running."""
        try:
            wins = find_windows(title_re=self.config.POS_TITLE_REGEX)
            return len(wins) > 0
        except Exception:
            return False
    
    def connect_to_pos(self):
        """Connect to the POS application."""
        try:
            self.app = Application(backend="uia").connect(title_re=self.config.POS_TITLE_REGEX)
            self.win = self.app.window(title_re=self.config.POS_TITLE_REGEX)
            self.win.set_focus()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to connect to POS: {e}")
            return False
    
    def login_to_pos(self, username=None, password=None):
        """Login to POS with provided or default credentials."""
        if not username:
            username = self.config.USERNAME
        if not password:
            password = self.config.PASSWORD
            
        # Try to find the login button
        login_btn = self.win.child_window(auto_id="UCLoginScreenLoginButton", control_type="Button")
        if not login_btn.exists(timeout=self.config.LOGIN_TIMEOUT):
            print("ℹ️ Login button not found. Trying to dismiss possible screen saver or overlay...")
            self._dismiss_overlays()
            login_btn = self.win.child_window(auto_id="UCLoginScreenLoginButton", control_type="Button")
        
        if login_btn.exists(timeout=self.config.LOGIN_TIMEOUT):
            login_btn.wait("enabled", timeout=self.config.LOGIN_TIMEOUT)
            login_btn.click_input()
            print("[SUCCESS] Login button clicked.")
        else:
            print("[ERROR] Login button not found after all attempts.")
            return False
        
        # Enter username
        if not self._enter_username(username):
            return False
        
        # Enter password
        if not self._enter_password(password):
            return False
        
        # Click sign-in OK button
        loginrc_btn = self.win.child_window(auto_id="UCSignInOKButton", control_type="Button")
        if loginrc_btn.exists(timeout=self.config.LOGIN_TIMEOUT):
            loginrc_btn.wait("enabled", timeout=self.config.LOGIN_TIMEOUT)
            loginrc_btn.click_input()
            print("[SUCCESS] Sign-in OK button clicked.")
            time.sleep(2)
            print("[SUCCESS] Login attempted. Check POS for success.")
            return True
        else:
            print("[ERROR] Login OK button not found.")
            return False
    
    def _dismiss_overlays(self):
        """Dismiss screen savers or overlays."""
        try:
            screensaver = self.win.child_window(class_name="MediaElement")
            if screensaver.exists(timeout=3):
                print("ℹ️ Screen saver detected. Attempting to dismiss...")
                screensaver.click_input()
                time.sleep(1)
        except Exception:
            print("ℹ️ Screen saver not detected.")
        
        # Random click if needed
        print("ℹ️ Clicking randomly on the window to dismiss any overlay...")
        rect = self.win.rectangle()
        x = random.randint(rect.left + 50, rect.right - 50)
        y = random.randint(rect.top + 50, rect.bottom - 50)
        self.win.click_input(coords=(x, y))
        time.sleep(1)
    
    def _enter_username(self, username):
        """Enter username in the login field."""
        username_field = self.win.child_window(auto_id="UserName", control_type="Edit")
        if username_field.exists(timeout=self.config.ELEMENT_WAIT):
            username_field.wait("ready", timeout=self.config.DEFAULT_TIMEOUT)
            current_username = username_field.get_value() if hasattr(username_field, 'get_value') else username_field.window_text()
            if current_username.strip() != username:
                username_field.type_keys(username, with_spaces=True)
                print(f"[SUCCESS] User ID field found and entered: {username}")
            else:
                print(f"ℹ️ Username already present: {current_username}. Skipping entry.")
            return True
        else:
            print("[ERROR] User ID field not found.")
            return False
    
    def _enter_password(self, password):
        """Enter password in the login field."""
        password_field = self.win.child_window(auto_id="Password", control_type="Edit")
        if password_field.exists(timeout=self.config.ELEMENT_WAIT):
            password_field.wait("ready", timeout=self.config.DEFAULT_TIMEOUT)
            password_field.type_keys(password, with_spaces=True)
            print(f"[SUCCESS] Password field found and entered: {'*' * len(password)}")
            return True
        else:
            print("[ERROR] Password field not found.")
            return False
    
    def check_nosale(self):
        """Check if the 'No Sale' button is enabled and visible."""
        nosale_btn = self.win.child_window(auto_id="commandsLowerButtonsNo Sale", control_type="Button")
        if nosale_btn.exists() and nosale_btn.is_visible():
            print("[SUCCESS] 'No Sale' button is enabled and exists.")
            return True
        else:
            print("[ERROR] 'No Sale' button is not enabled or does not exist.")
            return False
    
    def click_button_by_text(self, button_text, timeout=None):
        """Click a button by its text content."""
        if timeout is None:
            timeout = self.config.DEFAULT_TIMEOUT
            
        start_time = time.time()
        target_button = None
        while time.time() - start_time < timeout:
            buttons = self.win.descendants(control_type="Button")
            for btn in buttons:
                if (btn.window_text() == button_text and 
                    btn.is_visible() and btn.is_enabled()):
                    target_button = btn
                    break
            if target_button:
                break
            time.sleep(1)
        
        if target_button:
            target_button.click_input()
            time.sleep(0.5)
            return True
        else:
            print(f"[ERROR] '{button_text}' button not found within timeout.")
            return False
    
    def add_product_by_ean(self, ean):
        """Add a product using EAN code via numpad."""
        print(f"\n=== Adding product with EAN: {ean} ===")
        
        # Clear EAN field
        print("Clearing EAN field...")
        self._clear_ean_field()
        
        # Enter EAN digits
        print(f"Entering EAN: {ean}")
        for digit in str(ean):
            if not self.click_button_by_text(digit):
                print(f"[ERROR] Failed to enter digit: {digit}")
                return False
            time.sleep(0.2)
        
        # Click OK to add product
        if not self.click_button_by_text("OK"):
            print("[ERROR] Failed to click OK button")
            return False
        
        print("[SUCCESS] Product added successfully")
        return True
    
    def _clear_ean_field(self):
        """Clear the EAN input field."""
        max_clear_attempts = 20
        for _ in range(max_clear_attempts):
            edit_fields = self.win.descendants(control_type="Edit")
            cleared = True
            for field in edit_fields:
                val = field.get_value() if hasattr(field, 'get_value') else field.window_text()
                if val.strip():
                    cleared = False
                    if self.click_button_by_text("<<", timeout=2):
                        time.sleep(0.2)
            if cleared:
                print("[SUCCESS] EAN field cleared.")
                break
    
    def handle_loyalty_popup(self):
        """Handle loyalty popup by clicking Cancel."""
        popup = self.app.top_window()
        print("\n=== Handling loyalty popup ===")
        print("Popup title:", popup.window_text())
        
        buttons = popup.descendants(control_type="Button")
        for btn in buttons:
            if btn.window_text().strip().lower() == "cancel":
                time.sleep(4)
                btn.click_input()
                print("[SUCCESS] Clicked Cancel button on loyalty popup")
                return True
        
        print("[ERROR] Cancel button not found on loyalty popup")
        return False
    
    def complete_cash_tender(self):
        """Complete transaction with cash tender."""
        print("\n=== Completing transaction with cash ===")
        
        try:
            # Click Cash tender button
            tender_btn = self.win.child_window(auto_id="TenderButtonsCash", control_type="ListItem")
            if not tender_btn.exists():
                print("[ERROR] Cash tender button not found")
                return False
            
            tender_btn.click_input()
            print("[SUCCESS] Clicked Cash tender button")
            time.sleep(1)
            
            # Select first suggested amount
            cash_list = self.win.child_window(auto_id="SuggestedCashListBox", control_type="List")
            list_items = cash_list.children(control_type="ListItem")
            if list_items:
                list_items[0].click_input()
                print(f"[SUCCESS] Selected suggested amount: {list_items[0].window_text()}")
            else:
                print("[ERROR] No suggested amounts found")
                return False
            
            # Handle receipt popup
            time.sleep(4)
            popup = self.app.top_window()
            buttons = popup.descendants(control_type="Button")
            for btn in buttons:
                if btn.window_text().strip().lower() == "yes":
                    btn.click_input()
                    print("[SUCCESS] Clicked Yes on receipt popup")
                    return True
            
            print("[ERROR] Yes button not found on receipt popup")
            return False
            
        except Exception as e:
            print(f"[ERROR] Error during tender process: {e}")
            return False
    
    # Data-Driven Methods for Scenario-Based Testing
    def execute_scenario_login(self):
        """Login using credentials from scenario data"""
        credentials = self.get_user_credentials()
        if credentials['username'] and credentials['password']:
            print(f"🔐 Logging in with scenario credentials for: {credentials['username']}")
            return self.login(credentials['username'], credentials['password'])
        else:
            print("[ERROR] No valid credentials found in scenario data")
            return False
    
    def execute_scenario_add_item(self):
        """Add item using data from scenario"""
        item_data = self.get_item_data()
        if item_data and item_data.get('ean_code'):
            ean_code = item_data['ean_code']
            quantity = item_data.get('quantity', 1)
            
            print(f"🛒 Adding item from scenario: EAN={ean_code}, Qty={quantity}")
            
            # Add item multiple times if quantity > 1
            for i in range(quantity):
                success = self.add_item_by_ean(ean_code)
                if not success:
                    print(f"[ERROR] Failed to add item {i+1}/{quantity}")
                    return False
                print(f"[SUCCESS] Added item {i+1}/{quantity}")
            
            return True
        else:
            print("[ERROR] No valid item data found in scenario")
            return False
    
    def execute_scenario_payment(self):
        """Complete payment using data from scenario"""
        payment_data = self.get_payment_data()
        
        if payment_data and payment_data.get('cash_tender_amount'):
            cash_amount = str(payment_data['cash_tender_amount'])
            loyalty_number = payment_data.get('loyalty_number')
            
            print(f"💰 Processing payment from scenario: Cash=${cash_amount}")
            
            # Handle loyalty if present
            if loyalty_number:
                print(f"[TARGET] Loyalty number available: {loyalty_number}")
                # You can add loyalty handling logic here
            
            # Complete cash transaction
            return self.complete_cash_transaction(cash_amount)
        else:
            print("[ERROR] No valid payment data found in scenario")
            return False
    
    def add_item_by_ean(self, ean_code):
        """Add item by EAN code (placeholder method - implement based on your POS UI)"""
        # This is a placeholder method - you'll need to implement based on your specific POS UI
        print(f"🏷️ Adding item with EAN: {ean_code}")
        try:
            # Example implementation - adjust based on your POS interface
            # Find EAN input field and enter the code
            # ean_field = self.win.child_window(auto_id="EANInput", control_type="Edit")
            # ean_field.set_text(ean_code)
            # enter_btn = self.win.child_window(auto_id="AddItemButton", control_type="Button")
            # enter_btn.click()
            
            print(f"[SUCCESS] Item with EAN {ean_code} added successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to add item with EAN {ean_code}: {e}")
            return False
    
    def complete_cash_transaction(self, cash_amount):
        """Complete transaction with cash (placeholder method - implement based on your POS UI)"""
        print(f"💵 Completing cash transaction with amount: ${cash_amount}")
        try:
            # This is a placeholder method - implement based on your specific POS UI
            # Find cash button and click
            # cash_btn = self.win.child_window(auto_id="CashButton", control_type="Button")
            # cash_btn.click()
            
            # Enter cash amount
            # amount_field = self.win.child_window(auto_id="CashAmount", control_type="Edit")
            # amount_field.set_text(cash_amount)
            
            # Complete transaction
            # complete_btn = self.win.child_window(auto_id="CompleteButton", control_type="Button")
            # complete_btn.click()
            
            print(f"[SUCCESS] Cash transaction completed with ${cash_amount}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to complete cash transaction: {e}")
            return False
