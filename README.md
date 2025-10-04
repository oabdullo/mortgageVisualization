# 🏠 Mortgage Amortization Calculator

A comprehensive Python tool for calculating and visualizing mortgage amortization schedules, with support for comparing different loan terms and interest rates.

## Features

- 📊 **Complete Amortization Tables**: Generate detailed month-by-month payment breakdowns
- 🔄 **Loan Comparison**: Compare multiple mortgage options side-by-side
- 📈 **Data Visualization**: Create charts and interactive dashboards
- 💾 **Export Options**: Save results to CSV and generate visual reports
- 🎯 **Flexible Input**: Support for any loan amount, interest rate, and term
- 🖥️ **Interactive Mode**: Input your own mortgage rates instead of using static values

## Project Structure

```
mortgage_visualization/
├── src/                          # Core source code
│   ├── mortgage_calculator.py    # Main calculator classes
│   └── visualizations.py         # Chart and dashboard generation
├── test_and_demo/                # Test files and demo scripts
│   ├── tests/                    # Unit tests
│   ├── demo.py                   # Basic demo
│   ├── simple_demo.py            # Simple demo (no viz dependencies)
│   └── interactive_mortgage_input.py  # Interactive rate input
├── data/                         # Sample data files
├── output/                       # Generated charts and CSV files
├── notebooks/                    # Jupyter notebooks for analysis
├── app.py                        # Streamlit web app
├── main.py                       # Original main script
└── run_with_sample_data.py       # Enhanced main script with interactive mode
```

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the calculator**
   ```bash
   # Main interactive calculator
   python run_with_sample_data.py
   
   # Or use the original main script
   python main.py
   ```

3. **Run tests and demos**
   ```bash
   # Run demos
   python test_and_demo/demo.py
   python test_and_demo/simple_demo.py
   
   # Run interactive calculator
   python test_and_demo/interactive_mortgage_input.py
   
   # Run tests
   python -m pytest test_and_demo/tests/
   ```

## Usage Examples

### Basic Usage
```python
from src.mortgage_calculator import MortgageCalculator

# Create a 30-year mortgage calculator
loan = MortgageCalculator(
    principal=500000,
    annual_rate=0.065,
    years=30,
    loan_name="My House"
)

# Generate amortization table
amortization_table = loan.generate_amortization_table()

# Get loan summary
summary = loan.get_loan_summary()
print(f"Monthly payment: ${summary['monthly_payment']:,.2f}")
```

### Comparing Multiple Loans
```python
from src.mortgage_calculator import MortgageComparison

comparison = MortgageComparison()

# Add different loan options
comparison.add_loan(500000, 0.05, 15, "15-Year @ 5%")
comparison.add_loan(500000, 0.065, 30, "30-Year @ 6.5%")

# Compare loans
comparison_df = comparison.compare_loans()
print(comparison_df)
```

### Creating Visualizations
```python
from src.visualizations import MortgageVisualizer

visualizer = MortgageVisualizer()

# Plot amortization schedule
visualizer.plot_amortization_schedule(loan)

# Compare multiple loans
visualizer.plot_loan_comparison(comparison)

# Create interactive dashboard
visualizer.create_interactive_dashboard(comparison)
```

## Project Structure

```
mortgage visualization/
├── src/
│   ├── mortgage_calculator.py    # Core calculation logic
│   └── visualizations.py         # Chart and dashboard creation
├── notebooks/
│   └── analysis.ipynb           # Jupyter notebook for analysis
├── tests/
│   └── test_calculator.py       # Unit tests
├── data/                        # Sample data files
├── output/                      # Generated reports and charts
├── main.py                      # Main application
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Key Calculations

### Monthly Payment Formula
```
M = P [ r(1 + r)^n ] / [ (1 + r)^n - 1 ]
```
Where:
- M = Monthly payment
- P = Principal loan amount
- r = Monthly interest rate (annual rate / 12)
- n = Total number of payments (years × 12)

### Interest vs Principal
- **Interest Payment** = Remaining Balance × Monthly Rate
- **Principal Payment** = Monthly Payment - Interest Payment
- **New Balance** = Previous Balance - Principal Payment

## Visualization Features

- **Amortization Schedules**: Principal vs interest over time
- **Balance Tracking**: Remaining balance progression
- **Loan Comparisons**: Side-by-side analysis
- **Interactive Dashboards**: Plotly-powered interactive charts
- **Export Options**: PNG, HTML, and CSV formats

## Sample Output

The calculator generates:
- Monthly payment amounts
- Total interest paid over loan life
- Year-end balance summaries
- Principal vs interest breakdowns
- Visual charts and interactive dashboards

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python, Pandas, Matplotlib, and Plotly
- Inspired by the need for clear mortgage analysis tools
- Designed for both personal use and educational purposes
