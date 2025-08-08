import time
from pywinauto import Application
from pywinauto.findwindows import find_windows
import subprocess

def launch_pos():
    """
    Launch the POS application using launch.bat.
    """
    bat_path = r"c:\WIN_POC\pywinauto\Scripts\WOWPospplication\AI\launch.bat"
    try:
        subprocess.Popen([bat_path], shell=True)
        print(f"[SUCCESS] Launched POS application using: {bat_path}")
        time.sleep(20)  # Wait for the application to start
        return True
    except Exception as e:
        print(f"[ERROR] Failed to launch POS application: {e}")
        return False

def login_to_pos(username, password):
    app = Application(backend="uia").connect(title_re=".*R10PosClient.*")
    win = app.window(title_re=".*R10PosClient.*")
    win.set_focus()
    # Try to find the login button
    login_btn = win.child_window(auto_id="UCLoginScreenLoginButton", control_type="Button")
    if not login_btn.exists(timeout=5):
        print("ℹ️ Login button not found. Trying to dismiss possible screen saver or overlay...")
        # Try to find a screen saver overlay
        try:
            screensaver = win.child_window(class_name="MediaElement")
            if screensaver.exists(timeout=3):
                print("ℹ️ Screen saver detected. Attempting to dismiss...")
                screensaver.click_input()
                time.sleep(1)
                login_btn = win.child_window(auto_id="UCLoginScreenLoginButton", control_type="Button")
        except Exception:
            print("ℹ️ Screen saver not detected.")
        # If still not found, click randomly on the window
        if not login_btn.exists(timeout=3):
            print("ℹ️ Clicking randomly on the window to dismiss any overlay...")
            rect = win.rectangle()
            import random
            x = random.randint(rect.left + 50, rect.right - 50)
            y = random.randint(rect.top + 50, rect.bottom - 50)
            win.click_input(coords=(x, y))
            time.sleep(1)
            login_btn = win.child_window(auto_id="UCLoginScreenLoginButton", control_type="Button")
    if login_btn.exists(timeout=5):
        login_btn.wait("enabled", timeout=10)
        login_btn.click_input()
        print("[SUCCESS] Login button clicked.")
    else:
        print("[ERROR] Login button not found after all attempts. Cannot proceed with login.")
        return False
    # Enter username only if not already present
    username_field = win.child_window(auto_id="UserName", control_type="Edit")
    if username_field.exists(timeout=5):
        username_field.wait("ready", timeout=10)
        current_username = username_field.get_value() if hasattr(username_field, 'get_value') else username_field.window_text()
        if current_username.strip() != username:
            username_field.type_keys(username, with_spaces=True)
            print(f"[SUCCESS] User ID field found and entered: {username}")
        else:
            print(f"ℹ️ Username already present: {current_username}. Skipping entry.")
    else:
        print("[ERROR] User ID field not found.")
        return False
    # Enter password
    password_field = win.child_window(auto_id="Password", control_type="Edit")
    if password_field.exists(timeout=5):
        password_field.wait("ready", timeout=10)
        password_field.type_keys(password, with_spaces=True)
        print(f"[SUCCESS] Password field found and entered: {'*' * len(password)}")
    else:
        print("[ERROR] Password field not found.")
        return False
    # Click the sign-in OK button
    loginrc_btn = win.child_window(auto_id="UCSignInOKButton", control_type="Button")
    if loginrc_btn.exists(timeout=5):
        loginrc_btn.wait("enabled", timeout=5)
        loginrc_btn.click_input()
        print("[SUCCESS] Sign-in OK button clicked.")
        time.sleep(2)
        print("[SUCCESS] Login attempted. Check POS for success.")
        return True
    else:
        print("[ERROR] Login OK button not found.")
        return False

def check_nosale(win):
    """
    Check if the 'No Sale' button is enabled and visible.
    """
    nosale_btn = win.child_window(auto_id="commandsLowerButtonsNo Sale", control_type="Button")
    if nosale_btn.exists() and nosale_btn.is_visible():
        print("[SUCCESS] 'No Sale' button is enabled and exists.")
        return True
    else:
        print("[ERROR] 'No Sale' button is not enabled or does not exist.")
        return False

def click_button_by_text(win, button_text, timeout=10):
    start_time = time.time()
    target_button = None
    while time.time() - start_time < timeout:
        buttons = win.descendants(control_type="Button")
        for btn in buttons:
            if (
                btn.window_text() == button_text
                and btn.is_visible()
                and btn.is_enabled()
            ):
                target_button = btn
                break
        if target_button:
            break
        time.sleep(1)
    if target_button:
        print(f"Found button: {target_button.window_text()}")
        target_button.click_input()
        time.sleep(0.5)
        return True
    else:
        print(f"[ERROR] '{button_text}' button not found within timeout.")
        return False


def add_product_and_check_basket(win, ean):
    """
    Add a product using numpad and check basket
    """
    # Clear EAN field
    print("\n=== Adding product ===")
    print("Clearing EAN field...")
    max_clear_attempts = 20
    for _ in range(max_clear_attempts):
        edit_fields = win.descendants(control_type="Edit")
        cleared = True
        for field in edit_fields:
            val = field.get_value() if hasattr(field, 'get_value') else field.window_text()
            if val.strip():
                cleared = False
                if click_button_by_text(win, "<<", timeout=2):
                    time.sleep(0.2)
        if cleared:
            print("[SUCCESS] EAN field cleared.")
            break

    # Enter EAN digits
    print(f"Entering EAN: {ean}")
    for digit in str(ean):
        if not click_button_by_text(win, digit):
            print(f"[ERROR] Failed to enter digit: {digit}")
            return False
        time.sleep(0.2)

    # Click OK to add product
    if not click_button_by_text(win, "OK"):
        print("[ERROR] Failed to click OK button")
        return False
    print("[SUCCESS] Product added successfully")

    # Check basket contents
    print("\n=== Checking basket ===")
    time.sleep(1)
    basket_controls = win.descendants(control_type="List")
    if not basket_controls:
        basket_controls = win.descendants(control_type="ListBox")
    if not basket_controls:
        basket_controls = win.descendants(control_type="ListView")

    if basket_controls:
        basket = basket_controls[0]
        items = basket.descendants(control_type="ListItem")
        if not items:
            items = basket.children()
       
        print(f"Found {len(items)} item(s) in basket:")
        promotion_found = False
        for item in items:
            txt = item.window_text()
            print(f"- {txt}")
            if "promotion" in txt.lower() or "bonus" in txt.lower():
                promotion_found = True
                print(f"[SUCCESS] Promotion found: {txt}")
       
        print("[SUCCESS] Basket check completed.")
        time.sleep(2)
        click_button_by_text(win, "OK")
        return True
    else:
        print("[ERROR] Could not find basket")
        return False

def handle_loyalty_popup(app):
    """
    Handle loyalty popup and enter customer card
    """
    popup = app.top_window()
    print("\n=== Handling loyalty popup ===")
    print("Popup title:", popup.window_text())

    # Enter customer card
    card_number = "9344402191258"
    edit_fields = popup.descendants(control_type="Edit")
    entered = False
    for field in edit_fields:
        try:
            field.set_focus()
            field.type_keys(card_number, with_spaces=True)
            time.sleep(2)
            print(f"[SUCCESS] Entered customer card: {card_number}")
            entered = True
            break
        except Exception:
            continue

    if not entered:
        print("[ERROR] Could not enter customer card")
        return False

    # Click OK button
    buttons = popup.descendants(control_type="Button")
    for btn in buttons:
        if btn.window_text().strip().lower() == "ok":
            time.sleep(2)  # Wait for any animations
            btn.click_input()
            print("[SUCCESS] Clicked OK button on loyalty popup")
            return True
   
    print("[ERROR] OK button not found on loyalty popup")
    return False

def complete_cash_tender(app):
    """
    Complete transaction with cash tender
    """
    win = app.window(title_re=".*R10PosClient.*")
    win.set_focus()
    print("\n=== Completing transaction with cash ===")
   
    try:
        # Click Cash tender button
        tender_btn = win.child_window(auto_id="TenderButtonsCash", control_type="ListItem")
        if not tender_btn.exists():
            print("[ERROR] Cash tender button not found")
            return False
       
        tender_btn.click_input()
        print("[SUCCESS] Clicked Cash tender button")
        time.sleep(1)

        # Select first suggested amount
        cash_list = win.child_window(auto_id="SuggestedCashListBox", control_type="List")
        list_items = cash_list.children(control_type="ListItem")
        if list_items:
            list_items[0].click_input()
            print(f"[SUCCESS] Selected suggested amount: {list_items[0].window_text()}")
        else:
            print("[ERROR] No suggested amounts found")
            return False

        # Handle receipt popup
        time.sleep(4)
        popup = app.top_window()
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

def main():
    print("=== Starting Happy Flow ===")
   
    # Step 1: Check if POS is running, if not launch it

    pos_title_re = ".*R10PosClient.*"
    def is_pos_running():
        try:
            wins = find_windows(title_re=pos_title_re)
            return len(wins) > 0
        except Exception:
            return False
    # Main flow logic
    if is_pos_running():
        print("ℹ️ POS is already running. Checking for No Sale button...")
        app = Application(backend="uia").connect(title_re=pos_title_re)
        win = app.window(title_re=pos_title_re)
        win.set_focus()
        if check_nosale(win):
            print("[SUCCESS] POS is ready. No Sale button is present.")
        else:
            print("[ERROR] No Sale button not found. Attempting login...")
            if login_to_pos("atmgr5", "abcd1234"):
                print("[SUCCESS] Logged in successfully. Checking No Sale button...")
                if check_nosale(win):
                    print("[SUCCESS] No Sale button found after login.")
                else:
                    print("[ERROR] No Sale button still not found after login.")
            else:
                print("[ERROR] Login failed. Cannot check No Sale button.")
    else:
        print("ℹ️ POS is not running. Launching POS...")
        launch_pos()
        time.sleep(10)  # Wait longer for POS to launch
        if login_to_pos("atmgr5", "abcd1234"):
            print("[SUCCESS] Logged in successfully. Checking No Sale button...")
            app = Application(backend="uia").connect(title_re=pos_title_re)
            win = app.window(title_re=pos_title_re)
            win.set_focus()
            if check_nosale(win):
                print("[SUCCESS] No Sale button found after login.")
               
            else:
                print("[ERROR] No Sale button not found after login.")
        else:
            print("[ERROR] Login failed. Cannot check No Sale button.")
    # Step 2: Login to POS
 
    time.sleep(2)

    # Step 3: Add product and check basket
    if not add_product_and_check_basket(win, "9300675084147"):
        print("[ERROR] Failed to add product or check basket")
        return

    time.sleep(4)

    # Step 4: Handle loyalty popup
    if not handle_loyalty_popup(app):
        print("[ERROR] Failed to handle loyalty popup")
        return

    time.sleep(4)

    # Step 5: Complete transaction with cash tender
    if not complete_cash_tender(app):
        print("[ERROR] Failed to complete transaction")
        return

    print("\n[SUCCESS] Happy flow completed successfully!")
    time.sleep(2)
    # Click randomly on the POS window at the end
    import random
    rect = win.rectangle()
    x = random.randint(rect.left + 50, rect.right - 50)
    y = random.randint(rect.top + 50, rect.bottom - 50)
    win.click_input(coords=(x, y))
    print(f"Clicked randomly at ({x}, {y}) on the POS window.")

if __name__ == "__main__":
    main()


