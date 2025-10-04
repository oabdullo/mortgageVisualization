# Interactive Mortgage Calculator Usage

## Overview
The mortgage calculator now supports two modes:
1. **Sample Data Mode**: Uses predefined rates from `data/sample_loans.json`
2. **Interactive Mode**: Allows you to input your own mortgage rates and terms

## How to Use

### Option 1: Run the Enhanced Main Script
```bash
python3 run_with_sample_data.py
```

When prompted, choose:
- **1** for sample data (predefined rates)
- **2** for custom input (your own rates)

### Option 2: Run the Dedicated Interactive Script
```bash
python3 interactive_mortgage_input.py
```

This script goes directly to the interactive input mode.

## Interactive Input Process

When you choose the interactive mode, you'll be prompted to enter:

1. **Loan Amount (Principal)**: The total amount you want to borrow
2. **Number of Options**: How many different mortgage options you want to compare (1-5)
3. **For Each Option**:
   - **Name**: A descriptive name (e.g., "30-Year Fixed", "15-Year ARM")
   - **Interest Rate**: Annual rate as a percentage (e.g., 6.5 for 6.5%)
   - **Loan Term**: Number of years (e.g., 30, 15, 20)

## Example Session

```
🏠 Interactive Mortgage Calculator
==================================================
Enter loan amount (principal): $400000
Loan amount: $400,000.00

How many mortgage options do you want to compare? (1-5): 3

Enter details for 3 mortgage option(s):
----------------------------------------

Mortgage Option 1:
  Name for this option (e.g., '30-Year Fixed'): 30-Year Fixed
  Annual interest rate (e.g., 6.5 for 6.5%): 6.5
  Loan term in years (e.g., 30): 30
  ✓ Added: 30-Year Fixed - $400,000.00 @ 6.50% for 30 years

Mortgage Option 2:
  Name for this option (e.g., '30-Year Fixed'): 15-Year Fixed
  Annual interest rate (e.g., 6.5 for 6.5%): 5.8
  Loan term in years (e.g., 30): 15
  ✓ Added: 15-Year Fixed - $400,000.00 @ 5.80% for 15 years

Mortgage Option 3:
  Name for this option (e.g., '30-Year Fixed'): 20-Year Fixed
  Annual interest rate (e.g., 6.5 for 6.5%): 6.0
  Loan term in years (e.g., 30): 20
  ✓ Added: 20-Year Fixed - $400,000.00 @ 6.00% for 20 years
```

## Output

The calculator will generate:
- **Comparison Table**: Monthly payments, total interest, and total paid for each option
- **Key Insights**: Summary of each loan option
- **Best Options**: Which loan has the lowest monthly payment and lowest total interest
- **Amortization Details**: First 3 months of each loan's payment schedule
- **Visualizations**: Charts and graphs (if you choose to generate them)
- **Data Files**: CSV files with detailed amortization schedules

## Features

✅ **Dynamic Rate Input**: Enter any interest rate from 0% to 100%
✅ **Flexible Terms**: Choose any loan term from 1 to 50 years
✅ **Multiple Comparisons**: Compare up to 5 different mortgage options
✅ **Custom Names**: Give descriptive names to your loan options
✅ **Comprehensive Analysis**: Get detailed comparisons and insights
✅ **Data Export**: Save results to CSV files
✅ **Visualizations**: Generate charts and interactive dashboards

## Error Handling

The calculator includes robust error handling:
- Invalid numbers default to reasonable values
- Rate validation ensures values are between 0-100%
- Term validation ensures values are between 1-50 years
- Graceful handling of keyboard interrupts (Ctrl+C)

## Files Generated

When you choose to generate visualizations, the following files are created in the `output/` folder:
- `{loan_name}_amortization.png` - Individual amortization charts
- `{loan_name}_amortization.csv` - Detailed payment schedules
- `custom_loan_comparison.png` - Side-by-side comparison
- `custom_balance_comparison.png` - Balance over time
- `custom_dashboard.html` - Interactive dashboard
- `custom_loan_comparison.csv` - Summary comparison data

## Quick Start

1. Run: `python3 run_with_sample_data.py`
2. Choose option 2 (Enter your own mortgage rates)
3. Enter your loan amount
4. Enter the number of options to compare
5. For each option, enter the name, rate, and term
6. Review the comparison results
7. Choose whether to generate visualizations

That's it! You now have a fully interactive mortgage calculator that lets you input your own rates instead of using static values.
