import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Load the data for People of Determination
@st.cache_data
def load_pod_data():
    return pd.read_excel('data/my_analysis.xlsx')

# Load the data for Public Association
@st.cache_data
def load_public_assoc_data():
    return pd.read_excel('data/output2.xlsx')

# Sidebar filters for People of Determination
def pod_sidebar_filters(df):
    year_list = list(df["Year"].unique())
    year_list.sort()
    year = st.sidebar.selectbox("Year", year_list, index=len(year_list)-1)  # Select the latest year by default
    
    emirates_list = [""] + list(df["Emirates"].unique())
    emirates_list.sort()
    emirate = st.sidebar.selectbox("Emirate", emirates_list)

    pod_category_list = [""] + df.columns[4:14].tolist()  # Exclude the first four columns (Emirates, Year, Male, Female)
    pod_category = st.sidebar.selectbox("POD Category", pod_category_list)

    return year, emirate, pod_category

# Sidebar filters for Public Association
def public_assoc_sidebar_filters(df):
    year_list = list(df["TIME_PERIOD"].unique())
    year_list.sort()
    default_year_index = year_list.index(2023) if 2023 in year_list else len(year_list)-1
    year = st.sidebar.selectbox("Year", year_list, index=default_year_index)  # Default to 2023 if available
    
    emirates_list = ["UAE"] + list(df["Reference area"].unique())
    emirates_list.sort()
    emirate = st.sidebar.selectbox("Emirate", emirates_list, index=0 if "UAE" in emirates_list else len(emirates_list)-1)  # Default to UAE if available
    
    public_assoc_type_list = [""] + list(df.columns[2:-1])  # Exclude the first two columns (TIME_PERIOD and Reference area) and the last column (Total)
    public_assoc_type = st.sidebar.selectbox("Public Assoc Type", public_assoc_type_list)

    return year, emirate, public_assoc_type

# Function to generate charts for People of Determination
def generate_pod_charts(df, year, emirate, pod_category):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df['Year'] == year]  # Filter data by year

    if emirate and emirate != "UAE":
        filtered_df = filtered_df[filtered_df['Emirates'] == emirate]  # Filter data by emirate

    if pod_category:
        filtered_df = filtered_df.groupby('Emirates').sum()[pod_category].reset_index()  # Filter data by POD category

    # Generate charts
    charts = []

    if year:
        # Chart showing total disabled by category for the selected year
        total_disabled_by_category = filtered_df.set_index('Emirates')
        chart = go.Figure()
        for col in total_disabled_by_category.columns[1:]:
            chart.add_trace(go.Bar(x=total_disabled_by_category.index, y=total_disabled_by_category[col], name=col))
        chart.update_layout(title=f'Total Disabled by POD Category in {year}')
        charts.append(chart)

    if year and emirate:
        # Chart showing disabled by category over the years in the selected emirate
        emirate_filtered_df = df[df['Emirates'] == emirate]
        chart = go.Figure()
        for col in emirate_filtered_df.columns[4:14]:
            chart.add_trace(go.Scatter(x=emirate_filtered_df['Year'], y=emirate_filtered_df[col], mode='lines', name=col))
        chart.update_layout(title=f'Disabled in {emirate} by POD Category over the Years')
        charts.append(chart)

    if year and pod_category:
        # Chart showing disabled in the selected category over the years
        category_filtered_df = df.groupby('Year').sum().reset_index()
        chart = go.Figure()
        chart.add_trace(go.Scatter(x=category_filtered_df['Year'], y=category_filtered_df[pod_category], mode='lines', name=pod_category))
        chart.update_layout(title=f'{pod_category} over the Years')
        charts.append(chart)

    return charts

# Function to generate charts for Public Association
def generate_public_assoc_charts(df, year, emirate, public_assoc_type):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df["TIME_PERIOD"] == year]

    if emirate and emirate != "UAE":
        filtered_df = filtered_df[filtered_df["Reference area"] == emirate]

    if public_assoc_type:
        filtered_df = filtered_df.groupby("TIME_PERIOD").sum()[public_assoc_type].reset_index()

    # Generate charts
    charts = []

    if year and emirate:
        if emirate == "UAE":
            # Chart showing total number of public associations for the selected year and all emirates
            total_public_assoc = filtered_df.set_index('TIME_PERIOD')
            chart = go.Figure()
            chart.add_trace(go.Bar(x=total_public_assoc.index, y=total_public_assoc.iloc[:, 1:].sum(axis=1), name="Total Public Assoc"))
            chart.update_layout(title=f'Total Number of Public Associations in {year} across Emirates', xaxis_title='Year', yaxis_title='Total Number of Public Associations')
            charts.append(chart)
        else:
            # Chart showing number of public associations for the selected emirate across years
            emirate_filtered_df = df[df["Reference area"] == emirate]
            chart = go.Figure()
            for col in emirate_filtered_df.columns[2:-1]:
                chart.add_trace(go.Scatter(x=emirate_filtered_df['TIME_PERIOD'], y=emirate_filtered_df[col], mode='lines', name=col))
            chart.update_layout(title=f'Number of Public Associations in {emirate} over the Years', xaxis_title='Year', yaxis_title='Number of Public Associations')
            charts.append(chart)

    if year and public_assoc_type:
        # Chart showing number of public associations of the selected type for the selected emirate (if applicable) or UAE across years
        if emirate == "UAE":
            uae_filtered_df = df.groupby("TIME_PERIOD").sum().reset_index()
            chart = go.Figure()
            chart.add_trace(go.Scatter(x=uae_filtered_df['TIME_PERIOD'], y=uae_filtered_df[public_assoc_type], mode='lines', name=public_assoc_type))
            chart.update_layout(title=f'Number of {public_assoc_type} in UAE over the Years', xaxis_title='Year', yaxis_title=f'Number of {public_assoc_type}')
            charts.append(chart)
        else:
            emirate_filtered_df = df[df["Reference area"] == emirate]
            chart = go.Figure()
            chart.add_trace(go.Scatter(x=emirate_filtered_df['TIME_PERIOD'], y=emirate_filtered_df[public_assoc_type], mode='lines', name=public_assoc_type))
            chart.update_layout(title=f'Number of {public_assoc_type} in {emirate} over the Years', xaxis_title='Year', yaxis_title=f'Number of {public_assoc_type}')
            charts.append(chart)

    return charts

# Main function
def main():
    # Sidebar filters
    data_type = st.sidebar.selectbox("Data Type", ["People of Determination", "Public Association"])

    if data_type == "People of Determination":
        df = load_pod_data()
        year, emirate, pod_category = pod_sidebar_filters(df)
        charts = generate_pod_charts(df, year, emirate, pod_category)
        title = "People of Determination"
    else:
        df = load_public_assoc_data()
        year, emirate, public_assoc_type = public_assoc_sidebar_filters(df)
        charts = generate_public_assoc_charts(df, year, emirate, public_assoc_type)
        title = "Public Association"

    # Plot charts
    st.title(f"Chart analysis for the data on {title}")
    for chart in charts:
        st.plotly_chart(chart, use_container_width=True)

# Run the main function
if __name__ == "__main__":
    main()
