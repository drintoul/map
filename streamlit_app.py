import streamlit as st
import pymysql

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
st.title("MySQL-Streamlit App")

# Example query
query = "SELECT venue, latitude AS 'lat', longitude AS 'long' FROM venues WHERE latitude IS NOT NULL LIMIT 5"
cursor.execute(query)
venues = cursor.fetchall()

st.write(venues)
#st.map(venues)
