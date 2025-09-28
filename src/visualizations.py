import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class MortgageVisualizer:
    """Create visualizations for mortgage amortization data."""
    
    def __init__(self, style: str = "seaborn-v0_8"):
        """Initialize with matplotlib style."""
        plt.style.use(style)
        sns.set_palette("husl")
    
    def plot_amortization_schedule(self, loan, save_path: Optional[str] = None):
        """Plot principal vs interest payments over time."""
        if loan.amortization_table is None:
            loan.generate_amortization_table()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Principal vs Interest over time
        months = loan.amortization_table['Month']
        principal = loan.amortization_table['Principal']
        interest = loan.amortization_table['Interest']
        
        ax1.plot(months, principal, label='Principal', linewidth=2)
        ax1.plot(months, interest, label='Interest', linewidth=2)
        ax1.set_title(f'{loan.loan_name} - Principal vs Interest Payments Over Time')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Payment Amount ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Remaining balance over time
        balance = loan.amortization_table['Remaining_Balance']
        ax2.plot(months, balance, color='red', linewidth=2)
        ax2.set_title(f'{loan.loan_name} - Remaining Balance Over Time')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Remaining Balance ($)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_loan_comparison(self, comparison, save_path: Optional[str] = None):
        """Compare multiple loans side by side."""
        comparison_df = comparison.compare_loans()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Monthly payments comparison
        ax1.bar(comparison_df['loan_name'], comparison_df['monthly_payment'])
        ax1.set_title('Monthly Payment Comparison')
        ax1.set_ylabel('Monthly Payment ($)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Total interest comparison
        ax2.bar(comparison_df['loan_name'], comparison_df['total_interest'])
        ax2.set_title('Total Interest Paid Comparison')
        ax2.set_ylabel('Total Interest ($)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Interest percentage comparison
        ax3.bar(comparison_df['loan_name'], comparison_df['interest_percentage'])
        ax3.set_title('Interest as % of Total Payments')
        ax3.set_ylabel('Interest Percentage (%)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Total paid comparison
        ax4.bar(comparison_df['loan_name'], comparison_df['total_paid'])
        ax4.set_title('Total Amount Paid Comparison')
        ax4.set_ylabel('Total Paid ($)')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_balance_comparison(self, comparison, save_path: Optional[str] = None):
        """Plot remaining balance over time for multiple loans."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for loan in comparison.loans:
            if loan.amortization_table is None:
                loan.generate_amortization_table()
            
            months = loan.amortization_table['Month']
            balance = loan.amortization_table['Remaining_Balance']
            ax.plot(months, balance, label=loan.loan_name, linewidth=2)
        
        ax.set_title('Remaining Balance Comparison Over Time')
        ax.set_xlabel('Month')
        ax.set_ylabel('Remaining Balance ($)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_interactive_dashboard(self, comparison, save_path: Optional[str] = None):
        """Create an interactive Plotly dashboard."""
        combined_df = comparison.get_combined_amortization()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Remaining Balance Over Time', 
                          'Principal vs Interest Payments',
                          'Cumulative Interest Paid',
                          'Monthly Payment Breakdown'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": True}]]
        )
        
        # Plot 1: Remaining balance over time
        for loan_name in combined_df['Loan_Name'].unique():
            loan_data = combined_df[combined_df['Loan_Name'] == loan_name]
            fig.add_trace(
                go.Scatter(x=loan_data['Month'], y=loan_data['Remaining_Balance'],
                          mode='lines', name=f'{loan_name} Balance'),
                row=1, col=1
            )
        
        # Plot 2: Principal vs Interest
        for loan_name in combined_df['Loan_Name'].unique():
            loan_data = combined_df[combined_df['Loan_Name'] == loan_name]
            fig.add_trace(
                go.Scatter(x=loan_data['Month'], y=loan_data['Principal'],
                          mode='lines', name=f'{loan_name} Principal'),
                row=1, col=2
            )
            fig.add_trace(
                go.Scatter(x=loan_data['Month'], y=loan_data['Interest'],
                          mode='lines', name=f'{loan_name} Interest'),
                row=1, col=2
            )
        
        # Plot 3: Cumulative interest
        for loan_name in combined_df['Loan_Name'].unique():
            loan_data = combined_df[combined_df['Loan_Name'] == loan_name]
            fig.add_trace(
                go.Scatter(x=loan_data['Month'], y=loan_data['Total_Interest_Paid'],
                          mode='lines', name=f'{loan_name} Cumulative Interest'),
                row=2, col=1
            )
        
        # Plot 4: Monthly payment breakdown (pie chart)
        comparison_df = comparison.compare_loans()
        fig.add_trace(
            go.Pie(labels=comparison_df['loan_name'], 
                  values=comparison_df['monthly_payment'],
                  name="Monthly Payments"),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Mortgage Amortization Dashboard",
            showlegend=True,
            height=800
        )
        
        if save_path:
            fig.write_html(save_path)
        
        fig.show()
