import requests
from telegraph import Telegraph
from bot import logger

try:
    domains = ["telegra.ph", "graph.org"]
    for domain in domains:
        try:
            response = requests.get(f"https://{domain}", timeout=3)
            if response.status_code == 200:
                break
        except Exception as e:
            logger.error(e)
    
    telegraph = Telegraph(domain=domain)
    telegraph.create_account("@MissCiri_bot")
except Exception as e:
    logger.error(e)

class TELEGRAPH:
    def paste(text, username="anonymous"):
        """
        use <br> instead of \.n
        """
        try:
            path = telegraph.create_page(
                f"{username} - @MissCiri_bot",
                html_content=text,
                author_name=f"{username} using @MissCiri_bot",
                author_url="https://t.me/MissCiri_bot"
            )
            
            return path.get("url")
        except Exception as e:
            logger.error(e)


    def upload_img(image_path):
        try:
            path = telegraph.upload_file(image_path)[0]
            link = f"https://telegra.ph{path.get('src')}"
            return link
        except Exception as e:
            logger.error(e)
