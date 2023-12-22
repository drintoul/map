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
cnxn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
cursor = cnxn.cursor()

# Streamlit app
st.title("Track & Field Venues")

# Example query

@st.cache_data(ttl=3600*24)
def query():

  cursor.execute("SELECT venue, latitude, longitude FROM venues WHERE latitude IS NOT NULL")
  results = cursor.fetchall()
  return pd.DataFrame(results, columns=['venue', 'lat', 'lon'])

venues = query()

col1, col2 = st.columns(2)

venues = venues.sample(frac=1).head()

with col1:
  st.dataframe(venues, hide_index=True)

with col2:
  st.map(venues)

cursor.close()
cnxn.close()
