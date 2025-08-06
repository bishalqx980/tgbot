from bot import logger
from yt_dlp import YoutubeDL

def youtube_download(url):
    """
    ***Note: only `mp3` audio file download***\n
    :return dict: contains `file_name` and `file_path`
    """
    try:
        with YoutubeDL() as ytdl:
            file_info = ytdl.extract_info(url, download=False)
            title = file_info["title"]
            
            # Clean the title to make it filesystem-safe
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            file_path = f"downloads/{safe_title}.mp3"

            # Download with the sanitized filename
            ytdl = YoutubeDL({
                "format": "bestaudio[ext=mp3]/bestaudio/best",
                "outtmpl": file_path,
                "extractaudio": True,
                "audioformat": "mp3",
            })
            ytdl.download([url])

        return {
            "title": safe_title,
            "file_path": file_path
        }
    except Exception as e:
        logger.error(e)
        return str(e)
