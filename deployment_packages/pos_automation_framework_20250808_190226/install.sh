#!/bin/bash
# One-Click POS Automation Framework Installer

echo "========================================"
echo "POS Automation Framework - One Click Setup"
echo "========================================"
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found"
echo

# Run enhanced setup
echo "🚀 Starting framework installation..."
python3 setup_new_machine_enhanced.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Installation failed!"
    exit 1
fi

echo
echo "🎉 Installation completed successfully!"
echo
echo "📋 Next steps:"
echo "  1. Run: python3 run_all_diagnostics.py"
echo "  2. Open VS Code workspace: pos-automation.code-workspace"
echo "  3. Deploy to GitHub: python3 deploy_to_github.py"
echo
