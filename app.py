import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from src.mortgage_calculator import MortgageCalculator, MortgageComparison

# Page configuration
st.set_page_config(
    page_title="🏠 Mortgage Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def load_sample_loans():
    """Load loan configurations from JSON file."""
    try:
        with open("data/sample_loans.json", 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Fallback data if file doesn't exist
        return {
            "home_price": 400000,
            "down_payment": 92000,
            "sample_loans": [
                {"name": "15-Year @ 5.0%", "annual_rate": 0.05, "years": 15},
                {"name": "30-Year @ 6.5%", "annual_rate": 0.065, "years": 30},
                {"name": "20-Year @ 5.5%", "annual_rate": 0.055, "years": 20}
            ]
        }

def create_loan_comparison_chart(comparison_df):
    """Create a comparison chart for loan options."""
    fig = go.Figure()
    
    # Add monthly payment bars
    fig.add_trace(go.Bar(
        name='Monthly Payment',
        x=comparison_df['loan_name'],
        y=comparison_df['monthly_payment'],
        marker_color='#1f77b4',
        text=[f'${x:,.0f}' for x in comparison_df['monthly_payment']],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Monthly Payment Comparison',
        xaxis_title='Loan Type',
        yaxis_title='Monthly Payment ($)',
        showlegend=False,
        height=400
    )
    
    return fig

def create_total_cost_chart(comparison_df, down_payment):
    """Create total cost comparison chart."""
    total_costs = down_payment + comparison_df['total_paid']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Total Cost',
        x=comparison_df['loan_name'],
        y=total_costs,
        marker_color='#ff7f0e',
        text=[f'${x:,.0f}' for x in total_costs],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Total Cost Comparison (Including Down Payment)',
        xaxis_title='Loan Type',
        yaxis_title='Total Cost ($)',
        showlegend=False,
        height=400
    )
    
    return fig

def create_balance_over_time_chart(loans, home_price):
    """Create balance over time chart."""
    fig = go.Figure()
    
    # Add home value line
    years = list(range(0, 31))
    fig.add_trace(go.Scatter(
        x=years,
        y=[home_price] * len(years),
        mode='lines',
        name='Home Value',
        line=dict(color='black', dash='dash', width=2),
        opacity=0.7
    ))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for i, loan in enumerate(loans):
        year_ends = loan.get_year_end_balances()
        year_ends_30yr = year_ends[year_ends['Year'] <= 30]
        
        fig.add_trace(go.Scatter(
            x=year_ends_30yr['Year'],
            y=year_ends_30yr['Remaining_Balance'],
            mode='lines+markers',
            name=loan.loan_name,
            line=dict(color=colors[i], width=2),
            marker=dict(size=4)
        ))
    
    fig.update_layout(
        title='Remaining Balance vs Home Value Over Time',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_principal_interest_pie(loans):
    """Create principal vs interest pie charts."""
    fig = make_subplots(
        rows=1, cols=len(loans),
        specs=[[{'type': 'domain'} for _ in range(len(loans))]],
        subplot_titles=[loan.loan_name for loan in loans]
    )
    
    colors = ['#2ca02c', '#ff7f0e']
    
    for i, loan in enumerate(loans):
        summary = loan.get_loan_summary()
        principal = loan.principal
        interest = summary['total_interest']
        
        fig.add_trace(go.Pie(
            labels=['Principal', 'Interest'],
            values=[principal, interest],
            marker_colors=colors,
            name=loan.loan_name,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}'
        ), row=1, col=i+1)
    
    fig.update_layout(
        title='Principal vs Interest Breakdown',
        height=400,
        showlegend=False
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 Mortgage Calculator</h1>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    st.sidebar.header("🏠 Home Details")
    
    # Load default data
    default_data = load_sample_loans()
    
    # Input fields
    home_price = st.sidebar.number_input(
        "Home Price ($)",
        min_value=100000,
        max_value=10000000,
        value=default_data.get('home_price', 400000),
        step=10000,
        format="%d"
    )
    
    # Down payment input method selection
    st.sidebar.markdown("### 💰 Down Payment")
    down_payment_method = st.sidebar.radio(
        "Choose input method:",
        ["Dollar Amount", "Percentage"],
        horizontal=True
    )
    
    if down_payment_method == "Dollar Amount":
        down_payment = st.sidebar.number_input(
            "Down Payment ($)",
            min_value=0,
            max_value=home_price,
            value=default_data.get('down_payment', 92000),
            step=1000,
            format="%d",
            key="down_payment_dollar"
        )
        down_payment_percent = (down_payment / home_price) * 100 if home_price > 0 else 0
    else:  # Percentage
        # Common down payment percentages
        st.sidebar.markdown("**Quick Select:**")
        col1, col2, col3 = st.sidebar.columns(3)
        
        with col1:
            if st.button("5%", key="btn_5pct"):
                st.session_state.down_payment_percent = 5.0
        with col2:
            if st.button("10%", key="btn_10pct"):
                st.session_state.down_payment_percent = 10.0
        with col3:
            if st.button("20%", key="btn_20pct"):
                st.session_state.down_payment_percent = 20.0
        
        # Manual slider
        down_payment_percent = st.sidebar.slider(
            "Down Payment (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.get('down_payment_percent', 23.0),
            step=0.5,
            format="%.1f%%",
            key="down_payment_percent"
        )
        down_payment = (down_payment_percent / 100) * home_price
    
    # Calculate loan amount
    loan_amount = home_price - down_payment
    
    # Display summary with both values
    st.sidebar.markdown("### 📊 Purchase Summary")
    st.sidebar.metric("Home Price", f"${home_price:,}")
    
    # Show both down payment values
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Down Payment", f"${down_payment:,.0f}")
    with col2:
        st.metric("Down Payment %", f"{down_payment_percent:.1f}%")
    
    st.sidebar.metric("Loan Amount", f"${loan_amount:,}")
    
    # Add helpful information
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Tip**: Switch between dollar amount and percentage to see how they relate!")
    
    # Down payment information
    if down_payment_percent < 20:
        st.sidebar.warning("⚠️ **PMI Required**: Down payment < 20% typically requires Private Mortgage Insurance")
    elif down_payment_percent == 20:
        st.sidebar.success("✅ **No PMI**: 20% down payment avoids PMI requirements")
    else:
        st.sidebar.info("💰 **Great!**: Higher down payment reduces monthly payments and total interest")
    
    # Loan options
    st.sidebar.header("🏦 Loan Options")
    
    # Load loan configurations
    sample_loans = default_data['sample_loans']
    
    # Initialize session state for custom loans if not exists
    if 'custom_loans' not in st.session_state:
        st.session_state.custom_loans = sample_loans.copy()
    
    # Rate modification section
    st.sidebar.markdown("### ⚙️ Customize Rates")
    
    # Toggle between sample and custom rates
    use_custom_rates = st.sidebar.checkbox("Edit mortgage rates", value=False, help="Enable to modify interest rates and terms")
    
    if use_custom_rates:
        st.sidebar.markdown("**Edit existing loans:**")
        
        # Create editable loan options
        updated_loans = []
        for i, loan_data in enumerate(st.session_state.custom_loans):
            with st.sidebar.expander(f"📝 {loan_data['name']}", expanded=False):
                # Loan name
                new_name = st.text_input(
                    "Loan Name", 
                    value=loan_data['name'], 
                    key=f"name_{i}"
                )
                
                # Interest rate
                new_rate = st.number_input(
                    "Interest Rate (%)", 
                    min_value=0.0, 
                    max_value=30.0, 
                    value=loan_data['annual_rate'] * 100, 
                    step=0.1, 
                    format="%.2f",
                    key=f"rate_{i}"
                )
                
                # Loan term
                new_years = st.number_input(
                    "Loan Term (years)", 
                    min_value=1, 
                    max_value=50, 
                    value=loan_data['years'], 
                    step=1,
                    key=f"years_{i}"
                )
                
                # Update loan data
                updated_loan = {
                    'name': new_name,
                    'principal': loan_amount,
                    'annual_rate': new_rate / 100,
                    'years': int(new_years)
                }
                updated_loans.append(updated_loan)
        
        # Add new loan option
        st.sidebar.markdown("**Add new loan:**")
        if st.sidebar.button("➕ Add Loan Option"):
            if len(st.session_state.custom_loans) < 6:  # Limit to 6 loans
                new_loan = {
                    'name': f"Custom Loan {len(st.session_state.custom_loans) + 1}",
                    'principal': loan_amount,
                    'annual_rate': 6.0 / 100,
                    'years': 30
                }
                st.session_state.custom_loans.append(new_loan)
                st.rerun()
            else:
                st.sidebar.warning("Maximum 6 loan options allowed")
        
        # Remove loan option
        if len(st.session_state.custom_loans) > 1:
            st.sidebar.markdown("**Remove loan:**")
            loan_to_remove = st.sidebar.selectbox(
                "Select loan to remove",
                options=[f"{i}: {loan['name']}" for i, loan in enumerate(st.session_state.custom_loans)],
                key="remove_loan"
            )
            if st.sidebar.button("🗑️ Remove Selected Loan"):
                remove_index = int(loan_to_remove.split(':')[0])
                st.session_state.custom_loans.pop(remove_index)
                st.rerun()
        
        # Reset to sample data
        if st.sidebar.button("🔄 Reset to Sample Data"):
            st.session_state.custom_loans = sample_loans.copy()
            st.rerun()
        
        # Use custom loans
        loans_to_use = updated_loans
    else:
        # Use sample loans
        loans_to_use = sample_loans
    
    # Create comparison
    comparison = MortgageComparison()
    loans = []
    
    for loan_data in loans_to_use:
        loan = comparison.add_loan(
            principal=loan_amount,
            annual_rate=loan_data['annual_rate'],
            years=loan_data['years'],
            loan_name=loan_data['name']
        )
        loan.generate_amortization_table()
        loans.append(loan)
    
    # Generate comparison data
    comparison_df = comparison.compare_loans()
    
    # Main content
    # Show custom rates indicator
    if use_custom_rates:
        st.success("🎯 **Custom Rates Active** - You're comparing loans with your custom interest rates and terms!")
    else:
        st.info("📊 **Sample Rates** - Toggle 'Edit mortgage rates' in the sidebar to customize rates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Lowest Monthly Payment", 
                 f"${comparison_df['monthly_payment'].min():,.2f}",
                 f"{comparison_df.loc[comparison_df['monthly_payment'].idxmin(), 'loan_name']}")
    
    with col2:
        st.metric("Lowest Total Interest", 
                 f"${comparison_df['total_interest'].min():,.2f}",
                 f"{comparison_df.loc[comparison_df['total_interest'].idxmin(), 'loan_name']}")
    
    with col3:
        total_costs = down_payment + comparison_df['total_paid']
        min_cost_idx = total_costs.idxmin()
        st.metric("Lowest Total Cost", 
                 f"${total_costs.min():,.2f}",
                 f"{comparison_df.loc[min_cost_idx, 'loan_name']}")
    
    # Current rates display
    if use_custom_rates:
        st.header("⚙️ Current Loan Settings")
        rate_cols = st.columns(len(loans))
        for i, loan in enumerate(loans):
            with rate_cols[i]:
                st.metric(
                    loan.loan_name,
                    f"{loan.annual_rate * 100:.2f}%",
                    f"{loan.years} years"
                )
    
    # Charts section
    st.header("📊 Loan Comparison Charts")
    
    # Monthly payment comparison
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = create_loan_comparison_chart(comparison_df)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = create_total_cost_chart(comparison_df, down_payment)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Balance over time
    st.header("📈 Balance Over Time")
    fig3 = create_balance_over_time_chart(loans, home_price)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Principal vs Interest breakdown
    st.header("🥧 Principal vs Interest Breakdown")
    fig4 = create_principal_interest_pie(loans)
    st.plotly_chart(fig4, use_container_width=True)
    
    # Detailed comparison table
    st.header("📋 Detailed Comparison")
    
    # Add total cost column
    display_df = comparison_df.copy()
    display_df['total_cost'] = down_payment + display_df['total_paid']
    display_df['home_price'] = home_price
    display_df['down_payment'] = down_payment
    display_df['loan_amount'] = loan_amount
    
    # Format currency columns
    for col in ['monthly_payment', 'total_interest', 'total_paid', 'total_cost', 'home_price', 'down_payment', 'loan_amount']:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(display_df, use_container_width=True)
    
    # Equity build-up analysis
    st.header("🏡 Equity Build-up Analysis")
    
    equity_data = []
    for year in range(1, 11):  # First 10 years
        row = {'Year': year, 'Home Value': f"${home_price:,}"}
        for loan in loans:
            if year <= loan.years:
                year_ends = loan.get_year_end_balances()
                if year <= len(year_ends):
                    balance = year_ends[year_ends['Year'] == year]['Remaining_Balance'].iloc[0]
                    equity = home_price - balance
                    row[loan.loan_name] = f"${equity:,.0f}"
                else:
                    row[loan.loan_name] = f"${home_price:,.0f}"
            else:
                row[loan.loan_name] = f"${home_price:,.0f}"
        equity_data.append(row)
    
    equity_df = pd.DataFrame(equity_data)
    st.dataframe(equity_df, use_container_width=True)
    
    # Download data
    st.header("💾 Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Comparison Data"):
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="mortgage_comparison.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Download Amortization Tables"):
            # Create a zip file with all amortization tables
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for loan in loans:
                    safe_name = loan.loan_name.replace(" ", "_").replace("@", "at").replace("%", "pct")
                    csv_data = loan.amortization_table.to_csv(index=False)
                    zip_file.writestr(f"{safe_name}_amortization.csv", csv_data)
            
            zip_buffer.seek(0)
            st.download_button(
                label="Download ZIP",
                data=zip_buffer.getvalue(),
                file_name="amortization_tables.zip",
                mime="application/zip"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Mortgage Calculator v2.0")

if __name__ == "__main__":
    main()
