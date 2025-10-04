#!/usr/bin/env python3
"""
Simple demo script for the Mortgage Amortization Calculator (no visualization dependencies)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mortgage_calculator import MortgageCalculator, MortgageComparison

def simple_demo():
    """Run a simple demonstration of the mortgage calculator."""
    print("🏠 Mortgage Amortization Calculator - Simple Demo")
    print("=" * 50)
    
    # Create a comparison with the specified rates
    comparison = MortgageComparison()
    
    # Add 15-year loan at 5%
    loan_15yr = comparison.add_loan(
        principal=500000,
        annual_rate=0.05,
        years=15,
        loan_name="15-Year @ 5.0%"
    )
    
    # Add 30-year loan at 6.5%
    loan_30yr = comparison.add_loan(
        principal=500000,
        annual_rate=0.065,
        years=30,
        loan_name="30-Year @ 6.5%"
    )
    
    # Generate amortization tables
    print("Generating amortization tables...")
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
    
    # Show first few months of amortization
    print(f"\nFirst 5 months of 15-year loan:")
    print(loan_15yr.amortization_table[['Month', 'Payment', 'Principal', 'Interest', 'Remaining_Balance']].head().to_string(index=False))
    
    print(f"\nFirst 5 months of 30-year loan:")
    print(loan_30yr.amortization_table[['Month', 'Payment', 'Principal', 'Interest', 'Remaining_Balance']].head().to_string(index=False))
    
    # Show year-end balances
    print(f"\nYear-end balances comparison:")
    year_ends_15yr = loan_15yr.get_year_end_balances()
    year_ends_30yr = loan_30yr.get_year_end_balances()
    
    for year in [1, 5, 10, 15, 20, 25, 30]:
        if year <= 15:
            balance_15yr = year_ends_15yr[year_ends_15yr['Year'] == year]['Remaining_Balance'].iloc[0] if year <= len(year_ends_15yr) else 0
            print(f"Year {year:2d}: 15-year: ${balance_15yr:>10,.2f}", end="")
        else:
            print(f"Year {year:2d}: 15-year: ${'Paid Off':>10}", end="")
        
        if year <= 30:
            balance_30yr = year_ends_30yr[year_ends_30yr['Year'] == year]['Remaining_Balance'].iloc[0] if year <= len(year_ends_30yr) else 0
            print(f" | 30-year: ${balance_30yr:>10,.2f}")
        else:
            print(f" | 30-year: ${'Paid Off':>10}")
    
    print("\n✅ Simple demo complete!")
    print("📝 To install full dependencies and run visualizations:")
    print("   pip install -r requirements.txt")
    print("   python main.py")

if __name__ == "__main__":
    simple_demo()
