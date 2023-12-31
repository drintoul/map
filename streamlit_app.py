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

sql = "select distinct competitor, v.venue, p.date, v.latitude as 'lat', v.longitude as 'lon' " \
      "from venues v, performances p " \
      "where v.latitude is not null and v.longitude is not null " \
      f"and p.venue = v.venue and p.date >= '2023' order by p.date; "

@st.cache_data(ttl=3600)
def query():

  cursor.execute(sql)
  results = cursor.fetchall()
  venues = pd.DataFrame(results, columns=['competitor', 'venue', 'date', 'lat', 'lon'])
  return venues

venues = query()

competitor = st.selectbox('Enter Competitor', ['Udodi Chudi ONWUZURIKE', 'Julien ALFRED', 'Matthew BOLING', 'Cass ELLIOTT', 'Maxwell OTTERDAHL'])
venues = venues[venues['competitor'] == competitor]

st.dataframe(venues, hide_index=True)
st.map(venues)

cursor.close()
cnxn.close()
