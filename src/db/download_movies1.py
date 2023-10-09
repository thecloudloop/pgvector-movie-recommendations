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


headers = {
    "accept": "application/json",
    "Authorization": "Bearer <Token>"
}

s = requests.Session()
s.headers.update(headers)
dbconn = psycopg2.connect(host='localhost', port=5433, database="moviesdb", user="postgres", password="postgres")
dbcur = dbconn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
dbcur.execute("select * from movie.movies where users_watched is null")
result = dbcur.fetchall()
for movie in result:
    total_pages=1
    page = 1
    first_time = True
    print ('Working on movie ..{}'.format(movie.get('title')))
    userswatched = []
    while page <= total_pages:
        response = s.get(reviewurl.format(movie.get('id'), page, ), headers=headers)
        reviewers = json.loads(response.text)
        userslist = [ x.get('author_details', {}).get('username') for x in reviewers.get('results', []) ]
        userswatched = userswatched + userslist
        page = page + 1
        if first_time:
            total_pages = reviewers.get('total_pages', 1)
    print ("final userswatched {}".format(userswatched))
    sql = """update movie.movies set users_watched = %s where id = %s;"""
    dbcur.execute(sql, (userswatched, movie.get('id'),))
    dbconn.commit()

dbconn.commit()
dbconn.close()
