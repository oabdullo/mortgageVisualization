#!/usr/bin/env python3
"""
Script to run mortgage analysis using data from sample_loans.json
"""

import json
from src.mortgage_calculator import MortgageCalculator, MortgageComparison
from src.visualizations import MortgageVisualizer
import os

def load_sample_loans(json_file="data/sample_loans.json"):
    """Load loan data from JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data['sample_loans']

def run_analysis_with_sample_data():
    """Run mortgage analysis using sample loan data."""
    print("🏠 Mortgage Amortization Calculator - Sample Data Analysis")
    print("=" * 60)
    
    # Load sample loans
    print("Loading sample loan data...")
    sample_loans = load_sample_loans()
    
    # Create comparison
    comparison = MortgageComparison()
    
    # Add each loan from the sample data
    loans = []
    for loan_data in sample_loans:
        loan = comparison.add_loan(
            principal=loan_data['principal'],
            annual_rate=loan_data['annual_rate'],
            years=loan_data['years'],
            loan_name=loan_data['name']
        )
        loans.append(loan)
        print(f"Added: {loan_data['name']} - ${loan_data['principal']:,} @ {loan_data['annual_rate']*100:.1f}% for {loan_data['years']} years")
    
    # Generate amortization tables
    print("\nGenerating amortization tables...")
    for loan in loans:
        loan.generate_amortization_table()
    
    # Display comparison
    print("\n" + "="*80)
    print("LOAN COMPARISON SUMMARY")
    print("="*80)
    
    comparison_df = comparison.compare_loans()
    print(comparison_df[['loan_name', 'monthly_payment', 'total_interest', 'total_paid']].to_string(index=False))
    
    # Show key insights
    print(f"\nKey Insights:")
    for i, loan in enumerate(loans):
        summary = loan.get_loan_summary()
        print(f"• {loan.loan_name}: ${summary['monthly_payment']:,.2f}/month, ${summary['total_interest']:,.2f} total interest")
    
    # Find best and worst options
    monthly_payments = [loan.monthly_payment for loan in loans]
    total_interests = [loan.get_loan_summary()['total_interest'] for loan in loans]
    
    min_payment_idx = monthly_payments.index(min(monthly_payments))
    min_interest_idx = total_interests.index(min(total_interests))
    
    print(f"\n• Lowest monthly payment: {loans[min_payment_idx].loan_name} (${monthly_payments[min_payment_idx]:,.2f})")
    print(f"• Lowest total interest: {loans[min_interest_idx].loan_name} (${total_interests[min_interest_idx]:,.2f})")
    
    # Show first few months of each loan
    for loan in loans:
        print(f"\nFirst 3 months of {loan.loan_name}:")
        print(loan.amortization_table[['Month', 'Payment', 'Principal', 'Interest', 'Remaining_Balance']].head(3).to_string(index=False))
    
    # Create visualizations
    print("\nCreating visualizations...")
    visualizer = MortgageVisualizer()
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Generate plots for each loan
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        visualizer.plot_amortization_schedule(loan, f"output/{safe_name}_amortization.png")
    
    # Generate comparison plots
    visualizer.plot_loan_comparison(comparison, "output/sample_loans_comparison.png")
    visualizer.plot_balance_comparison(comparison, "output/sample_loans_balance_comparison.png")
    visualizer.create_interactive_dashboard(comparison, "output/sample_loans_dashboard.html")
    
    # Save data
    print("\nSaving data...")
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        loan.amortization_table.to_csv(f"output/{safe_name}_amortization.csv", index=False)
    
    comparison_df.to_csv("output/sample_loans_comparison.csv", index=False)
    
    print("\n✅ Analysis complete! Check the 'output' folder for results.")
    print("📊 Files generated:")
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        print(f"  • {safe_name}_amortization.png - {loan.loan_name} amortization chart")
        print(f"  • {safe_name}_amortization.csv - {loan.loan_name} detailed data")
    print("  • sample_loans_comparison.png - Side-by-side loan comparison")
    print("  • sample_loans_balance_comparison.png - Balance comparison over time")
    print("  • sample_loans_dashboard.html - Interactive dashboard")
    print("  • sample_loans_comparison.csv - Summary comparison data")

if __name__ == "__main__":
    run_analysis_with_sample_data()
