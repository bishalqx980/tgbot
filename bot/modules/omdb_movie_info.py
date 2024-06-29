import requests
from bot import logger
from bot.modules.database.mongodb import MongoDB
from bot.modules.database.local_database import LOCAL_DATABASE

async def get_movie_info(movie_name=None, imdb_id=None, year=None):
  omdb_api = await LOCAL_DATABASE.get_data("bot_docs", "omdb_api")
  if not omdb_api:
    omdb_api = await MongoDB.get_data("bot_docs", "omdb_api")
    if not omdb_api:
      logger.error("omdb_api not found!")
      return False
  
  if movie_name:
    url = f"https://omdbapi.com/?apikey={omdb_api}&t={movie_name}&y={year}"
  elif imdb_id:
    url = f"https://omdbapi.com/?apikey={omdb_api}&i={imdb_id}"
  else:
    logger.info(f"Movie Name or IMDB ID not provided!!")
    return

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
    logger.error(e)
