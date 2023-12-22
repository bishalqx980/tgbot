import requests
from helper import shortener_api_key

def shortener_url(url):
    try:
        post_url = f"https://shrinkme.io/api?api={shortener_api_key}&url={url}"
        response = requests.get(post_url)
        shortened_url = response.json().get("shortenedUrl")
        if shortened_url:
            return shortened_url
    except Exception as e:
        print(e)
