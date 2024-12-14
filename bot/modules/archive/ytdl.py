import requests
from bot import logger
from pytube import YouTube, Search

class PYTUBE:
    async def ytdl(url, extention):
        try:
            logger.info("Starting Download...")
            yt = YouTube(url)
            title = yt.title
            thumbnail_url = yt.thumbnail_url
            extention = extention # mp3/mp4
            if extention == "mp4":
                file_type = "video"
                progressive = True
            elif extention == "mp3":
                file_type = "audio"
                progressive = False
            order_by = "abr" # bitrate
            file_path = "download/"
            thumbnail = "download/thumbnail.jpg"

            stream = (
                yt.streams
                .filter(progressive=progressive, type=file_type) # progressive audio & video are not separate / highest quality 720p
                .order_by(order_by)
                .desc()
                .first()
            )

            if stream:
                filename = f"{title}.{extention}"
                file_path = stream.download(output_path=file_path, filename=filename)
                t_res = requests.get(thumbnail_url)
                if t_res.status_code == 200:
                    open(thumbnail, "wb").write(t_res.content)
                    logger.info("Thumbnail Downloaded!")
                else:
                    logger.info("Thumbnail Download Failed!")
                if file_path:
                    logger.info("Video Downloaded!!")
                if extention == "mp4":
                    return title, file_path, thumbnail
                elif extention == "mp3":
                    return title, file_path
            else:
                logger.info("No stream found for this video")
        except Exception as e:
            logger.error(e)
            return False, f"{e}"


    async def yts(keyword):
        try:
            logger.info("Searching...")
            result = Search(keyword).results
            logger.info(f"Video Found: {len(result)}")
            return result
        except Exception as e:
            logger.error(e)
