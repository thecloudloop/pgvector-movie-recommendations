import streamlit as st
import pandas as pd
import psycopg2
import psycopg2.extras
import os

dbhost=os.environ.get('DBHOST', 'host.docker.internal')
dbport=os.environ.get('DBPORT', 5433)
dbuser=os.environ.get('DBUSER', 'postgres')
dbpass=os.environ.get('DBPASSWORD', 'postgres')
dbname=os.environ.get('DBNAME', 'moviesdb')

st.write("## :blue[Discover Your Next Favorite Movie :cinema:]")

@st.cache_data
def load_data():
    with psycopg2.connect(database=dbname, host=dbhost, port=dbport, user=dbuser, password=dbpass) as dbconn:
        sql = "SELECT id, title FROM movie.movies;"
        return pd.read_sql_query(sql, dbconn, index_col="id")

def write_columns_data(result):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.image("https://image.tmdb.org/t/p/w185{}".format(result[0].get('poster')))
    col2.image("https://image.tmdb.org/t/p/w185{}".format(result[1].get('poster')))
    col3.image("https://image.tmdb.org/t/p/w185{}".format(result[2].get('poster')))
    col4.image("https://image.tmdb.org/t/p/w185{}".format(result[3].get('poster')))
    col5.image("https://image.tmdb.org/t/p/w185{}".format(result[4].get('poster')))
    return

try:
    df = load_data()
    option = st.selectbox('##### :red[Select a movie you watched?]', df.title.unique())
    st.write('You have selected :blue[', option, ']')
    st.divider()
    with st.container():
        st.write("##### :green[Personalized Movie Recommendations]")
        with psycopg2.connect(database=dbname, host=dbhost, port=dbport, user=dbuser, password=dbpass) as dbconn:
            dbcur = dbconn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            dbcur.execute("SELECT m.id, m.title, m.poster FROM movie.movies m WHERE title <> %s ORDER BY m.embedding <=> (SELECT embedding FROM movie.movies WHERE title = %s LIMIT 1)  LIMIT 5;", (option, option, ))
            result = dbcur.fetchall()
            write_columns_data(result)
    st.divider()

    with st.container():
        st.write("##### :violet[Movie Recommendations from Similar Viewers]")
        with psycopg2.connect(database=dbname, host=dbhost, port=dbport, user=dbuser, password=dbpass) as dbconn:
            dbcur = dbconn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            dbcur.execute("SELECT m.id, m.title, m.poster FROM movie.movies m WHERE title <> %s ORDER BY m.users_watched_embedding <=> (SELECT embedding FROM movie.movies WHERE title = %s LIMIT 1)  LIMIT 5;", (option, option, ))
            result = dbcur.fetchall()
            write_columns_data(result)

    st.divider()
        
except Exception as e:
    print ("Error {}".format(e))
