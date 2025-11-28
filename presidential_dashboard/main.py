import streamlit as st
import pandas as pd
from data_loader import load_data

# Set page config to wide for full screen charts
st.set_page_config(layout="wide", page_title="Presidential Dashboard")

def main():
    # Clean, simple styling
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            margin-bottom: 1.5rem;
        }
        h2 {
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        h3 {
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Presidential Dashboard")

    # Load data
    df = load_data()
    df_clean = df[~df['Fiscal_Year'].astype(str).str.contains('nov', case=False)]

    # First chart: Full width across entire screen
    st.header("Revenue by Year and Revenue Account")
    revenue_per_year_account = df_clean.groupby(['Fiscal_Year', 'Revenue_Account'], as_index=False)['Amount'].sum()
    st.bar_chart(
        revenue_per_year_account.pivot(index="Fiscal_Year", columns="Revenue_Account", values="Amount").fillna(0),
        use_container_width=True,
        height=400
    )

    # Spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Four charts in 2x2 grid
    total_revenue_per_year = df_clean.groupby(['Fiscal_Year'], as_index=False)['Amount'].sum()
    unique_donors_per_year = df_clean.groupby(['Fiscal_Year'], as_index=False)['Contact_ID'].nunique()
    donation_count_per_year = df_clean.groupby(['Fiscal_Year'], as_index=False)['Donation_ID'].count()
    average_donation_per_year = df_clean.groupby(['Fiscal_Year'], as_index=False)['Amount'].mean()

    # First row of 2x2 grid
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Revenue per Year")
        st.bar_chart(total_revenue_per_year.set_index('Fiscal_Year'), use_container_width=True, height=300)
    
    with col2:
        st.subheader("Unique Donors per Year")
        st.bar_chart(unique_donors_per_year.set_index('Fiscal_Year'), use_container_width=True, height=300)

    # Second row of 2x2 grid
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Donation Count per Year")
        st.bar_chart(donation_count_per_year.set_index('Fiscal_Year'), use_container_width=True, height=300)
    
    with col4:
        st.subheader("Average Donation per Year")
        st.bar_chart(average_donation_per_year.set_index('Fiscal_Year'), use_container_width=True, height=300)

if __name__ == "__main__":
    main()
