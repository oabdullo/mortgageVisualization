#!/usr/bin/env python3
"""
Demo script showing different home buying scenarios
"""

import json
from src.mortgage_calculator import MortgageCalculator, MortgageComparison

def run_scenario(home_price, down_payment, scenario_name):
    """Run a specific scenario."""
    print(f"\n{'='*60}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*60}")
    
    loan_amount = home_price - down_payment
    down_payment_percent = (down_payment / home_price) * 100
    
    print(f"Home Price: ${home_price:,}")
    print(f"Down Payment: ${down_payment:,} ({down_payment_percent:.1f}%)")
    print(f"Loan Amount: ${loan_amount:,}")
    
    # Load sample loan configurations
    with open("data/sample_loans.json", 'r') as f:
        data = json.load(f)
    sample_loans = data['sample_loans']
    
    # Create comparison
    comparison = MortgageComparison()
    loans = []
    
    for loan_data in sample_loans:
        loan = comparison.add_loan(
            principal=loan_amount,
            annual_rate=loan_data['annual_rate'],
            years=loan_data['years'],
            loan_name=loan_data['name']
        )
        loan.generate_amortization_table()
        loans.append(loan)
    
    # Show comparison
    comparison_df = comparison.compare_loans()
    print(f"\nMonthly Payments:")
    for _, row in comparison_df.iterrows():
        print(f"  {row['loan_name']}: ${row['monthly_payment']:,.2f}")
    
    print(f"\nTotal Interest:")
    for _, row in comparison_df.iterrows():
        print(f"  {row['loan_name']}: ${row['total_interest']:,.2f}")
    
    print(f"\nTotal Cost (including down payment):")
    for _, row in comparison_df.iterrows():
        total_cost = down_payment + row['total_paid']
        print(f"  {row['loan_name']}: ${total_cost:,.2f}")
    
    # Find best options
    monthly_payments = [loan.monthly_payment for loan in loans]
    total_costs = [down_payment + loan.get_loan_summary()['total_paid'] for loan in loans]
    
    min_payment_idx = monthly_payments.index(min(monthly_payments))
    min_cost_idx = total_costs.index(min(total_costs))
    
    print(f"\nBest Options:")
    print(f"  Lowest monthly payment: {loans[min_payment_idx].loan_name} (${monthly_payments[min_payment_idx]:,.2f})")
    print(f"  Lowest total cost: {loans[min_cost_idx].loan_name} (${total_costs[min_cost_idx]:,.2f})")

def main():
    """Run multiple scenarios."""
    print("🏠 Mortgage Calculator - Scenario Comparison")
    print("=" * 60)
    
    scenarios = [
        (300000, 60000, "First-time buyer (20% down)"),
        (500000, 100000, "Move-up buyer (20% down)"),
        (750000, 150000, "Luxury buyer (20% down)"),
        (400000, 40000, "Low down payment (10% down)"),
        (400000, 120000, "High down payment (30% down)"),
    ]
    
    for home_price, down_payment, name in scenarios:
        run_scenario(home_price, down_payment, name)
    
    print(f"\n{'='*60}")
    print("SUMMARY INSIGHTS")
    print(f"{'='*60}")
    print("• Higher down payments reduce loan amount and monthly payments")
    print("• 15-year loans have higher monthly payments but much lower total interest")
    print("• 30-year loans have the lowest monthly payments but highest total interest")
    print("• 20-year loans offer a middle ground between monthly payment and total cost")
    print("• The 'best' choice depends on your monthly budget vs. long-term savings goals")

if __name__ == "__main__":
    main()
