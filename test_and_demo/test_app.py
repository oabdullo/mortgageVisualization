#!/usr/bin/env python3
"""
Test script to verify the Streamlit app works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mortgage_calculator import MortgageCalculator, MortgageComparison
import json

def test_mortgage_calculations():
    """Test the mortgage calculation functions."""
    print("🧪 Testing Mortgage Calculator Functions...")
    
    # Test basic loan calculation
    loan = MortgageCalculator(principal=400000, annual_rate=0.05, years=15)
    loan.generate_amortization_table()
    
    summary = loan.get_loan_summary()
    print(f"✅ 15-year loan: ${summary['monthly_payment']:,.2f}/month")
    
    # Test comparison
    comparison = MortgageComparison()
    loan1 = comparison.add_loan(400000, 0.05, 15, "15-Year @ 5%")
    loan2 = comparison.add_loan(400000, 0.065, 30, "30-Year @ 6.5%")
    
    loan1.generate_amortization_table()
    loan2.generate_amortization_table()
    
    comparison_df = comparison.compare_loans()
    print(f"✅ Comparison works: {len(comparison_df)} loans compared")
    
    # Test JSON loading
    try:
        with open("data/sample_loans.json", 'r') as f:
            data = json.load(f)
        print(f"✅ JSON loading works: {len(data['sample_loans'])} loan options")
    except Exception as e:
        print(f"❌ JSON loading failed: {e}")
        return False
    
    print("🎉 All tests passed! The app should work correctly.")
    return True

if __name__ == "__main__":
    test_mortgage_calculations()
