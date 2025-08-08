@echo off
REM POS Automation Test Suite Runner
REM This batch file provides easy access to run different test scenarios

echo ================================================================
echo                 POS AUTOMATION TEST SUITE
echo ================================================================
echo.

:MENU
echo Please select an option:
echo.
echo 1. Run All Tests
echo 2. Run Basic Cash Sale Test
echo 3. Run Promotion Cash Sale Test  
echo 4. Run Loyalty Cash Sale Test
echo 5. Run Smoke Tests Only
echo 6. Run Regression Tests Only
echo 7. Open Reports Folder
echo 8. Exit
echo.

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto RUN_ALL
if "%choice%"=="2" goto RUN_BASIC
if "%choice%"=="3" goto RUN_PROMOTION
if "%choice%"=="4" goto RUN_LOYALTY
if "%choice%"=="5" goto RUN_SMOKE
if "%choice%"=="6" goto RUN_REGRESSION
if "%choice%"=="7" goto OPEN_REPORTS
if "%choice%"=="8" goto EXIT

echo Invalid choice. Please try again.
echo.
goto MENU

:RUN_ALL
echo Running all POS automation tests...
python run_tests.py
goto COMPLETE

:RUN_BASIC
echo Running Basic Cash Sale test...
python run_tests.py test_01_basic_cash_sale
goto COMPLETE

:RUN_PROMOTION
echo Running Promotion Cash Sale test...
python run_tests.py test_02_promotion_cash_sale
goto COMPLETE

:RUN_LOYALTY
echo Running Loyalty Cash Sale test...
python run_tests.py test_03_loyalty_cash_sale
goto COMPLETE

:RUN_SMOKE
echo Running Smoke tests only...
python -m pytest tests/pos_automation/ -m smoke --html=reports/smoke_report.html --self-contained-html -v
goto COMPLETE

:RUN_REGRESSION
echo Running Regression tests only...
python -m pytest tests/pos_automation/ -m regression --html=reports/regression_report.html --self-contained-html -v
goto COMPLETE

:OPEN_REPORTS
echo Opening reports folder...
start explorer reports
goto MENU

:COMPLETE
echo.
echo Test execution completed!
echo Check the reports folder for detailed results.
echo.
pause
goto MENU

:EXIT
echo.
echo Thank you for using POS Automation Test Suite!
echo.
pause
