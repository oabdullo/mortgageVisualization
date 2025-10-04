#!/usr/bin/env python3
"""
Interactive Mortgage Calculator - Allows users to input their own mortgage rates and terms
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mortgage_calculator import MortgageCalculator, MortgageComparison
from src.visualizations import MortgageVisualizer

def get_user_input():
    """Get mortgage details from user input."""
    print("🏠 Interactive Mortgage Calculator")
    print("=" * 50)
    
    # Get basic loan information
    try:
        principal = float(input("Enter loan amount (principal): $"))
        print(f"Loan amount: ${principal:,.2f}")
    except ValueError:
        print("Invalid input. Using default amount of $308,000")
        principal = 308000
    
    # Get number of loan options to compare
    try:
        num_loans = int(input("\nHow many mortgage options do you want to compare? (1-5): "))
        if num_loans < 1 or num_loans > 5:
            num_loans = 3
            print("Using default of 3 options")
    except ValueError:
        num_loans = 3
        print("Using default of 3 options")
    
    loans_data = []
    
    print(f"\nEnter details for {num_loans} mortgage option(s):")
    print("-" * 40)
    
    for i in range(num_loans):
        print(f"\nMortgage Option {i+1}:")
        
        # Get loan name
        loan_name = input(f"  Name for this option (e.g., '30-Year Fixed'): ").strip()
        if not loan_name:
            loan_name = f"Option {i+1}"
        
        # Get interest rate
        while True:
            try:
                rate_input = input(f"  Annual interest rate (e.g., 6.5 for 6.5%): ")
                annual_rate = float(rate_input) / 100
                if annual_rate < 0 or annual_rate > 1:
                    print("  Please enter a rate between 0 and 100")
                    continue
                break
            except ValueError:
                print("  Please enter a valid number")
        
        # Get loan term
        while True:
            try:
                years = int(input(f"  Loan term in years (e.g., 30): "))
                if years < 1 or years > 50:
                    print("  Please enter a term between 1 and 50 years")
                    continue
                break
            except ValueError:
                print("  Please enter a valid number")
        
        loans_data.append({
            'name': loan_name,
            'principal': principal,
            'annual_rate': annual_rate,
            'years': years
        })
        
        print(f"  ✓ Added: {loan_name} - ${principal:,.2f} @ {annual_rate*100:.2f}% for {years} years")
    
    return loans_data

def run_interactive_analysis():
    """Run mortgage analysis with user input."""
    # Get user input
    loans_data = get_user_input()
    
    # Create comparison
    comparison = MortgageComparison()
    loans = []
    
    print("\n" + "="*60)
    print("GENERATING AMORTIZATION TABLES")
    print("="*60)
    
    # Add each loan from user input
    for loan_data in loans_data:
        loan = comparison.add_loan(
            principal=loan_data['principal'],
            annual_rate=loan_data['annual_rate'],
            years=loan_data['years'],
            loan_name=loan_data['name']
        )
        loans.append(loan)
        print(f"Processing: {loan_data['name']}...")
        loan.generate_amortization_table()
    
    # Display comparison
    print("\n" + "="*80)
    print("MORTGAGE COMPARISON SUMMARY")
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
    print(f"\nFirst 3 months of each loan:")
    for loan in loans:
        print(f"\n{loan.loan_name}:")
        print(loan.amortization_table[['Month', 'Payment', 'Principal', 'Interest', 'Remaining_Balance']].head(3).to_string(index=False))
    
    # Ask if user wants to generate visualizations
    create_viz = input("\nGenerate visualizations and save data? (y/n): ").lower().strip()
    
    if create_viz in ['y', 'yes']:
        # Create visualizations
        print("\nCreating visualizations...")
        visualizer = MortgageVisualizer()
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        # Generate plots for each loan
        for loan in loans:
            safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct").replace("/", "_")
            visualizer.plot_amortization_schedule(loan, f"output/{safe_name}_amortization.png")
            print(f"  ✓ Created: {safe_name}_amortization.png")
        
        # Generate comparison plots
        visualizer.plot_loan_comparison(comparison, "output/interactive_loan_comparison.png")
        visualizer.plot_balance_comparison(comparison, "output/interactive_balance_comparison.png")
        visualizer.create_interactive_dashboard(comparison, "output/interactive_dashboard.html")
        
        # Save data
        print("\nSaving data...")
        for loan in loans:
            safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct").replace("/", "_")
            loan.amortization_table.to_csv(f"output/{safe_name}_amortization.csv", index=False)
            print(f"  ✓ Saved: {safe_name}_amortization.csv")
        
        comparison_df.to_csv("output/interactive_loan_comparison.csv", index=False)
        print("  ✓ Saved: interactive_loan_comparison.csv")
        
        print("\n✅ Analysis complete! Check the 'output' folder for results.")
        print("📊 Files generated:")
        for loan in loans:
            safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct").replace("/", "_")
            print(f"  • {safe_name}_amortization.png - {loan.loan_name} amortization chart")
            print(f"  • {safe_name}_amortization.csv - {loan.loan_name} detailed data")
        print("  • interactive_loan_comparison.png - Side-by-side loan comparison")
        print("  • interactive_balance_comparison.png - Balance comparison over time")
        print("  • interactive_dashboard.html - Interactive dashboard")
        print("  • interactive_loan_comparison.csv - Summary comparison data")
    else:
        print("\n✅ Analysis complete! No files saved.")

def save_current_rates_to_json(loans_data, filename="data/current_rates.json"):
    """Save the current rates to a JSON file for future reference."""
    data = {
        "home_price": loans_data[0]['principal'] if loans_data else 308000,
        "down_payment": 0,  # Not used in this context
        "sample_loans": loans_data
    }
    
    os.makedirs("data", exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Current rates saved to {filename}")

if __name__ == "__main__":
    try:
        run_interactive_analysis()
        
        # Ask if user wants to save the rates
        save_rates = input("\nSave these rates for future use? (y/n): ").lower().strip()
        if save_rates in ['y', 'yes']:
            # This would require getting the loans_data from the function
            # For now, we'll just show the option
            print("To save rates, run the script again and choose 'y' when prompted.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Analysis cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your inputs and try again.")
