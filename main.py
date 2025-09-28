from src.mortgage_calculator import MortgageCalculator, MortgageComparison
from src.visualizations import MortgageVisualizer
import pandas as pd
import os

def main():
    """Main application function."""
    print("🏠 Mortgage Amortization Calculator")
    print("=" * 50)
    
    # Get user input
    principal = float(input("Enter loan amount: $") or "500000")
    
    # Create comparison
    comparison = MortgageComparison()
    
    # Add 15-year loan at 5%
    loan_15yr = comparison.add_loan(
        principal=principal,
        annual_rate=0.05,
        years=15,
        loan_name="15-Year @ 5.0%"
    )
    
    # Add 30-year loan at 6.5%
    loan_30yr = comparison.add_loan(
        principal=principal,
        annual_rate=0.065,
        years=30,
        loan_name="30-Year @ 6.5%"
    )
    
    # Generate amortization tables
    print("\nGenerating amortization tables...")
    loan_15yr.generate_amortization_table()
    loan_30yr.generate_amortization_table()
    
    # Display comparison
    print("\n" + "="*60)
    print("LOAN COMPARISON SUMMARY")
    print("="*60)
    
    comparison_df = comparison.compare_loans()
    print(comparison_df[['loan_name', 'monthly_payment', 'total_interest', 'total_paid']].to_string(index=False))
    
    # Calculate savings
    monthly_diff = loan_15yr.monthly_payment - loan_30yr.monthly_payment
    interest_savings = loan_30yr.get_loan_summary()['total_interest'] - loan_15yr.get_loan_summary()['total_interest']
    
    print(f"\nKey Insights:")
    print(f"• 15-year loan costs ${monthly_diff:,.2f} more per month")
    print(f"• 15-year loan saves ${interest_savings:,.2f} in total interest")
    print(f"• Interest savings: {(interest_savings/loan_30yr.get_loan_summary()['total_interest']*100):.1f}%")
    
    # Create visualizations
    print("\nCreating visualizations...")
    visualizer = MortgageVisualizer()
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Generate plots
    visualizer.plot_amortization_schedule(loan_15yr, "output/15yr_amortization.png")
    visualizer.plot_amortization_schedule(loan_30yr, "output/30yr_amortization.png")
    visualizer.plot_loan_comparison(comparison, "output/loan_comparison.png")
    visualizer.plot_balance_comparison(comparison, "output/balance_comparison.png")
    visualizer.create_interactive_dashboard(comparison, "output/interactive_dashboard.html")
    
    # Save data
    print("\nSaving data...")
    loan_15yr.amortization_table.to_csv("output/15yr_amortization.csv", index=False)
    loan_30yr.amortization_table.to_csv("output/30yr_amortization.csv", index=False)
    comparison_df.to_csv("output/loan_comparison.csv", index=False)
    
    print("\n✅ Analysis complete! Check the 'output' folder for results.")
    print("📊 Files generated:")
    print("  • 15yr_amortization.png - 15-year loan amortization chart")
    print("  • 30yr_amortization.png - 30-year loan amortization chart")
    print("  • loan_comparison.png - Side-by-side loan comparison")
    print("  • balance_comparison.png - Balance comparison over time")
    print("  • interactive_dashboard.html - Interactive dashboard")
    print("  • CSV files with detailed data")

if __name__ == "__main__":
    main()
