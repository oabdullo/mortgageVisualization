import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from mortgage_calculator import MortgageCalculator, MortgageComparison

class TestMortgageCalculator(unittest.TestCase):
    
    def setUp(self):
        self.loan = MortgageCalculator(500000, 0.05, 30, "Test Loan")
    
    def test_monthly_payment_calculation(self):
        """Test monthly payment calculation."""
        expected_payment = 2684.11  # Approximate
        actual_payment = self.loan.monthly_payment
        self.assertAlmostEqual(actual_payment, expected_payment, places=1)
    
    def test_amortization_table_generation(self):
        """Test amortization table generation."""
        table = self.loan.generate_amortization_table()
        
        # Check table has correct number of rows
        self.assertEqual(len(table), 360)  # 30 years * 12 months
        
        # Check first payment
        first_payment = table.iloc[0]
        self.assertAlmostEqual(first_payment['Payment'], self.loan.monthly_payment, places=2)
        
        # Check last payment (should have zero balance)
        last_payment = table.iloc[-1]
        self.assertAlmostEqual(last_payment['Remaining_Balance'], 0, places=2)
    
    def test_loan_summary(self):
        """Test loan summary calculation."""
        summary = self.loan.get_loan_summary()
        
        self.assertEqual(summary['principal'], 500000)
        self.assertEqual(summary['annual_rate'], 0.05)
        self.assertEqual(summary['years'], 30)
        self.assertGreater(summary['total_interest'], 0)

class TestMortgageComparison(unittest.TestCase):
    
    def setUp(self):
        self.comparison = MortgageComparison()
        self.comparison.add_loan(500000, 0.05, 15, "15-Year")
        self.comparison.add_loan(500000, 0.065, 30, "30-Year")
    
    def test_loan_comparison(self):
        """Test loan comparison functionality."""
        comparison_df = self.comparison.compare_loans()
        
        self.assertEqual(len(comparison_df), 2)
        self.assertIn('15-Year', comparison_df['loan_name'].values)
        self.assertIn('30-Year', comparison_df['loan_name'].values)

if __name__ == '__main__':
    unittest.main()
