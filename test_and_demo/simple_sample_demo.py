#!/usr/bin/env python3
"""
Simple demo script using sample_loans.json data (no visualization dependencies)
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mortgage_calculator import MortgageCalculator, MortgageComparison

def load_sample_loans(json_file="../data/sample_loans.json"):
    """Load loan data from JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def simple_sample_demo():
    """Run a simple demonstration using sample loan data."""
    print("🏠 Mortgage Amortization Calculator - Sample Data Demo")
    print("=" * 60)
    
    # Load sample loans
    print("Loading sample loan data...")
    data = load_sample_loans()
    sample_loans = data['sample_loans']
    home_price = data.get('home_price', 400000)
    down_payment = data.get('down_payment', 92000)
    loan_amount = home_price - down_payment
    
    print(f"Home Price: ${home_price:,}")
    print(f"Down Payment: ${down_payment:,} ({(down_payment/home_price)*100:.1f}%)")
    print(f"Loan Amount: ${loan_amount:,}")
    
    # Create comparison
    comparison = MortgageComparison()
    
    # Add each loan from the sample data
    loans = []
    for loan_data in sample_loans:
        loan = comparison.add_loan(
            principal=loan_amount,
            annual_rate=loan_data['annual_rate'],
            years=loan_data['years'],
            loan_name=loan_data['name']
        )
        loans.append(loan)
        print(f"Added: {loan_data['name']} - ${loan_amount:,} @ {loan_data['annual_rate']*100:.1f}% for {loan_data['years']} years")
    
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
    
    # Show year-end balances for comparison
    print(f"\nYear-end balances comparison:")
    year_ends = {}
    for loan in loans:
        year_ends[loan.loan_name] = loan.get_year_end_balances()
    
    max_years = max([loan.years for loan in loans])
    for year in range(1, min(max_years + 1, 11)):  # Show first 10 years
        print(f"Year {year:2d}:", end="")
        for loan in loans:
            if year <= loan.years:
                balance = year_ends[loan.loan_name][year_ends[loan.loan_name]['Year'] == year]['Remaining_Balance'].iloc[0] if year <= len(year_ends[loan.loan_name]) else 0
                print(f" {loan.loan_name}: ${balance:>10,.2f}", end="")
            else:
                print(f" {loan.loan_name}: ${'Paid Off':>10}", end="")
        print()
    
    print("\n✅ Sample data demo complete!")
    print("📝 To install full dependencies and run with visualizations:")
    print("   pip install -r requirements.txt")
    print("   python run_with_sample_data.py")

if __name__ == "__main__":
    simple_sample_demo()
