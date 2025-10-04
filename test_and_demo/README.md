# Test and Demo Files

This directory contains all test files and demonstration scripts for the Mortgage Visualization project.

## Test Files

### `test_app.py`
Test script to verify the Streamlit app works correctly. Tests the core mortgage calculation functions.

### `tests/`
Directory containing unit tests:
- `test_calculator.py` - Unit tests for the MortgageCalculator class

## Demo Files

### `demo.py`
Quick demo script showing basic mortgage calculator functionality with predefined rates.

### `simple_demo.py`
Simple demo script with no visualization dependencies - just the core calculations.

### `simple_sample_demo.py`
Demo using sample data from `sample_loans.json` without visualization dependencies.

### `demo_scenarios.py`
Demo script showing different home buying scenarios with various home prices and down payments.

### `run_sample_data_fixed.py`
Fixed version of the sample data runner with additional error handling and improvements.

### `interactive_mortgage_input.py`
Interactive mortgage calculator that allows users to input their own rates and terms instead of using static values.

## Running the Files

All files in this directory have been updated with proper import paths to work from this subdirectory. You can run them directly:

```bash
# Run a specific demo
python3 test_and_demo/demo.py

# Run the interactive calculator
python3 test_and_demo/interactive_mortgage_input.py

# Run tests
python3 -m pytest test_and_demo/tests/
```

## Notes

- All files have been updated to use relative imports that work from this subdirectory
- Data file paths have been updated to reference `../data/sample_loans.json`
- The files maintain all their original functionality while being properly organized
