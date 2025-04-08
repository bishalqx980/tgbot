from .. import logger
from yt_dlp import YoutubeDL

def youtube_download(url):
    """
    ***Note: only `mp3` audio file download***
    """
    try:
        options = {
            "format": "bestaudio[ext=mp3]/bestaudio/best",
            "outtmpl": "downloads/audio.mp3"
        }

        ytdl = YoutubeDL(options)
        ytdl.download([url])

        file_info = ytdl.extract_info(url)
        data = {
            "file_name": file_info["fulltitle"],
            "file_path": "downloads/audio.mp3"
        }

        return data
    except Exception as e:
        logger.error(e)
