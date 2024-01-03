from pytube import YouTube


class YouTubeDownload:
    def ytdl(url):
        yt = YouTube(url)
        title = yt.title
        file_type = "audio"
        extention = "mp3"
        order_by = "abr"
        file_path = "ytdl/download/"

        stream = (
            yt.streams
            .filter(type=file_type)
            .order_by(order_by)
            .desc()
            .first()
        )
        if stream:
            filename = f"{title}.{extention}"
            file_path = stream.download(output_path=file_path, filename=filename)
            return title, file_path
        else:
            print("No stream found for this video")
