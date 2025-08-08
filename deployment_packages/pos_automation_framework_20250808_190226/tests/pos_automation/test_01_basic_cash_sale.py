"""
Test Case 1: Basic Item Addition and Cash Sale
This test covers the basic flow of adding a single item and completing with cash payment.
"""
import pytest
import time
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import modules (IDE may show import error but it works at runtime)
from config.config import Config  # type: ignore

@pytest.mark.smoke
@pytest.mark.cash_flow
class TestBasicCashSale:
    
    def test_add_single_item_complete_with_cash(self, pos_transaction, capture_test_info):
        """
        Test Case: Add single item and complete transaction with cash
        
        Steps:
        1. Add product using EAN: 9300675084147
        2. Verify product in basket
        3. Handle loyalty popup (cancel)
        4. Complete transaction with cash tender
        5. Handle receipt confirmation
        
        Expected Result: Transaction completed successfully
        """
        pos = pos_transaction
        config = Config()
        
        print("\n" + "="*60)
        print("🧪 TEST: Basic Item Addition and Cash Sale")
        print("="*60)
        
        # Step 1: Add product to basket
        print("\n📦 Step 1: Adding product to basket...")
        ean = config.TEST_PRODUCTS["basic_item"]
        assert pos.add_product_by_ean(ean), f"Failed to add product with EAN: {ean}"
        
        # Step 2: Verify basket contents
        print("\n🛒 Step 2: Checking basket contents...")
        basket_verified = self._check_basket_contents(pos)
        assert basket_verified, "Failed to verify basket contents"
        
        # Add small delay for UI stability
        time.sleep(2)
        
        # Step 3: Handle loyalty popup
        print("\n💳 Step 3: Handling loyalty popup...")
        loyalty_handled = pos.handle_loyalty_popup()
        assert loyalty_handled, "Failed to handle loyalty popup"
        
        # Add delay before tender
        time.sleep(4)
        
        # Step 4: Complete cash tender
        print("\n💰 Step 4: Completing cash tender...")
        cash_completed = pos.complete_cash_tender()
        assert cash_completed, "Failed to complete cash tender"
        
        print("\n🎉 TEST PASSED: Basic cash sale completed successfully!")
        
        # Final cleanup click
        self._cleanup_pos_window(pos)
    
    def _check_basket_contents(self, pos):
        """Helper method to check and verify basket contents."""
        try:
            print("\n=== Checking basket ===")
            time.sleep(1)
            
            # Find basket controls
            basket_controls = pos.win.descendants(control_type="List")
            if not basket_controls:
                basket_controls = pos.win.descendants(control_type="ListBox")
            if not basket_controls:
                basket_controls = pos.win.descendants(control_type="ListView")
            
            if basket_controls:
                basket = basket_controls[0]
                items = basket.descendants(control_type="ListItem")
                if not items:
                    items = basket.children()
                
                print(f"Found {len(items)} item(s) in basket:")
                for item in items:
                    txt = item.window_text()
                    print(f"- {txt}")
                    if "promotion" in txt.lower() or "bonus" in txt.lower():
                        print(f"🎉 Promotion found: {txt}")
                
                print("✅ Basket check completed.")
                time.sleep(2)
                pos.click_button_by_text("OK")
                return True
            else:
                print("❌ Could not find basket")
                pos.click_button_by_text("OK")
                return False
                
        except Exception as e:
            print(f"❌ Error checking basket: {e}")
            return False
    
    def _cleanup_pos_window(self, pos):
        """Helper method to perform final cleanup."""
        try:
            time.sleep(2)
            import random
            rect = pos.win.rectangle()
            x = random.randint(rect.left + 50, rect.right - 50)
            y = random.randint(rect.top + 50, rect.bottom - 50)
            pos.win.click_input(coords=(x, y))
            print(f"🧹 Cleanup: Clicked at ({x}, {y}) on POS window")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
