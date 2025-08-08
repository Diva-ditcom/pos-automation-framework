"""
Pytest fixtures for POS automation tests
"""
import pytest
import time
import sys
import os

# Add pywinauto root to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules (IDE may show import error but it works at runtime)
from utils.pos_base import POSAutomation  # type: ignore

@pytest.fixture(scope="session")
def pos_session():
    """Session-scoped fixture to manage POS application lifecycle."""
    pos = POSAutomation()
    
    # Setup: Launch and login to POS if not running
    if not pos.is_pos_running():
        print("\n[LAUNCH] Launching POS application...")
        assert pos.launch_pos(), "Failed to launch POS application"
        time.sleep(10)
    
    print("\n[CONNECT] Connecting to POS...")
    assert pos.connect_to_pos(), "Failed to connect to POS"
    
    # Check if already logged in by looking for No Sale button
    if not pos.check_nosale():
        print("\n🔐 Logging into POS...")
        assert pos.login_to_pos(), "Failed to login to POS"
        assert pos.check_nosale(), "POS not ready after login"
    else:
        print("\n[SUCCESS] POS already logged in and ready")
    
    yield pos
    
    # Teardown: Click randomly to ensure POS is in good state
    print("\n🧹 Cleaning up POS session...")
    try:
        import random
        rect = pos.win.rectangle()
        x = random.randint(rect.left + 50, rect.right - 50)
        y = random.randint(rect.top + 50, rect.bottom - 50)
        pos.win.click_input(coords=(x, y))
        print(f"[SUCCESS] Cleanup completed - clicked at ({x}, {y})")
    except Exception as e:
        print(f"[WARNING] Cleanup warning: {e}")

@pytest.fixture(scope="function")
def pos_transaction(pos_session):
    """Function-scoped fixture for individual transactions."""
    pos = pos_session
    
    # Ensure POS is ready before each test
    assert pos.check_nosale(), "POS not ready for transaction"
    
    yield pos
    
    # Reset POS state after each test
    time.sleep(1)
    print("🔄 Transaction completed")

@pytest.fixture(scope="function")
def capture_test_info(request):
    """Fixture to capture test information for reporting."""
    test_info = {
        'name': request.node.name,
        'module': request.module.__name__,
        'start_time': time.time()
    }
    
    yield test_info
    
    test_info['end_time'] = time.time()
    test_info['duration'] = test_info['end_time'] - test_info['start_time']
    print(f"\n[REPORT] Test '{test_info['name']}' completed in {test_info['duration']:.2f} seconds")


# Data-Driven Fixtures for CSV-based testing
@pytest.fixture(scope="function") 
def pos_automation_with_scenario(request):
    """Data-driven POS automation fixture that loads scenario data"""
    # Import here to avoid circular imports
    from data.csv_data_manager import csv_data_manager  # type: ignore
    
    # Get scenario name from test function name or parameter
    scenario_name = getattr(request, 'param', None)
    
    if not scenario_name:
        # Try to extract scenario name from test function name
        test_name = request.node.name
        if 'basic_cash_sale' in test_name:
            scenario_name = 'basic_cash_sale'
        elif 'promotion_cash_sale' in test_name:
            scenario_name = 'promotion_cash_sale'
        elif 'loyalty_cash_sale' in test_name:
            scenario_name = 'loyalty_cash_sale'
    
    if scenario_name:
        print(f"\n[TARGET] Setting up test with scenario: {scenario_name}")
        automation = POSAutomation(scenario_name)
        
        # Validate scenario data before test
        if not automation.scenario_data:
            pytest.fail(f"Failed to load data for scenario: {scenario_name}")
        
        yield automation
    else:
        # Fallback to basic fixture
        print("\n[WARNING] No scenario detected, using basic automation")
        automation = POSAutomation()
        yield automation


@pytest.fixture(scope="session")
def available_scenarios():
    """Fixture that provides list of available test scenarios"""
    from data.csv_data_manager import csv_data_manager  # type: ignore
    scenarios = csv_data_manager.list_available_scenarios()
    print(f"\n📋 Available test scenarios: {scenarios}")
    return scenarios


def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line(
        "markers", 
        "scenario(name): mark test to run with specific scenario data"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add scenario information"""
    for item in items:
        # Add scenario marker based on test name
        if 'basic_cash_sale' in item.name:
            item.add_marker(pytest.mark.scenario(name='basic_cash_sale'))
        elif 'promotion_cash_sale' in item.name:
            item.add_marker(pytest.mark.scenario(name='promotion_cash_sale'))
        elif 'loyalty_cash_sale' in item.name:
            item.add_marker(pytest.mark.scenario(name='loyalty_cash_sale'))
