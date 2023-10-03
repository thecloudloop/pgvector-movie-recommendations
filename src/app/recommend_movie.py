import openai
from pgvector.psycopg2 import register_vector
import psycopg2
import psycopg2.extras
import os

movie_watched = "The Martian"
#movie_watched = "Gravity"
#movie_watched = "The Equalizer"
#movie_watched = "Barbie"

conn = psycopg2.connect(database='moviesdb', host='localhost', port=5433, user='postgres', password='postgres')
conn.set_session(autocommit=True)

dbcur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

dbcur.execute("""SET ivfflat.probes = 10;""")

def recommend_movie_from_content(dbcur, movie_watched):
    print ("Movies recommended by content: ")
    dbcur.execute("""SELECT m.id, m.title FROM movie.movies m WHERE title <> %s ORDER BY m.embedding <=> (SELECT embedding FROM movie.movies WHERE title = %s)  LIMIT 5;""", (movie_watched,movie_watched,))
    for r in dbcur.fetchall():
        print (r)

def recommend_movie_from_users(dbcur, movie_watched):
    print ("Movies recommended by users: ")
    dbcur.execute("""SELECT m.id, m.title FROM movie.movies m WHERE title <> %s ORDER BY m.users_watched_embedding <=> (SELECT users_watched_embedding FROM movie.movies WHERE title = %s)  LIMIT 5;""", (movie_watched,movie_watched,))
    for r in dbcur.fetchall():
        print (r)

recommend_movie_from_content(dbcur, movie_watched)
recommend_movie_from_users(dbcur, movie_watched)
conn.close()
