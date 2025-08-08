#!/usr/bin/env powershell
# GitHub Push Script for Windows
# Run this after creating the repository on GitHub

Write-Host "🚀 Pushing POS Automation Framework to GitHub..." -ForegroundColor Green
Write-Host "Repository: https://github.com/Diva-ditcom/pos-automation-framework" -ForegroundColor Cyan
Write-Host ""

# Show current status
Write-Host "📊 Current Git Status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Show commits ready to push
Write-Host "📦 Commits ready to push:" -ForegroundColor Yellow
git log --oneline -5
Write-Host ""

# Try to push
Write-Host "🚀 Attempting to push to GitHub..." -ForegroundColor Green
$pushResult = git push -u origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Repository pushed to GitHub!" -ForegroundColor Green
    Write-Host "🔗 View at: https://github.com/Diva-ditcom/pos-automation-framework" -ForegroundColor Cyan
    Write-Host "⚡ GitHub Actions will run automatically!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Go to the repository on GitHub"
    Write-Host "   2. Click 'Actions' tab to see the CI/CD pipeline"
    Write-Host "   3. Watch the automated tests run!"
} else {
    Write-Host ""
    Write-Host "❌ Push failed!" -ForegroundColor Red
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $pushResult -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 To fix this, you need to:" -ForegroundColor Yellow
    Write-Host "   1. Create the repository manually on GitHub first:" -ForegroundColor White
    Write-Host "      - Go to https://github.com/Diva-ditcom" -ForegroundColor Cyan
    Write-Host "      - Click 'New repository'" -ForegroundColor Cyan
    Write-Host "      - Name: pos-automation-framework" -ForegroundColor Cyan
    Write-Host "      - Don't initialize with README" -ForegroundColor Cyan
    Write-Host "   2. Set up authentication if needed" -ForegroundColor White
    Write-Host "   3. Run this script again" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to continue"
