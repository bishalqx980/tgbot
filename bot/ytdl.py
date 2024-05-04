import requests
from pytube import YouTube, Search


class YouTubeDownload:
    async def ytdl(url, extention):
        try:
            print("Starting Download...")
            def _on_progress(stream, chunk, bytes_remaining):
                total_size = stream.filesize
                progress = (total_size - bytes_remaining) * 100 / total_size
                print(f"Downloading... {int(progress)}%")

            yt = YouTube(url, on_progress_callback=_on_progress)
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
            file_path = "ytdl/download/"
            thumbnail = "ytdl/download/thumbnail.png"

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
                    with open(thumbnail, "wb") as t_file:
                        t_file.write(t_res.content)
                        print("Thumbnail Downloaded!")
                else:
                    print("Thumbnail Download Failed!")
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


    async def yts(keyword):
        try:
            print("Searching...")
            result = Search(keyword).results
            print(f"Video Found: {len(result)}")
            return result
        except Exception as e:
            print(f"Error yts: {e}")
