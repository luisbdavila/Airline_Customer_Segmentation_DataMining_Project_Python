# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import os

st.set_page_config(
    page_title="Airline Customer Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    # Safe way to reference the file relative to the app
    df_customer = pd.read_csv(os.path.join("data", "DM_AIAI_CustomerDB.csv"))
    df_flights = pd.read_csv(os.path.join("data", 'DM_AIAI_FlightsDB.csv'))
    df_master = pd.read_csv(os.path.join("data", 'DM_AIAI_MasterCustomerDB.csv'))
    return df_customer, df_flights, df_master

df_customer, df_flights, df_master = load_data()

# --- Sidebar filters with "Select All" buttons ---
st.sidebar.title('Filters')

# Initialize session state for filters
filter_keys = [
    'selected_years', 'selected_provinces', 'selected_cities',
    'selected_enrollment', 'selected_marital', 'selected_loyalty', 'selected_education'
]

for key in filter_keys:
    if key not in st.session_state:
        st.session_state[key] = []

# --- Year filter ---
if 'Year' in df_flights.columns:
    years = sorted(df_flights['Year'].dropna().unique())
else:
    years = []
if st.sidebar.button("Select All Years"):
    st.session_state.selected_years = years

selected_years = st.sidebar.multiselect(
    "Select Years", years, default=st.session_state.selected_years or years
)
st.session_state.selected_years = selected_years

# --- Province/State filter ---
province_col = 'Province or State'
if province_col in df_master.columns:
    provinces = sorted(df_master[province_col].dropna().unique())
else:
    provinces = []
if st.sidebar.button("Select All Provinces/States"):
    st.session_state.selected_provinces = provinces

selected_provinces = st.sidebar.multiselect(
    "Select Provinces/States", provinces, default=st.session_state.selected_provinces or provinces[:5]
)
st.session_state.selected_provinces = selected_provinces

# --- City filter ---
city_col = 'City'
if city_col in df_master.columns:
    cities = sorted(
        df_master[df_master[province_col].isin(selected_provinces)][city_col].dropna().unique()
    ) if selected_provinces else sorted(df_master[city_col].dropna().unique())
else:
    cities = []

# Clean up previously selected cities that no longer belong to the selected provinces
if 'selected_cities' in st.session_state:
    st.session_state.selected_cities = [
        city for city in st.session_state.selected_cities if city in cities
    ]

if st.sidebar.button("Select All Cities"):
    st.session_state.selected_cities = cities

selected_cities = st.sidebar.multiselect(
    "Select Cities", cities, default=st.session_state.selected_cities or cities[:5]
)
st.session_state.selected_cities = selected_cities

# --- Enrollment Type filter ---
enroll_col = 'EnrollmentType'
if enroll_col in df_master.columns:
    enrollment_types = sorted(df_master[enroll_col].dropna().unique())
else:
    enrollment_types = []
if st.sidebar.button("Select All Enrollment Types"):
    st.session_state.selected_enrollment = enrollment_types

selected_enrollment = st.sidebar.multiselect(
    "Select Enrollment Types", enrollment_types, default=st.session_state.selected_enrollment or enrollment_types
)
st.session_state.selected_enrollment = selected_enrollment

# --- Marital Status filter ---
marital_col = 'Marital Status'
if marital_col in df_master.columns:
    marital_statuses = sorted(df_master[marital_col].dropna().unique())
else:
    marital_statuses = []
if st.sidebar.button("Select All Marital Statuses"):
    st.session_state.selected_marital = marital_statuses

selected_marital = st.sidebar.multiselect(
    "Select Marital Status", marital_statuses, default=st.session_state.selected_marital or marital_statuses
)
st.session_state.selected_marital = selected_marital

# --- Loyalty Status filter ---
loyalty_col = 'LoyaltyStatus'
if loyalty_col in df_master.columns:
    loyalty_statuses = sorted(df_master[loyalty_col].dropna().unique())
else:
    loyalty_statuses = []
if st.sidebar.button("Select All Loyalty Statuses"):
    st.session_state.selected_loyalty = loyalty_statuses

selected_loyalty = st.sidebar.multiselect(
    "Select Loyalty Status", loyalty_statuses, default=st.session_state.selected_loyalty or loyalty_statuses
)
st.session_state.selected_loyalty = selected_loyalty

# --- Education filter ---
edu_col = 'Education'
if edu_col in df_master.columns:
    education_levels = sorted(df_master[edu_col].dropna().unique())
else:
    education_levels = []
if st.sidebar.button("Select All Education Levels"):
    st.session_state.selected_education = education_levels

selected_education = st.sidebar.multiselect(
    "Select Education Levels", education_levels, default=st.session_state.selected_education or education_levels
)
st.session_state.selected_education = selected_education

# --- Apply all filters to the master dataframe ---
# Guard against missing columns by checking existence; if missing, create an 'all pass' mask
mask = pd.Series(True, index=df_master.index)

if province_col in df_master.columns and selected_provinces:
    mask &= df_master[province_col].isin(selected_provinces)
if city_col in df_master.columns and selected_cities:
    mask &= df_master[city_col].isin(selected_cities)
if enroll_col in df_master.columns and selected_enrollment:
    mask &= df_master[enroll_col].isin(selected_enrollment)
if marital_col in df_master.columns and selected_marital:
    mask &= df_master[marital_col].isin(selected_marital)
if loyalty_col in df_master.columns and selected_loyalty:
    mask &= df_master[loyalty_col].isin(selected_loyalty)
if edu_col in df_master.columns and selected_education:
    mask &= df_master[edu_col].isin(selected_education)

filtered_master = df_master[mask].copy()

# Filter flights
if 'Year' in df_flights.columns and selected_years:
    flights_year_mask = df_flights['Year'].isin(selected_years)
else:
    flights_year_mask = pd.Series(True, index=df_flights.index)

if 'Loyalty#' in df_flights.columns and 'Loyalty#' in filtered_master.columns:
    flights_loyalty_mask = df_flights['Loyalty#'].isin(filtered_master['Loyalty#'])
else:
    flights_loyalty_mask = pd.Series(True, index=df_flights.index)

filtered_flights = df_flights[flights_year_mask & flights_loyalty_mask].copy()

# Dashboard Title
st.title('Airline Customer Analytics Dashboard')

# Metric Cards - MEDIAN
col1, col2, col3, col4 = st.columns(4)

# --- Helper Function ---
def get_safe_median_int(series):
    """Return median as int; 0 if NaN or series empty."""
    if (series is None) or series.empty:
        return 0
    median_val = series.median()
    if pd.isna(median_val):
        return 0
    return int(median_val)

# --- Metrics ---
# Use column names that likely exist in df_master
col1.metric("Median Flights per Customer", get_safe_median_int(filtered_master.get('Total_NumFlights', pd.Series(dtype=float))))
col2.metric("Median Distance (KM) per Customer", get_safe_median_int(filtered_master.get('Total_DistanceKM', pd.Series(dtype=float))))

try:
    median_pct_companions = filtered_master.get('Perc_Flights_With_Companions', pd.Series(dtype=float)).median()
    if pd.isna(median_pct_companions):
        median_pct_companions = 0.0
except Exception:
    median_pct_companions = 0.0
col3.metric("Flights with Companions (%)", f"{median_pct_companions:.1f}%")

col4.metric(
    "Redeemable $ by Customer",
    get_safe_median_int(filtered_master.get('Dollar_Cost_Points_Remaining', pd.Series(dtype=float)))
)

# --- Time Series Trends (Interactive Streamlit Chart) ---
st.header("Flight Metrics Over Time")

if {'Year', 'Month'}.issubset(filtered_flights.columns):
    filtered_flights['YearMonthDate'] = pd.to_datetime(
        filtered_flights[['Year', 'Month']].assign(DAY=1)
    )

    monthly_flights = filtered_flights.groupby('YearMonthDate').agg({
        'NumFlights': 'sum' if 'NumFlights' in filtered_flights.columns else 'count',
        'NumFlightsWithCompanions': 'sum' if 'NumFlightsWithCompanions' in filtered_flights.columns else 'sum',
        'DistanceKM': 'sum' if 'DistanceKM' in filtered_flights.columns else 'sum',
        'DollarCostPointsRedeemed': 'sum' if 'DollarCostPointsRedeemed' in filtered_flights.columns else 'sum'
    }).reset_index()

    if 'DistanceKM' in monthly_flights.columns:
        monthly_flights['DistanceKM'] = monthly_flights['DistanceKM'] / 1000  # convert to thousands of km

    monthly_melted = monthly_flights.melt(
        id_vars='YearMonthDate',
        value_vars=[c for c in ['NumFlights', 'NumFlightsWithCompanions', 'DistanceKM', 'DollarCostPointsRedeemed'] if c in monthly_flights.columns],
        var_name='Metric',
        value_name='Value'
    )

    metric_labels = {
        'NumFlights': 'Flights',
        'NumFlightsWithCompanions': 'Flights w/ Companions',
        'DistanceKM': 'Distance (Thousands of KM)',
        'DollarCostPointsRedeemed': 'Dollar Cost (Points Redeemed)'
    }

    fig = px.line(
        monthly_melted,
        x='YearMonthDate',
        y='Value',
        color='Metric',
        markers=True,
        title='Flight Metrics Over Time'
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Metric',
        hovermode='x unified',
        template='plotly_white'
    )
    # nicer legend names
    for t in fig.data:
        if t.name in metric_labels:
            t.name = metric_labels[t.name]

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Not enough flight time-series columns (Year, Month) to build time series chart.")

# --- Categorical charts (Marital Status, Enrollment Type, Education, LoyaltyStatus, Gender, Location Code) ---
st.header("Categorical Overview")

# Define chart type per variable
categorical_cols = [
    ('Marital Status', 'Marital Status', 'pie'),
    ('EnrollmentType', 'Enrollment Type', 'pie'),
    ('Education', 'Education', 'bar'),
    ('LoyaltyStatus', 'Loyalty Status', 'pie'),
    ('Gender', 'Gender', 'pie'),
    ('Location Code', 'Location Code', 'bar')
]

cols = st.columns(3)
i = 0
for display_col, title, chart_type in categorical_cols:
    target_col = display_col
    if target_col not in filtered_master.columns:
        # try common variations
        if display_col == 'EnrollmentType' and 'Enrollment Type' in filtered_master.columns:
            target_col = 'Enrollment Type'
        elif display_col == 'LoyaltyStatus' and 'Loyalty Status' in filtered_master.columns:
            target_col = 'Loyalty Status'
        else:
            target_col = None

    if target_col and target_col in filtered_master.columns:
        counts = filtered_master[target_col].fillna('Unknown').value_counts().reset_index()
        counts.columns = [target_col, 'count']

        if chart_type == 'pie':
            fig_cat = px.pie(
                counts,
                names=target_col,
                values='count',
                title=title,
                hole=0.3  # makes it a donut-style pie
            )
            fig_cat.update_traces(textinfo='percent+label', textfont_size=12)
            fig_cat.update_layout(template='plotly_white')
        else:
            fig_cat = px.bar(counts, x=target_col, y='count', title=title, text='count')
            fig_cat.update_layout(xaxis_title=None, yaxis_title='Count', template='plotly_white')
            fig_cat.update_traces(textposition='outside', marker_line_width=1, marker_line_color='black')

        cols[i % 3].plotly_chart(fig_cat, use_container_width=True)
    else:
        cols[i % 3].info(f"Column '{display_col}' not found.")
    i += 1

# --- Histograms in requested order ---
st.header("Customer Value and Enrollment")

# Normalize column names for enrollment date - map EnrollmentDateOpening -> EnrollmentDate if needed
if 'EnrollmentDateOpening' in filtered_master.columns and 'EnrollmentDate' not in filtered_master.columns:
    filtered_master['EnrollmentDate'] = filtered_master['EnrollmentDateOpening']

# Convert date columns to datetime safely
if 'EnrollmentDate' in filtered_master.columns:
    filtered_master['EnrollmentDate'] = pd.to_datetime(filtered_master['EnrollmentDate'], errors='coerce')
if 'CancellationDate' in filtered_master.columns:
    filtered_master['CancellationDate'] = pd.to_datetime(filtered_master['CancellationDate'], errors='coerce')

# Layout: two columns, left: Enrollment & Cancellation (dates); right: CLV & Income
left_col, right_col = st.columns(2)

# Common histogram update options (make bar borders visible)
hist_update_kwargs = dict(marker_line_width=1, marker_line_color='black', opacity=0.85)

# 1) Enrollment date
with left_col:
    if 'EnrollmentDate' in filtered_master.columns and filtered_master['EnrollmentDate'].notna().any():
        fig_enroll_date = px.histogram(
            filtered_master.dropna(subset=['EnrollmentDate']), x='EnrollmentDate',
            nbins=50, title='Enrollment Date Distribution'
        )
        fig_enroll_date.update_traces(**hist_update_kwargs)
        fig_enroll_date.update_layout(template='plotly_white', xaxis_title='Enrollment Date', yaxis_title='Count')
        st.plotly_chart(fig_enroll_date, use_container_width=True)
    else:
        st.info("No Enrollment Date data available for histogram.")

    # 2) Cancellation date
    if 'CancellationDate' in filtered_master.columns and filtered_master['CancellationDate'].notna().any():
        fig_cancel_date = px.histogram(
            filtered_master.dropna(subset=['CancellationDate']), x='CancellationDate',
            nbins=50, title='Cancellation Date Distribution'
        )
        fig_cancel_date.update_traces(**hist_update_kwargs)
        fig_cancel_date.update_layout(template='plotly_white', xaxis_title='Cancellation Date', yaxis_title='Count')
        st.plotly_chart(fig_cancel_date, use_container_width=True)
    else:
        st.info("No Cancellation Date data available for histogram.")

# 3) Customer Lifetime Value
with right_col:
    if 'Customer Lifetime Value' in filtered_master.columns:
        fig_clv = px.histogram(filtered_master, x='Customer Lifetime Value', nbins=50,
                               title='Customer Lifetime Value Distribution')
        fig_clv.update_traces(**hist_update_kwargs)
        fig_clv.update_layout(template='plotly_white', xaxis_title='Customer Lifetime Value', yaxis_title='Count')
        st.plotly_chart(fig_clv, use_container_width=True)
    else:
        st.info("No 'Customer Lifetime Value' column found.")

    # 4) Income
    if 'Income' in filtered_master.columns:
        fig_income = px.histogram(filtered_master, x='Income', nbins=50, title='Income Distribution')
        fig_income.update_traces(**hist_update_kwargs)
        fig_income.update_layout(template='plotly_white', xaxis_title='Income', yaxis_title='Count')
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.info("No 'Income' column found.")

# --- Geographic Map ---
st.header("Customer Distribution by City")
if {'Latitude', 'Longitude'}.issubset(filtered_master.columns):
    city_counts = (filtered_master.groupby(['City', 'Latitude', 'Longitude'])
                                 .agg({'Loyalty#': 'count'}).reset_index()
                                 .rename(columns={'Loyalty#': 'ClientCount'}))
    
    fig_map = px.scatter_mapbox(
        city_counts,
        lat='Latitude',
        lon='Longitude',
        size='ClientCount',
        color='ClientCount',
        hover_name='City',
        zoom=3,
        title='Customers per City',
        size_max=30,
        color_continuous_scale='RdYlGn_r'  # green -> yellow -> red
    )
    # Add marker opacity and borders
    fig_map.update_traces(marker=dict(opacity=0.85))
    fig_map.update_layout(mapbox_style="open-street-map", template='plotly_white',
                          margin=dict(t=40, b=0, l=0, r=0))
    
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Geolocation data not available for map rendering.")

