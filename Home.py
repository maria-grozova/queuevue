import requests
import streamlit as st
from streamlit_lottie import st_lottie

# Page configuration
st.set_page_config(
    page_title="queuevue",
    page_icon="🎢",
    layout="centered"
)

# Importing the lottie animation
url = requests.get("https://lottie.host/4810a552-ab6b-48f6-b86c-a3279f9a308d/QoTPUx0C9V.json")
url_json = dict()
if url.status_code == 200:
    url_json = url.json()
else:
    print("Error in lottie animation URL")


# Main page content
st.write("# Welcome to QueueVue")
st.write("Explore theme park wait time stats and trends")

st_lottie(url_json,
    height=400,
    width=400,
    speed=0.5,
    loop=True,
    quality='high',
    key='Rollercoaster'
)

# Footer
st.divider()
st.markdown("[Powered by Queue-Times.com](https://queue-times.com/)")

# Sidebar navigation
st.sidebar.write("Select an option above to get started")
