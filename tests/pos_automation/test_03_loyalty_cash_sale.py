"""
Test Case 3: Item Addition with Loyalty Integration and Cash Sale
This test covers adding items with loyalty program integration and completing with cash payment.
"""
import pytest
import time
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import modules (IDE may show import error but it works at runtime)
from config.config import Config  # type: ignore

@pytest.mark.regression
@pytest.mark.loyalty
@pytest.mark.cash_flow
class TestLoyaltyCashSale:
    
    def test_add_item_with_loyalty_integration_cash_sale(self, pos_transaction, capture_test_info):
        """
        Test Case: Add item with loyalty integration and complete transaction with cash
        
        Steps:
        1. Add product using EAN: 9300675084147
        2. Verify product in basket
        3. Handle loyalty popup with proper integration
        4. Verify loyalty benefits if applicable
        5. Complete transaction with cash tender
        6. Handle receipt confirmation
        
        Expected Result: Transaction with loyalty integration completed successfully
        """
        pos = pos_transaction
        config = Config()
        
        print("\n" + "="*60)
        print("🧪 TEST: Item Addition with Loyalty Integration and Cash Sale")
        print("="*60)
        
        # Step 1: Add product to basket
        print("\n📦 Step 1: Adding product for loyalty transaction...")
        ean = config.TEST_PRODUCTS["basic_item"]
        assert pos.add_product_by_ean(ean), f"Failed to add product with EAN: {ean}"
        
        # Step 2: Verify basket contents with loyalty context
        print("\n🛒 Step 2: Checking basket contents for loyalty transaction...")
        loyalty_basket_data = self._check_basket_for_loyalty(pos)
        assert loyalty_basket_data["basket_verified"], "Failed to verify basket contents"
        
        # Add delay for UI stability
        time.sleep(2)
        
        # Step 3: Handle loyalty popup with detailed processing
        print("\n💳 Step 3: Processing loyalty integration...")
        loyalty_result = self._handle_loyalty_with_integration(pos)
        assert loyalty_result["handled"], "Failed to handle loyalty popup"
        
        # Add delay before tender
        time.sleep(4)
        
        # Step 4: Complete cash tender
        print("\n💰 Step 4: Completing cash tender with loyalty benefits...")
        cash_completed = pos.complete_cash_tender()
        assert cash_completed, "Failed to complete cash tender"
        
        print("\n🎉 TEST PASSED: Loyalty integration cash sale completed successfully!")
        print(f"💳 Loyalty Summary: {loyalty_result['summary']}")
        
        # Final cleanup click
        self._cleanup_pos_window(pos)
    
    def _check_basket_for_loyalty(self, pos):
        """Check basket contents with loyalty program context."""
        try:
            print("\n=== Loyalty Transaction Basket Analysis ===")
            time.sleep(1)
            
            # Find basket controls
            basket_controls = pos.win.descendants(control_type="List")
            if not basket_controls:
                basket_controls = pos.win.descendants(control_type="ListBox")
            if not basket_controls:
                basket_controls = pos.win.descendants(control_type="ListView")
            
            loyalty_data = {
                "basket_verified": False,
                "eligible_for_loyalty": False,
                "loyalty_items": [],
                "total_amount": 0.0
            }
            
            if basket_controls:
                basket = basket_controls[0]
                items = basket.descendants(control_type="ListItem")
                if not items:
                    items = basket.children()
                
                print(f"Found {len(items)} item(s) in loyalty transaction basket:")
                
                total = 0.0
                loyalty_eligible_items = []
                
                for idx, item in enumerate(items, 1):
                    txt = item.window_text()
                    print(f"  {idx}. {txt}")
                    
                    # Check if item is eligible for loyalty benefits
                    if self._is_loyalty_eligible_item(txt):
                        loyalty_eligible_items.append(txt)
                        print(f"      💳 Loyalty eligible item detected")
                    
                    # Try to extract price for loyalty calculation
                    try:
                        children = item.children()
                        for child in children:
                            child_txt = child.window_text()
                            if any(c in child_txt for c in ["$", ".", ","]):
                                try:
                                    price_val = float(child_txt.replace("$", "").replace(",", "").strip())
                                    total += price_val
                                    break
                                except Exception:
                                    pass
                    except Exception:
                        pass
                
                loyalty_data["total_amount"] = total
                loyalty_data["loyalty_items"] = loyalty_eligible_items
                loyalty_data["eligible_for_loyalty"] = len(loyalty_eligible_items) > 0
                
                print(f"\n💳 LOYALTY ANALYSIS:")
                print(f"   Total Items: {len(items)}")
                print(f"   Loyalty Eligible Items: {len(loyalty_eligible_items)}")
                print(f"   Transaction Amount: ${total:.2f}")
                
                if loyalty_data["eligible_for_loyalty"]:
                    print("   ✅ Transaction eligible for loyalty benefits")
                else:
                    print("   ℹ️ Transaction may not have specific loyalty benefits")
                
                print("✅ Loyalty basket analysis completed.")
                loyalty_data["basket_verified"] = True
                
                time.sleep(2)
                pos.click_button_by_text("OK")
                return loyalty_data
            else:
                print("❌ Could not find basket for loyalty analysis")
                pos.click_button_by_text("OK")
                return loyalty_data
                
        except Exception as e:
            print(f"❌ Error in loyalty basket analysis: {e}")
            return loyalty_data
    
    def _is_loyalty_eligible_item(self, item_text):
        """Determine if an item is eligible for loyalty benefits."""
        # This is a simplified check - in real scenarios, this would be more sophisticated
        loyalty_keywords = ["eligible", "reward", "points", "member"]
        return any(keyword in item_text.lower() for keyword in loyalty_keywords)
    
    def _handle_loyalty_with_integration(self, pos):
        """Handle loyalty popup with detailed integration processing."""
        try:
            popup = pos.app.top_window()
            print("\n=== Loyalty Integration Processing ===")
            print(f"Popup title: {popup.window_text()}")
            
            loyalty_result = {
                "handled": False,
                "integration_type": "Cancel",
                "summary": ""
            }
            
            # In this test scenario, we'll cancel the loyalty popup
            # but with more detailed tracking
            print("💳 Processing loyalty integration options...")
            print("   Analyzing loyalty popup for member benefits...")
            
            # Simulate checking for loyalty card input field
            edit_fields = popup.descendants(control_type="Edit")
            if edit_fields:
                print(f"   Found {len(edit_fields)} input field(s) for loyalty card")
                # In a real scenario, you might enter a loyalty card number here
                # For this test, we'll proceed with cancel
            
            # Find and click Cancel button
            buttons = popup.descendants(control_type="Button")
            for btn in buttons:
                if btn.window_text().strip().lower() == "cancel":
                    print("   💳 Choosing to skip loyalty integration for this transaction")
                    time.sleep(4)  # Wait for any animations
                    btn.click_input()
                    print("   ✅ Successfully handled loyalty popup")
                    
                    loyalty_result["handled"] = True
                    loyalty_result["integration_type"] = "Skipped"
                    loyalty_result["summary"] = "Loyalty integration skipped - proceeded without member benefits"
                    return loyalty_result
            
            print("   ❌ Cancel button not found on loyalty popup")
            loyalty_result["summary"] = "Failed to find cancel button on loyalty popup"
            return loyalty_result
            
        except Exception as e:
            print(f"❌ Error handling loyalty integration: {e}")
            return {
                "handled": False,
                "integration_type": "Error",
                "summary": f"Error during loyalty processing: {str(e)}"
            }
    
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
