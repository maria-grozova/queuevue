import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Wait time stats",
    page_icon="🎡",
    layout="centered"
)

# Page dataframe imports

# Import the average wait time CSV file
avg_wait = "etl/data/outputs/average_wait.csv"
avg_wait_df = pd.read_csv(avg_wait)
# Get unique continents from the dataframe
continents = avg_wait_df["continent"].unique()

# Import the maximum wait time CSV file
max_wait = "etl/data/outputs/max_wait_per_continent.csv"
max_wait_df = pd.read_csv(max_wait).set_index("continent")

# Create filtered DataFrames for each continent
filtered_dataframes = {}
for continent in continents:
    filtered_dataframes[continent] = avg_wait_df[
        avg_wait_df["continent"] == continent
    ]

# Main page content
st.title("Wait time stats")
st.write(
    "##### Average ride wait times by theme park. "
    "Select a continent to filter the data."
)
st.markdown('''
    Parks displaying no data have an average wait times of 0 minutes
    Hover over the bars to see the ride names and wait times''')

# Filter selector (continents)
options = []
for continent in continents:
    options.append(continent)
selection = st.segmented_control(
    "Filter by", options, default=options[1], selection_mode="single"
)
# Display the filtered bar chart and metric based on the selected continent
st.bar_chart(
    filtered_dataframes[selection],
    x="park_name",
    y="avg_wait_time",
    y_label="Theme park name",
    x_label="Average wait time",
    color="ride_name",
    horizontal=True,
    use_container_width=True
)

row = max_wait_df.loc[selection]  # Get the row for the selected continent
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Longest ride wait in this region:",
        f"{row['wait_time']} minutes",
        label_visibility="visible",
        border=True
    )
    st.caption(f"Wait time recorded on **{row['date']}**")
with col2:
    st.write(f"Ride name: **{row['ride_name']}**")
    st.write(f"Theme park name: **{row['park_name']}**")
    st.write(f"Country: **{row['country']}**")
