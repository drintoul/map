import streamlit as st
import pymysql
import pandas as pd
import numpy as np
import pydeck as pdk

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

sql = "select v.venue, latitude as 'lat', longitude as 'lon' " \
      "from venues v, performances p " \
      "where v.latitude is not null and v.longitude is not null " \
      "and p.venue = v.venue and p.competitor = 'Julien ALFRED';" 

@st.cache_data(ttl=3600)
def query():

  cursor.execute(sql)
  results = cursor.fetchall()
  venues = pd.DataFrame(results, columns=['venue', 'lat', 'lon'])
  return venues

venues = query()

st.dataframe(venues, hide_index=True)
st.map(venues)

cursor.close()
cnxn.close()
