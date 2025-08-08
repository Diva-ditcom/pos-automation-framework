#!/usr/bin/env python3
"""
Quick POS Connection Test
Tests if the framework can connect to your R10PosClient application
"""

import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from config.config import Config  # type: ignore
    from utils.pos_base import POSAutomation  # type: ignore
    from pywinauto import Application, find_windows
    
    def test_pos_connection():
        """Test POS application connection"""
        print("🔧 POS Connection Test")
        print("=" * 40)
        
        # Load configuration
        config = Config()
        print(f"✅ Configuration loaded")
        print(f"   Launch path: {config.POS_LAUNCH_PATH}")
        print(f"   Title regex: {config.POS_TITLE_REGEX}")
        
        # Check if POS is already running
        print(f"\n🔍 Checking for existing POS windows...")
        try:
            wins = find_windows(title_re=config.POS_TITLE_REGEX)
            if wins:
                print(f"✅ Found {len(wins)} POS window(s):")
                for i, win in enumerate(wins):
                    print(f"   Window {i+1}: {win.window_text()}")
            else:
                print("⚠️ No POS windows found")
        except Exception as e:
            print(f"❌ Error finding windows: {e}")
        
        # Test connection with POSAutomation
        print(f"\n🤖 Testing POSAutomation connection...")
        try:
            pos = POSAutomation()
            if pos.connect_to_pos():
                print("✅ Successfully connected to POS!")
                print(f"   App: {pos.app}")
                print(f"   Window: {pos.win}")
                return True
            else:
                print("❌ Failed to connect to POS")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    if __name__ == "__main__":
        success = test_pos_connection()
        print("\n" + "=" * 40)
        if success:
            print("🎉 POS connection test PASSED!")
        else:
            print("💡 Troubleshooting tips:")
            print("   • Make sure your POS application is running")
            print("   • Verify the title regex matches your app window")
            print("   • Check if the window title contains 'R10PosClient'")
        
        input("\nPress Enter to continue...")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the correct directory")
    input("Press Enter to continue...")
