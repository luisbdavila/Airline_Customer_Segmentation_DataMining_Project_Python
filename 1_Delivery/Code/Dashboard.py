import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

#to run: python -m streamlit run Dashboard.py
# Set page config
'''
st.set_page_config(
    page_title="Airline Customer Analytics Dashboard",
    page_layout="wide",
    initial_sidebar_state="expanded"
)
'''

# Load data
@st.cache_data
def load_data():
    df_customer = pd.read_csv('../../data/DM_AIAI_CustomerDB.csv')
    df_flights = pd.read_csv('../../data/DM_AIAI_FlightsDB.csv')
    df_master = pd.read_csv('../../data/DM_AIAI_MasterCustomerDB.csv')
    return df_customer, df_flights, df_master


df_customer, df_flights, df_master = load_data()

# Sidebar filters
st.sidebar.title('Filters')

# Year filter
years = sorted(df_flights['Year'].unique())
selected_years = st.sidebar.multiselect('Select Years', years, default=years)

# Province/State filter
provinces = sorted(df_master['Province or State'].unique())
selected_provinces = st.sidebar.multiselect('Select Provinces/States', provinces, default=provinces[:5])

# City filter
cities = sorted(df_master[df_master['Province or State'].isin(selected_provinces)]['City'].unique())
selected_cities = st.sidebar.multiselect('Select Cities', cities, default=cities[:5])

# Filter data based on selections
filtered_master = df_master[
    df_master['Province or State'].isin(selected_provinces) &
    df_master['City'].isin(selected_cities)
]

filtered_flights = df_flights[
    df_flights['Year'].isin(selected_years) &
    df_flights['CustomerID'].isin(filtered_master['CustomerID'])
]

# Main dashboard
st.title('Airline Customer Analytics Dashboard')

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        len(filtered_master['CustomerID'].unique()),
        f"{len(filtered_master['CustomerID'].unique()) - len(df_master['CustomerID'].unique())}"
    )

with col2:
    st.metric(
        "Average Customer Lifetime Value",
        f"${filtered_master['Customer Lifetime Value'].mean():,.2f}",
        f"{(filtered_master['Customer Lifetime Value'].mean() / df_master['Customer Lifetime Value'].mean() - 1):.1%}"
    )

with col3:
    st.metric(
        "Total Flights",
        filtered_flights['NumFlights'].sum(),
        f"{filtered_flights['NumFlights'].sum() / df_flights['NumFlights'].sum():.1%}"
    )

with col4:
    st.metric(
        "Average Distance (KM)",
        f"{filtered_flights['DistanceKM'].mean():,.0f}",
        f"{(filtered_flights['DistanceKM'].mean() / df_flights['DistanceKM'].mean() - 1):.1%}"
    )

# Time Series Analysis
st.header('Flight Trends Over Time')
tab1, tab2 = st.tabs(["Monthly Trends", "Yearly Analysis"])

with tab1:
    # Monthly trends
    monthly_flights = filtered_flights.groupby(['Year', 'Month']).agg({
        'NumFlights': 'sum',
        'DistanceKM': 'sum',
        'NumFlightsWithCompanions': 'sum'
    }).reset_index()
    
    monthly_flights['Date'] = pd.to_datetime(monthly_flights[['Year', 'Month']].assign(DAY=1))
    
    fig_monthly = px.line(monthly_flights, x='Date', y=['NumFlights', 'NumFlightsWithCompanions'],
                         title='Monthly Flight Trends')
    st.plotly_chart(fig_monthly, use_container_width=True)

with tab2:
    # Yearly analysis
    yearly_flights = filtered_flights.groupby('Year').agg({
        'NumFlights': 'sum',
        'DistanceKM': 'mean',
        'NumFlightsWithCompanions': 'sum'
    }).reset_index()
    
    fig_yearly = px.bar(yearly_flights, x='Year', y='NumFlights',
                       title='Yearly Flight Distribution')
    st.plotly_chart(fig_yearly, use_container_width=True)

# Customer Segmentation Analysis
st.header('Customer Segmentation')
col1, col2 = st.columns(2)

with col1:
    # Customer Lifetime Value Distribution
    fig_clv = px.histogram(filtered_master, x='Customer Lifetime Value',
                          title='Customer Lifetime Value Distribution')
    st.plotly_chart(fig_clv, use_container_width=True)

with col2:
    # Enrollment Type Distribution
    enrollment_dist = filtered_master['EnrollmentType'].value_counts()
    fig_enrollment = px.pie(values=enrollment_dist.values, names=enrollment_dist.index,
                          title='Enrollment Type Distribution')
    st.plotly_chart(fig_enrollment, use_container_width=True)

# Geographic Analysis
st.header('Geographic Distribution')
geo_data = filtered_master.groupby(['Province or State', 'City']).agg({
    'CustomerID': 'count',
    'Customer Lifetime Value': 'mean'
}).reset_index()

fig_geo = px.treemap(geo_data, 
                     path=['Province or State', 'City'],
                     values='CustomerID',
                     color='Customer Lifetime Value',
                     title='Customer Distribution by Location')
st.plotly_chart(fig_geo, use_container_width=True)

# Customer Behavior Analysis
st.header('Customer Behavior Analysis')
col1, col2 = st.columns(2)

with col1:
    # Flight Distance vs Customer Lifetime Value
    fig_scatter = px.scatter(filtered_master, 
                           x='Total_DistanceKM',
                           y='Customer Lifetime Value',
                           color='EnrollmentType',
                           title='Flight Distance vs Customer Lifetime Value')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Customer Engagement Metrics
    fig_engagement = px.box(filtered_master,
                          y=['Days_with_us', 'Recency_Days'],
                          title='Customer Engagement Metrics')
    st.plotly_chart(fig_engagement, use_container_width=True)

# Correlation Analysis
st.header('Variable Correlations')
numeric_cols = filtered_master.select_dtypes(include=['float64', 'int64']).columns
correlation = filtered_master[numeric_cols].corr()

fig_corr = px.imshow(correlation,
                     title='Correlation Matrix of Numeric Variables')
st.plotly_chart(fig_corr, use_container_width=True)

# Add download capability for filtered data
st.header('Download Filtered Data')
csv = filtered_master.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download filtered data as CSV",
    csv,
    "filtered_data.csv",
    "text/csv",
    key='download-csv'
)
