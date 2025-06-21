import re

class RE_LINK:
    @staticmethod
    def detectLinks(text):
        """
        :param text: text that contain link/s
        :returns list: list of link/s contains in given text
        """
        pattern = r"(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(/[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=%]*)?"
        links = re.findall(pattern, text)
        return ["".join(link) for link in links]
    
    @staticmethod
    def extractDomainName(link):
        """
        :param link: link/URL
        :returns str: domain name of the given link
        """
        domain_match = re.search(r"([a-zA-Z0-9-]+\.[a-zA-Z]{2,})", link)
        return domain_match.group(0) if domain_match else None
