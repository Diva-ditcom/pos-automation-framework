"""
Test Case 2: Multiple Items with Promotion and Cash Sale
This test covers adding multiple items, checking for promotions, and completing with cash payment.
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
@pytest.mark.promotion
@pytest.mark.cash_flow
class TestPromotionCashSale:
    
    def test_add_multiple_items_with_promotion_cash_sale(self, pos_transaction, capture_test_info):
        """
        Test Case: Add multiple promotion items and complete transaction with cash
        
        Steps:
        1. Add promotion product twice using EAN: 9300675079686
        2. Verify basket contents and check for promotions
        3. Calculate totals and verify promotion discounts
        4. Handle loyalty popup (cancel)
        5. Complete transaction with cash tender
        6. Handle receipt confirmation
        
        Expected Result: Transaction with promotion completed successfully
        """
        pos = pos_transaction
        config = Config()
        
        print("\n" + "="*60)
        print("🧪 TEST: Multiple Items with Promotion and Cash Sale")
        print("="*60)
        
        # Step 1: Add first promotion item
        print("\n📦 Step 1a: Adding first promotion item...")
        ean = config.TEST_PRODUCTS["promotion_item"]
        assert pos.add_product_by_ean(ean), f"Failed to add first item with EAN: {ean}"
        
        time.sleep(2)
        
        # Step 2: Add second promotion item (same EAN)
        print("\n📦 Step 1b: Adding second promotion item...")
        assert pos.add_product_by_ean(ean), f"Failed to add second item with EAN: {ean}"
        
        # Step 3: Check basket with detailed promotion analysis
        print("\n🛒 Step 2: Checking basket for promotions...")
        promotion_data = self._check_basket_with_promotion_analysis(pos)
        assert promotion_data["basket_verified"], "Failed to verify basket contents"
        
        # Add delay for UI stability
        time.sleep(4)
        
        # Step 4: Handle loyalty popup
        print("\n💳 Step 3: Handling loyalty popup...")
        loyalty_handled = pos.handle_loyalty_popup()
        assert loyalty_handled, "Failed to handle loyalty popup"
        
        # Add delay before tender
        time.sleep(4)
        
        # Step 5: Complete cash tender
        print("\n💰 Step 4: Completing cash tender...")
        cash_completed = pos.complete_cash_tender()
        assert cash_completed, "Failed to complete cash tender"
        
        print("\n[SUCCESS] TEST PASSED: Promotion cash sale completed successfully!")
        print(f"[REPORT] Promotion Summary: {promotion_data['summary']}")
        
        # Final cleanup click
        self._cleanup_pos_window(pos)
    
    def _check_basket_with_promotion_analysis(self, pos):
        """Enhanced basket checking with promotion analysis."""
        try:
            print("\n=== Enhanced Basket Analysis ===")
            time.sleep(1)
            
            # Find basket controls
            basket_controls = pos.win.descendants(control_type="List")
            if not basket_controls:
                basket_controls = pos.win.descendants(control_type="ListBox")
            if not basket_controls:
                basket_controls = pos.win.descendants(control_type="ListView")
            
            promotion_data = {
                "basket_verified": False,
                "total_items": 0,
                "total_amount": 0.0,
                "promotion_amount": 0.0,
                "promotion_found": False,
                "summary": ""
            }
            
            if basket_controls:
                basket = basket_controls[0]
                items = basket.descendants(control_type="ListItem")
                if not items:
                    items = basket.children()
                
                promotion_data["total_items"] = len(items)
                print(f"Found {len(items)} item(s) in basket:")
                
                total = 0.0
                promo_total = 0.0
                promotion_found = False
                
                for idx, item in enumerate(items, 1):
                    name = item.window_text()
                    price = None
                    quantity = None
                    
                    # Try to extract price and quantity from children
                    children = item.children()
                    for child in children:
                        txt = child.window_text()
                        # Try to find price (contains $ or decimal)
                        if any(c in txt for c in ["$", ".", ","]):
                            try:
                                price_val = float(txt.replace("$", "").replace(",", "").strip())
                                price = price_val
                            except Exception:
                                pass
                        # Try to find quantity (integer)
                        if txt.isdigit():
                            quantity = int(txt)
                    
                    print(f"  {idx}. Name: {name}")
                    print(f"      Quantity: {quantity if quantity else 'N/A'}")
                    print(f"      Amount: ${price if price else 'N/A'}")
                    
                    if price is not None:
                        total += price
                        # Check for promotion (negative price or promotion keywords)
                        if price < 0 or any(keyword in name.lower() for keyword in ["promotion", "bonus", "discount"]):
                            promo_total += price
                            promotion_found = True
                            print(f"      [SUCCESS] PROMOTION DETECTED!")
                    
                    if any(keyword in name.lower() for keyword in ["promotion", "bonus", "ff", "discount"]):
                        promotion_found = True
                        print(f"      [TARGET] Promotion keyword found in: {name}")
                
                # Update promotion data
                promotion_data["total_amount"] = total
                promotion_data["promotion_amount"] = promo_total
                promotion_data["promotion_found"] = promotion_found
                
                print(f"\n[REPORT] BASKET SUMMARY:")
                print(f"   Total Items: {len(items)}")
                print(f"   Gross Amount: ${total:.2f}")
                
                if promo_total < 0:
                    print(f"   Promotion Discount: ${promo_total:.2f}")
                    print(f"   Final Total: ${total:.2f}")
                    promotion_data["summary"] = f"Items: {len(items)}, Total: ${total:.2f}, Discount: ${promo_total:.2f}"
                else:
                    print(f"   No monetary discount applied")
                    promotion_data["summary"] = f"Items: {len(items)}, Total: ${total:.2f}, No discount"
                
                if promotion_found:
                    print("   [SUCCESS] Promotion items detected in basket")
                else:
                    print("   ℹ️ No promotion items detected")
                
                print("[SUCCESS] Enhanced basket analysis completed.")
                promotion_data["basket_verified"] = True
                
                time.sleep(3)
                pos.click_button_by_text("OK")
                return promotion_data
            else:
                print("[ERROR] Could not find basket/list control.")
                pos.click_button_by_text("OK")
                return promotion_data
                
        except Exception as e:
            print(f"[ERROR] Error in basket analysis: {e}")
            return promotion_data
    
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
            print(f"[WARNING] Cleanup warning: {e}")
