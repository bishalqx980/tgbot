import re

class RE_LINK:
    async def detect_link(text):
        """
        retuns `list` of links
        """
        link_pattern = r"(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=%]*)?"
        links = re.findall(link_pattern, text)
        links_list = ["".join(link) for link in links]
        return links_list
    

    async def get_domain(link):
        """
        returns str(`link`)
        """
        domain_match = re.search(r"([a-zA-Z0-9-]+\.[a-zA-Z]{2,})", link)
        if domain_match:
            domain = domain_match.group(0)
        else:
            domain = None
        return domain
