import requests
import json
import psycopg2
import psycopg2.extras
import sys
import os

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&language=en-US&sort_by=popularity.desc&with_original_language=en&page={}"
kwurl = "https://api.themoviedb.org/3/movie/{}/keywords"
videourl = "https://api.themoviedb.org/3/movie/{}/videos?language=en-US"
crediturl = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US"
reviewurl = "https://api.themoviedb.org/3/movie/{}/reviews?language=en-US&page={}"
posterurl = "https://api.themoviedb.org/3/movie/{}?language=en-US"


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzOTMwN2I2ZjBmN2JmNmNiNzRlMzNiNjQ0YWZiMjY1NSIsInN1YiI6IjY1MDI3NmI0NmEyMjI3MDBhYmE5NzYwYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.D20xmqrADx67d7tzKhUkfI4QIC8YTB13EdWfr3rBKko"
}

s = requests.Session()
s.headers.update(headers)
dbconn = psycopg2.connect(host='localhost', port=5433, database="moviesdb", user="postgres", password="postgres")
dbcur = dbconn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
dbcur.execute("select * from movie.movies where poster is null")
result = dbcur.fetchall()
sql = """update movie.movies set poster = %s where id = %s;"""
for movie in result:
    response = s.get(posterurl.format(movie.get('id'),), headers=headers)
    poster = json.loads(response.text).get("poster_path")
    if poster:
       dbcur.execute(sql, (poster, movie.get('id'),))
       dbconn.commit()

dbconn.commit()
dbconn.close()
