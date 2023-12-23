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

query = """select v.venue, latitude as 'lat', longitude as 'lon', count(*) as 'count'
           from venues v, performances p
           where v.latitude is not null and v.longitude is not null
           and p.venue = v.venue group by p.venue
           order by count(*) desc limit 10;"""

#@st.cache_data(ttl=3600*24)
def query():

  cursor.execute(query)
  results = cursor.fetchall()
  venues = pd.DataFrame(results, columns=['venue', 'lat', 'lon'])
  return venues.sample(frac=1).head()

venues = query()

st.dataframe(venues, hide_index=True)
st.map(venues)

cursor.close()
cnxn.close()
