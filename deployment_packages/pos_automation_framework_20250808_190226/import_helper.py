#!/usr/bin/env python3
"""
Import Helper for VS Code - POS Automation Framework
This script provides alternative import methods for VS Code development
"""

import sys
import os
from typing import Any, Optional

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def safe_import(module_path: str, class_name: Optional[str] = None) -> Any:
    """
    Safely import a module or class with fallback error handling
    
    Args:
        module_path: Python module path (e.g., 'config.config')
        class_name: Optional class name to extract from module
        
    Returns:
        Imported module or class, or None if import fails
    """
    try:
        # Try standard import first
        if class_name:
            module = __import__(module_path, fromlist=[class_name])
            return getattr(module, class_name)
        else:
            return __import__(module_path)
    except ImportError:
        try:
            # Fallback to importlib method
            import importlib.util
            
            # Convert module path to file path
            parts = module_path.split('.')
            file_path = os.path.join(current_dir, *parts[:-1], f"{parts[-1]}.py")
            
            if os.path.exists(file_path):
                spec = importlib.util.spec_from_file_location(module_path, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if class_name:
                        return getattr(module, class_name, None)
                    else:
                        return module
        except Exception as e:
            print(f"Failed to import {module_path}: {e}")
            
        return None

# Pre-import common framework components for VS Code
try:
    Config = safe_import('config.config', 'Config')
    csv_data_manager = safe_import('data.csv_data_manager', 'csv_data_manager')
    POSAutomation = safe_import('utils.pos_base', 'POSAutomation')
    
    # Export for easy importing in other scripts
    __all__ = ['Config', 'csv_data_manager', 'POSAutomation', 'safe_import']
    
except Exception as e:
    print(f"Import helper initialization failed: {e}")

if __name__ == "__main__":
    print("POS Automation Framework - Import Helper")
    print("=" * 50)
    
    # Test all imports
    modules = [
        ('config.config', 'Config'),
        ('data.csv_data_manager', 'csv_data_manager'),
        ('utils.pos_base', 'POSAutomation')
    ]
    
    for module_path, class_name in modules:
        result = safe_import(module_path, class_name)
        status = "✓" if result else "✗"
        print(f"{status} {module_path}.{class_name}: {'Success' if result else 'Failed'}")
    
    print("\nImport helper ready for use in VS Code!")
