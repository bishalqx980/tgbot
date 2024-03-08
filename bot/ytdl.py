from pytube import YouTube


class YouTubeDownload:
    async def ytdl(url, extention):
        try:
            print("Downloading...")
            yt = YouTube(url)
            title = yt.title
            thumbnail = yt.thumbnail_url
            extention = extention # mp3/mp4
            if extention == "mp4":
                file_type = "video"
                progressive = True
            elif extention == "mp3":
                file_type = "audio"
            progressive = False
            order_by = "abr" # bitrate
            file_path = "ytdl/download/"

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
                if file_path:
                    print("Video Downloaded!!")
                if extention == "mp4":
                    return title, file_path, thumbnail
                elif extention == "mp3":
                    return title, file_path
            else:
                print("No stream found for this video")
        except Exception as e:
            print(f"Error ytdl: {e}")
