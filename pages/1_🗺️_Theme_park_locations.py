import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Theme Park Locations",
    page_icon="🗺️",
    layout="centered"
)

# Page dataframe imports
map = "etl/data/outputs/map_dataframe.csv"  # Import the map CSV file
map_df = pd.read_csv(map)

parks_by_continent = 'etl/data/outputs/parks_by_continent.csv'  # Import the parks count CSV file
parks_count_df = pd.read_csv(parks_by_continent)

parks_by_country = 'etl/data/outputs/parks_by_country.csv'  # Import the parks by country CSV file
countries_df = pd.read_csv(parks_by_country)

# Main page content
# Park location map
st.title("Theme park locations")
st.write("##### This is a map of theme parks, with each dot representing a tracked theme park")
st.map(data=map_df, latitude=None, longitude=None, color='#00ABAD', size=None, zoom=1, use_container_width=True, width=None, height=None)

# Parks count by continent
st.write("##### Theme parks tracked by continent:")
# Park count metric, depending on the selected continent
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(parks_count_df.iloc[0, 0], parks_count_df.iloc[0, 1], delta=None, delta_color="normal", help=None, label_visibility="visible", border=False)
with col2:
    st.metric(parks_count_df.iloc[1, 0], parks_count_df.iloc[1, 1], delta=None, delta_color="normal", help=None, label_visibility="visible", border=False)
with col3:
    st.metric(parks_count_df.iloc[2, 0], parks_count_df.iloc[2, 1], delta=None, delta_color="normal", help=None, label_visibility="visible", border=False)
with col4:
    st.metric(parks_count_df.iloc[3, 0], parks_count_df.iloc[3, 1], delta=None, delta_color="normal", help=None, label_visibility="visible", border=False)

# Parks count by country
st.write("##### Theme parks count by country:")
st.bar_chart(data=countries_df, x="country", y="num_of_parks", y_label="Country name", x_label="Parks count", color="continent", horizontal=True, use_container_width=True)
