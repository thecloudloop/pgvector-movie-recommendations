from pgvector.psycopg2 import register_vector
import psycopg2
import psycopg2.extras
import os
import sys
from sentence_transformers import SentenceTransformer

dbhost=os.environ.get('DBHOST', 'host.docker.internal')
dbport=os.environ.get('DBPORT', 5433)
dbuser=os.environ.get('DBUSER', 'postgres')
dbpass=os.environ.get('DBPASSWORD', 'postgres')
dbname=os.environ.get('DBNAME', 'moviesdb')

conn = psycopg2.connect(database=dbname, host=dbhost, port=dbport, user=dbuser, password=dbpass)
conn.set_session(autocommit=True)

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def gen_embedding_overview(conn, model):

    dbcur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    dbcur.execute("create extension if not exists vector;")
    register_vector(conn)
    dbcur.execute("alter table movie.movies add if not exists embedding vector(768);")
    dbcur.execute("select * from movie.movies ;")
    result = dbcur.fetchall()
    for r in result:
        print (r.get('id'))
        embedding = model.encode( r.get('overview') + ' ' + ' '.join(r.get('keywords')) )
        dbcur.execute("""UPDATE movie.movies SET embedding = %s WHERE id = %s;""", (embedding, r.get('id')))
    conn.commit()
    dbcur.execute("vacuum full analyze movie.movies;")
    dbcur.close()

def gen_embedding_users(conn, model):

    dbcur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    dbcur.execute("create extension if not exists vector;")
    register_vector(conn)
    dbcur.execute("alter table movie.movies add if not exists users_watched_embedding vector(768);")
    dbcur.execute("select * from movie.movies ;")
    result = dbcur.fetchall()
    for r in result:
        print (r.get('id'))
        embedding = model.encode( r.get('title') + ' ' + ' '.join(r.get('users_watched')) )
        dbcur.execute("""UPDATE movie.movies SET users_watched_embedding = %s WHERE id = %s;""", (embedding, r.get('id')))
    conn.commit()
    dbcur.execute("CREATE INDEX ON movie.movies USING ivfflat (embedding vector_cosine_ops) WITH (lists = 250);")
    dbcur.execute("CREATE INDEX ON movie.movies USING ivfflat (users_watched_embedding vector_cosine_ops) WITH (lists = 250);")
    dbcur.execute("vacuum full analyze movie.movies;")
    dbcur.close()

gen_embedding_overview(conn, model)
gen_embedding_users(conn, model)
conn.close()
