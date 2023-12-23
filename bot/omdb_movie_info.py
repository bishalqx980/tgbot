import requests
from bot import omdb_api

def get_movie_info(movie_name=None, imdb_id=None, year=None):
  url = f"https://omdbapi.com/?apikey={omdb_api}&t={movie_name}&i{imdb_id}&y={year}"
  if movie_name or imdb_id:
    try:
      response = requests.get(url)
      if response.status_code == 200:
        output = response.json()

        poster = output.get("Poster") # img
        content_type = output.get("Type")
        title = output.get("Title")
        released = output.get("Released")
        runtime = output.get("Runtime") # return min
        runtime = f"{int(runtime[0:3]) // 60} Hour {int(runtime[0:3]) % 60} Min"
        genre = output.get("Genre")
        director = output.get("Director")
        writer = output.get("Writer")
        actors = output.get("Actors")
        plot = output.get("Plot")
        language = output.get("Language")
        country = output.get("Country")
        awards = output.get("Awards")
        meta_score = output.get("Metascore")
        imdb_rating = output.get("imdbRating")
        imdb_votes = output.get("imdbVotes")
        imdb_id = output.get("imdbID")
        box_office = output.get("BoxOffice")

        return poster, content_type, title, released, runtime, genre, director, writer, actors, plot, language, country, awards, meta_score, imdb_rating, imdb_votes, imdb_id, box_office
    except Exception as e:
      print(f"Error (Getting movie info): {e}")
  else:
    print(f"Movie Name or IMDB ID not provided!!")
