#!/usr/bin/env python3
"""
Interactive Mortgage Calculator with Home Price and Down Payment Input
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
    return data

def get_user_input():
    """Get home price and down payment from user."""
    print("🏠 Interactive Mortgage Calculator")
    print("=" * 50)
    
    # Get home price
    while True:
        try:
            home_price = float(input("Enter home price: $") or "400000")
            if home_price <= 0:
                print("Please enter a positive home price.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Get down payment
    while True:
        try:
            down_payment = float(input("Enter down payment: $") or "92000")
            if down_payment < 0:
                print("Down payment cannot be negative.")
                continue
            if down_payment >= home_price:
                print("Down payment must be less than home price.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Calculate loan amount
    loan_amount = home_price - down_payment
    down_payment_percent = (down_payment / home_price) * 100
    
    print(f"\n📊 Purchase Summary:")
    print(f"   Home Price: ${home_price:,.2f}")
    print(f"   Down Payment: ${down_payment:,.2f} ({down_payment_percent:.1f}%)")
    print(f"   Loan Amount: ${loan_amount:,.2f}")
    
    return home_price, down_payment, loan_amount

def create_enhanced_visualizations(loans, comparison, home_price, down_payment):
    """Create enhanced visualizations with home price context."""
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # 1. Monthly Payment Comparison
    plt.figure(figsize=(12, 8))
    loan_names = [loan.loan_name for loan in loans]
    monthly_payments = [loan.monthly_payment for loan in loans]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    bars = plt.bar(loan_names, monthly_payments, color=colors)
    plt.title(f'Monthly Payment Comparison\nHome: ${home_price:,.0f} | Down: ${down_payment:,.0f}', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Loan Type', fontsize=12)
    plt.ylabel('Monthly Payment ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for i, v in enumerate(monthly_payments):
        plt.text(i, v + 20, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/monthly_payment_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Total Cost Comparison (including down payment)
    plt.figure(figsize=(12, 8))
    total_costs = [down_payment + loan.get_loan_summary()['total_paid'] for loan in loans]
    
    bars = plt.bar(loan_names, total_costs, color=colors)
    plt.title(f'Total Cost Comparison (Including Down Payment)\nHome: ${home_price:,.0f} | Down: ${down_payment:,.0f}', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Loan Type', fontsize=12)
    plt.ylabel('Total Cost ($)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for i, v in enumerate(total_costs):
        plt.text(i, v + 5000, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/total_cost_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Interest vs Principal Breakdown
    fig, axes = plt.subplots(1, len(loans), figsize=(15, 6))
    if len(loans) == 1:
        axes = [axes]
    
    for i, loan in enumerate(loans):
        summary = loan.get_loan_summary()
        principal = loan.principal
        interest = summary['total_interest']
        
        # Create pie chart
        sizes = [principal, interest]
        labels = ['Principal', 'Interest']
        colors_pie = ['#2ca02c', '#ff7f0e']
        
        axes[i].pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
        axes[i].set_title(f'{loan.loan_name}\nPrincipal: ${principal:,.0f}\nInterest: ${interest:,.0f}', 
                         fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('output/principal_interest_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Balance Over Time with Home Value
    plt.figure(figsize=(14, 8))
    colors_line = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # Add home value line
    years = list(range(0, 31))
    home_values = [home_price] * len(years)
    plt.plot(years, home_values, 'k--', linewidth=2, label=f'Home Value (${home_price:,.0f})', alpha=0.7)
    
    for i, loan in enumerate(loans):
        year_ends = loan.get_year_end_balances()
        # Show up to 30 years
        year_ends_30yr = year_ends[year_ends['Year'] <= 30]
        plt.plot(year_ends_30yr['Year'], year_ends_30yr['Remaining_Balance'], 
                marker='o', linewidth=2, label=loan.loan_name, color=colors_line[i])
    
    plt.title(f'Remaining Balance vs Home Value Over Time\nHome: ${home_price:,.0f} | Down: ${down_payment:,.0f}', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Amount ($)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/balance_vs_home_value.png', dpi=300, bbox_inches='tight')
    plt.close()

def run_interactive_analysis():
    """Run interactive mortgage analysis."""
    # Get user input
    home_price, down_payment, loan_amount = get_user_input()
    
    # Load sample loan configurations
    print("\nLoading loan options...")
    data = load_sample_loans()
    sample_loans = data['sample_loans']
    
    # Create comparison
    comparison = MortgageComparison()
    
    # Add each loan from the sample data with calculated principal
    loans = []
    for loan_data in sample_loans:
        loan = comparison.add_loan(
            principal=loan_amount,  # Use calculated loan amount
            annual_rate=loan_data['annual_rate'],
            years=loan_data['years'],
            loan_name=loan_data['name']
        )
        loans.append(loan)
        print(f"Added: {loan_data['name']} - ${loan_amount:,.0f} @ {loan_data['annual_rate']*100:.1f}% for {loan_data['years']} years")
    
    # Generate amortization tables
    print("\nGenerating amortization tables...")
    for loan in loans:
        loan.generate_amortization_table()
    
    # Display comparison
    print("\n" + "="*90)
    print("LOAN COMPARISON SUMMARY")
    print("="*90)
    
    comparison_df = comparison.compare_loans()
    print(comparison_df[['loan_name', 'monthly_payment', 'total_interest', 'total_paid']].to_string(index=False))
    
    # Show enhanced insights
    print(f"\nKey Insights:")
    for i, loan in enumerate(loans):
        summary = loan.get_loan_summary()
        total_cost = down_payment + summary['total_paid']
        print(f"• {loan.loan_name}: ${summary['monthly_payment']:,.2f}/month, ${summary['total_interest']:,.2f} interest, ${total_cost:,.2f} total cost")
    
    # Find best options
    monthly_payments = [loan.monthly_payment for loan in loans]
    total_interests = [loan.get_loan_summary()['total_interest'] for loan in loans]
    total_costs = [down_payment + loan.get_loan_summary()['total_paid'] for loan in loans]
    
    min_payment_idx = monthly_payments.index(min(monthly_payments))
    min_interest_idx = total_interests.index(min(total_interests))
    min_cost_idx = total_costs.index(min(total_costs))
    
    print(f"\n• Lowest monthly payment: {loans[min_payment_idx].loan_name} (${monthly_payments[min_payment_idx]:,.2f})")
    print(f"• Lowest total interest: {loans[min_interest_idx].loan_name} (${total_interests[min_interest_idx]:,.2f})")
    print(f"• Lowest total cost: {loans[min_cost_idx].loan_name} (${total_costs[min_cost_idx]:,.2f})")
    
    # Show equity build-up over time
    print(f"\nEquity Build-up Analysis (First 5 Years):")
    print("Year | Home Value | Remaining Balance | Equity")
    print("-" * 50)
    for year in range(1, 6):
        print(f"{year:4d} | ${home_price:>10,.0f} | ", end="")
        for i, loan in enumerate(loans):
            if year <= loan.years:
                year_ends = loan.get_year_end_balances()
                if year <= len(year_ends):
                    balance = year_ends[year_ends['Year'] == year]['Remaining_Balance'].iloc[0]
                    equity = home_price - balance
                    if i == 0:
                        print(f"${balance:>15,.0f} | ${equity:>6,.0f}")
                    else:
                        print(f"      | ${balance:>15,.0f} | ${equity:>6,.0f}")
                else:
                    if i == 0:
                        print(f"${'Paid Off':>15} | ${home_price:>6,.0f}")
                    else:
                        print(f"      | ${'Paid Off':>15} | ${home_price:>6,.0f}")
            else:
                if i == 0:
                    print(f"${'Paid Off':>15} | ${home_price:>6,.0f}")
                else:
                    print(f"      | ${'Paid Off':>15} | ${home_price:>6,.0f}")
    
    # Create visualizations
    print("\nCreating enhanced visualizations...")
    create_enhanced_visualizations(loans, comparison, home_price, down_payment)
    
    # Save data
    print("\nSaving data...")
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        loan.amortization_table.to_csv(f"output/{safe_name}_amortization.csv", index=False)
    
    # Create enhanced comparison CSV
    enhanced_df = comparison_df.copy()
    enhanced_df['home_price'] = home_price
    enhanced_df['down_payment'] = down_payment
    enhanced_df['loan_amount'] = loan_amount
    enhanced_df['total_cost'] = down_payment + enhanced_df['total_paid']
    enhanced_df.to_csv("output/enhanced_loan_comparison.csv", index=False)
    
    print("\n✅ Interactive analysis complete! Check the 'output' folder for results.")
    print("📊 Files generated:")
    print("  • monthly_payment_comparison.png - Monthly payment comparison")
    print("  • total_cost_comparison.png - Total cost including down payment")
    print("  • principal_interest_breakdown.png - Principal vs interest breakdown")
    print("  • balance_vs_home_value.png - Balance vs home value over time")
    for loan in loans:
        safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
        print(f"  • {safe_name}_amortization.csv - {loan.loan_name} detailed data")
    print("  • enhanced_loan_comparison.csv - Complete comparison with home price data")

if __name__ == "__main__":
    run_interactive_analysis()
