#!/usr/bin/env python3
"""
Script to run mortgage analysis using data from sample_loans.json (fixed version)
"""

import json
from src.mortgage_calculator import MortgageCalculator, MortgageComparison
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_sample_loans(json_file="data/sample_loans.json"):
    """Load loan data from JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data['sample_loans']

def create_simple_visualizations(loans, comparison):
    """Create simple visualizations using matplotlib."""
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # 1. Monthly Payment Comparison
    plt.figure(figsize=(10, 6))
    loan_names = [loan.loan_name for loan in loans]
    monthly_payments = [loan.monthly_payment for loan in loans]
    
    plt.bar(loan_names, monthly_payments, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Monthly Payment Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Loan Type', fontsize=12)
    plt.ylabel('Monthly Payment ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for i, v in enumerate(monthly_payments):
        plt.text(i, v + 20, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/monthly_payment_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Total Interest Comparison
    plt.figure(figsize=(10, 6))
    total_interests = [loan.get_loan_summary()['total_interest'] for loan in loans]
    
    plt.bar(loan_names, total_interests, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Total Interest Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Loan Type', fontsize=12)
    plt.ylabel('Total Interest ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for i, v in enumerate(total_interests):
        plt.text(i, v + 5000, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/total_interest_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Balance Over Time (first 10 years)
    plt.figure(figsize=(12, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, loan in enumerate(loans):
        year_ends = loan.get_year_end_balances()
        # Only show first 10 years for better visualization
        year_ends_10yr = year_ends[year_ends['Year'] <= 10]
        plt.plot(year_ends_10yr['Year'], year_ends_10yr['Remaining_Balance'], 
                marker='o', linewidth=2, label=loan.loan_name, color=colors[i])
    
    plt.title('Remaining Balance Over Time (First 10 Years)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Remaining Balance ($)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/balance_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Amortization Schedule (Principal vs Interest)
    fig, axes = plt.subplots(1, len(loans), figsize=(15, 5))
    if len(loans) == 1:
        axes = [axes]
    
    for i, loan in enumerate(loans):
        # Get first 5 years of data
        amort_data = loan.amortization_table[loan.amortization_table['Month'] <= 60]
        
        axes[i].plot(amort_data['Month'], amort_data['Principal'], label='Principal', linewidth=2)
        axes[i].plot(amort_data['Month'], amort_data['Interest'], label='Interest', linewidth=2)
        axes[i].set_title(f'{loan.loan_name}\n(First 5 Years)', fontweight='bold')
        axes[i].set_xlabel('Month')
        axes[i].set_ylabel('Amount ($)')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/amortization_schedules.png', dpi=300, bbox_inches='tight')
    plt.close()

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
    create_simple_visualizations(loans, comparison)
    
    # Save data
    print("\nSaving data...")
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        loan.amortization_table.to_csv(f"output/{safe_name}_amortization.csv", index=False)
    
    comparison_df.to_csv("output/sample_loans_comparison.csv", index=False)
    
    print("\n✅ Analysis complete! Check the 'output' folder for results.")
    print("📊 Files generated:")
    print("  • monthly_payment_comparison.png - Bar chart comparing monthly payments")
    print("  • total_interest_comparison.png - Bar chart comparing total interest")
    print("  • balance_over_time.png - Line chart showing balance over time")
    print("  • amortization_schedules.png - Principal vs Interest over time")
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        print(f"  • {safe_name}_amortization.csv - {loan.loan_name} detailed data")
    print("  • sample_loans_comparison.csv - Summary comparison data")

if __name__ == "__main__":
    run_analysis_with_sample_data()
