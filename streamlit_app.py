import streamlit as st
import pymysql
import pandas as pd

# Database connection details
host = st.secrets["database"]["host"]
user = st.secrets["database"]["user"]
password = st.secrets["database"]["password"]
database = st.secrets["database"]["name"]
port = st.secrets["database"]["port"]

# Connect to the database
conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
cursor = conn.cursor()

# Streamlit app
st.title("Track & Field Venues")

# Example query
query = "SELECT venue, latitude AS 'lat', longitude AS 'long' FROM venues WHERE latitude IS NOT NULL"
@st.cache_data(ttl=86400)
cursor.execute(query)
results = cursor.fetchall()

venues = pd.DataFrame(results, columns=['venue', 'lat', 'lon'])

col1, col2 = st.columns(2)

venues = venues.sample(frac=1).head()

with col1:
  st.dataframe(venues, hide_index=True)

with col2:
  st.map(venues)
