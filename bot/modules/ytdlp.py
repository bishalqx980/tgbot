from bot import logger
from yt_dlp import YoutubeDL

def youtube_download(url):
    """
    ***Note: only `mp3` audio file download***
    :returns path: audio file path
    """
    try:
        file_path = "downloads/audio.mp3"
        ytdl = YoutubeDL({"format": "bestaudio[ext=mp3]/bestaudio/best", "outtmpl": file_path})
        ytdl.download([url])

        # getting youtube (video) info
        file_info = ytdl.extract_info(url)

        return {"file_name": file_info["fulltitle"], "file_path": file_path}
    except Exception as e:
        logger.error(e)
