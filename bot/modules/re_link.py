import re

class RE_LINK:
    def detect_link(text):
        """
        retuns `list` of links
        """
        link_pattern = r"(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=%]*)?"
        links = re.findall(link_pattern, text)
        return ["".join(link) for link in links]
    

    def get_domain(link):
        domain_match = re.search(r"([a-zA-Z0-9-]+\.[a-zA-Z]{2,})", link)
        return domain_match.group(0) if domain_match else None
