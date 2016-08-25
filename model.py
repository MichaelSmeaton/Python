import requests
import re
from bs4 import BeautifulSoup


class WebScraper:
    def is_correct(self, url):
        """
        Method WebScraper.is_correct()'s docstring.
        Check if URL is missing scheme. Only for HTTP URLS
        Remove extra whitespaces
        Extension: Include HTTPS, FTP, SFTP and IP address checks
        """
        s = "http://"
        if s not in url or url.index(s) != 0:
            url = s+url
        words = url.split()
        new_url = ""
        for li in words:
            new_url += li
        return new_url

    def is_valid(self, url):
        """
        Method WebScraper.is_valid()'s docstring.
        Check if URL is valid and is in it's correct format. Supports HTTP and HTTPS
        """
        if re.match("((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", url, re.I):
                print("Good format")
                return True
        else:
            print("Bad format")
            return False

    def is_connected(self, url):
        """
        Method WebScraper.is_connected()'s docstring.
        Check if HTTP response code is OK.
        """
        if self.is_valid(url):
            try:
                requests.head(url)
                return True
            except requests.ConnectionError as e:
                print(e)
                return False

    def fetch(self, url):
        """
        Method WebScraper.fetch()'s docstring.
        Get and store data from Web page.
        """
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        contents = soup.findAll('div')
        results = []
        for record in contents:
            results.append(record.text)
        return results