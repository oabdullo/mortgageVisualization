import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class MortgageCalculator:
    """
    A comprehensive mortgage amortization calculator with visualization capabilities.
    """
    
    def __init__(self, principal: float, annual_rate: float, years: int, 
                 loan_name: str = "Mortgage", start_date: datetime = None):
        """
        Initialize the mortgage calculator.
        
        Args:
            principal: Loan amount
            annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            years: Loan term in years
            loan_name: Name for this loan (for comparison purposes)
            start_date: Start date of the loan (defaults to today)
        """
        self.principal = principal
        self.annual_rate = annual_rate
        self.years = years
        self.loan_name = loan_name
        self.start_date = start_date or datetime.now()
        self.monthly_rate = annual_rate / 12
        self.num_payments = years * 12
        self.monthly_payment = self._calculate_monthly_payment()
        self.amortization_table = None
        
    def _calculate_monthly_payment(self) -> float:
        """Calculate monthly payment using the standard mortgage formula."""
        if self.monthly_rate == 0:
            return self.principal / self.num_payments
        
        monthly_payment = (self.principal * 
                          (self.monthly_rate * (1 + self.monthly_rate)**self.num_payments) / 
                          ((1 + self.monthly_rate)**self.num_payments - 1))
        return monthly_payment
    
    def generate_amortization_table(self) -> pd.DataFrame:
        """Generate complete amortization table."""
        table_data = []
        remaining_balance = self.principal
        total_interest_paid = 0
        
        for month in range(1, self.num_payments + 1):
            payment_date = self.start_date + timedelta(days=30 * month)
            interest_payment = remaining_balance * self.monthly_rate
            principal_payment = self.monthly_payment - interest_payment
            remaining_balance -= principal_payment
            total_interest_paid += interest_payment
            
            # Ensure remaining balance doesn't go negative due to rounding
            if remaining_balance < 0.01:
                remaining_balance = 0
                principal_payment += remaining_balance
            
            table_data.append({
                'Month': month,
                'Payment_Date': payment_date,
                'Payment': round(self.monthly_payment, 2),
                'Principal': round(principal_payment, 2),
                'Interest': round(interest_payment, 2),
                'Remaining_Balance': round(remaining_balance, 2),
                'Total_Interest_Paid': round(total_interest_paid, 2),
                'Cumulative_Principal': round(self.principal - remaining_balance, 2)
            })
        
        self.amortization_table = pd.DataFrame(table_data)
        return self.amortization_table
    
    def get_loan_summary(self) -> Dict:
        """Get summary statistics for the loan."""
        if self.amortization_table is None:
            self.generate_amortization_table()
        
        total_paid = self.monthly_payment * self.num_payments
        total_interest = total_paid - self.principal
        
        return {
            'loan_name': self.loan_name,
            'principal': self.principal,
            'annual_rate': self.annual_rate,
            'monthly_rate': self.monthly_rate,
            'years': self.years,
            'monthly_payment': self.monthly_payment,
            'total_payments': self.num_payments,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'interest_percentage': (total_interest / total_paid) * 100
        }
    
    def get_year_end_balances(self) -> pd.DataFrame:
        """Get remaining balance at the end of each year."""
        if self.amortization_table is None:
            self.generate_amortization_table()
        
        year_ends = []
        for year in range(1, self.years + 1):
            month_idx = year * 12 - 1
            if month_idx < len(self.amortization_table):
                row = self.amortization_table.iloc[month_idx]
                year_ends.append({
                    'Year': year,
                    'Remaining_Balance': row['Remaining_Balance'],
                    'Total_Interest_Paid': row['Total_Interest_Paid'],
                    'Cumulative_Principal': row['Cumulative_Principal']
                })
        
        return pd.DataFrame(year_ends)

class MortgageComparison:
    """Compare multiple mortgage options."""
    
    def __init__(self):
        self.loans = []
    
    def add_loan(self, principal: float, annual_rate: float, years: int, 
                 loan_name: str = None, start_date: datetime = None):
        """Add a loan to the comparison."""
        if loan_name is None:
            loan_name = f"{years}-Year @ {annual_rate*100:.1f}%"
        
        loan = MortgageCalculator(principal, annual_rate, years, loan_name, start_date)
        self.loans.append(loan)
        return loan
    
    def compare_loans(self) -> pd.DataFrame:
        """Compare all loans in the comparison."""
        comparison_data = []
        for loan in self.loans:
            summary = loan.get_loan_summary()
            comparison_data.append(summary)
        
        return pd.DataFrame(comparison_data)
    
    def get_combined_amortization(self) -> pd.DataFrame:
        """Get amortization tables for all loans combined."""
        combined_data = []
        for loan in self.loans:
            if loan.amortization_table is None:
                loan.generate_amortization_table()
            
            df = loan.amortization_table.copy()
            df['Loan_Name'] = loan.loan_name
            combined_data.append(df)
        
        return pd.concat(combined_data, ignore_index=True)
