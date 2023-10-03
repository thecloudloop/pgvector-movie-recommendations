import requests
import json
import psycopg2

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&language=en-US&sort_by=popularity.desc&with_original_language=en&page={}"
kwurl = "https://api.themoviedb.org/3/movie/{}/keywords"
videourl = "https://api.themoviedb.org/3/movie/{}/videos?language=en-US"
crediturl = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US"

total_pages=500
page = 1

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzOTMwN2I2ZjBmN2JmNmNiNzRlMzNiNjQ0YWZiMjY1NSIsInN1YiI6IjY1MDI3NmI0NmEyMjI3MDBhYmE5NzYwYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.D20xmqrADx67d7tzKhUkfI4QIC8YTB13EdWfr3rBKko"
}

s = requests.Session()
s.headers.update(headers)
dbconn = psycopg2.connect(host='localhost', port=5432, database="moviesdb", user="postgres", password="postgres")
dbcur = dbconn.cursor()
while page <= total_pages:
    response = s.get(url.format(page), headers=headers)
    moviedata = json.loads(response.text)
    for movie in moviedata.get('results', []):
        print ('Working on movie ..{}'.format(movie.get('title')))
        response = s.get(kwurl.format(movie.get('id')), headers=headers)
        keywords = json.loads(response.text)
        keywords = keywords.get('keywords')    
        response = s.get(crediturl.format(movie.get('id')), headers=headers)
        credits = []
        videos = []
        for x in json.loads(response.text).get('cast'):
            if x.get('order') > 8:
                break
            credits.append( {'name': x.get('name'), 'order': x.get('order') } )
        response = s.get(videourl.format(movie.get('id')), headers=headers)
        videos = [ x.get('key') for x in json.loads(response.text).get('results') if x.get('site') == 'YouTube' and x.get('type') == 'Trailer' and x.get('official') == True and x.get('iso_639_1') == 'en' and x.get('iso_3166_1') == 'US' ]
        credits = json.dumps(credits)
        videos = json.dumps(videos)
        sql = "insert into movie.movies(id, title, genre_ids, overview, vote_average, vote_count, popularity, credits, videos) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        dbcur.execute(sql, (movie.get('id'), movie.get('title'), movie.get('genre_ids'), movie.get('overview'), movie.get('vote_average'), movie.get('vote_count'), movie.get('popularity'), credits, videos, ))
        dbconn.commit()
#    with open("movies.{}.json".format(page), "w") as outfile:
#        json.dump(json.loads(response.text), outfile, indent=4)
    page = page + 1
