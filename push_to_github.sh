#!/bin/bash
# GitHub Push Script
# Run this after creating the repository on GitHub

echo "🚀 Pushing POS Automation Framework to GitHub..."
echo "Repository: https://github.com/Diva-ditcom/pos-automation-framework"
echo ""

# Configure git if needed
echo "📋 Configuring Git..."
git config user.name "Diva-ditcom"
git config user.email "diva.ditcom@example.com"

# Show current status
echo "📊 Current Git Status:"
git status --porcelain
echo ""

# Show commits ready to push
echo "📦 Commits ready to push:"
git log --oneline -5
echo ""

# Try to push
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Repository pushed to GitHub!"
    echo "🔗 View at: https://github.com/Diva-ditcom/pos-automation-framework"
    echo "⚡ GitHub Actions will run automatically!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Go to the repository on GitHub"
    echo "   2. Click 'Actions' tab to see the CI/CD pipeline"
    echo "   3. Watch the automated tests run!"
else
    echo ""
    echo "❌ Push failed. You may need to:"
    echo "   1. Create the repository manually on GitHub first"
    echo "   2. Set up authentication (Personal Access Token)"
    echo "   3. Check your internet connection"
fi
