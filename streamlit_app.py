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

sql = "select v.venue, latitude as 'lat', longitude as 'lon', count(*) as 'count' " \
      "from venues v, performances p " \
      "where v.latitude is not null and v.longitude is not null " \
      "and p.venue = v.venue group by p.venue " \
      "order by count(*) desc limit 10;"

@st.cache_data(ttl=3600*24)
def query():

  cursor.execute(sql)
  results = cursor.fetchall()
  venues = pd.DataFrame(results, columns=['venue', 'lat', 'lon', 'count'])
  return venues

venues = query()

#st.dataframe(venues, hide_index=True)
#st.map(venues)

cursor.close()
cnxn.close()

st.pydeck_chart(pdk.Deck(
    map_style=None,
    #initial_view_state=pdk.ViewState(
    #    latitude=37.76,
    #    longitude=-122.4,
    #    zoom=11,
    #    pitch=50,
    #),
    layers=[
        #pdk.Layer(
        #   'HexagonLayer',
        #   data=venues,
        #   get_position='[lon, lat]',
        #   radius=200,
        #   elevation_scale=4,
        #   elevation_range=[0, 1000],
        #   pickable=True,
        #   extruded=True,
        #),
        pdk.Layer(
            'ScatterplotLayer',
            data=venues,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))
