import requests
import re
from bs4 import BeautifulSoup
from decimal import Decimal


class WebScraper:
    def is_correct(self, url):
        """
        Method WebScraper.is_correct()'s docstring.
        Check if URL is missing scheme. Only for HTTP and HTTPS URLS
        Remove extra whitespaces
        """
        if ' ' in url:
            words = url.split()
            url = ""
            for li in words:
                url += li

        s = ["http://", "https://"]
        count = 0
        for i in s:
            if i not in url or not url.startswith(i):
                count += 1
                if count == 2:
                    url = s[0] + url
        # print(url)
        return url

    def is_valid(self, url):
        """
        Method WebScraper.is_valid()'s docstring.
        Check if URL is valid and is in it's correct format. Supports HTTP and
        HTTPS
        """
        if re.match("((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", url,
                    re.I):
            # print("Good format")
            return True
        else:
            # print("Bad format")
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
            except requests.ConnectionError:
                print("Error: Failed to connect.")
                return False
            except requests.exceptions.InvalidURL:
                print("Error: Invalid URL.")
                return False

    def fetch(self, url, maximum=10):
        """
        Method WebScraper.fetch()'s docstring.
        Get data from Web page.
        """
        req = requests.get(url)
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        content = soup.find_all('div', {'id': 'main'})
        for div in content:
            li = div.find_all('li', limit=maximum)
            for data in li:
                results.append(data)
        return results

    def fetch_by_keyword(self, url, attr, keyword, maximum=10):
        """
        Method WebScraper.fetch()'s docstring.
        Get data by keyword lookup from Web page.
        """
        req = requests.get(url)
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        content = soup.find_all('div', {'id': 'main'})
        for div in content:
            ul = div.find_all('li')
            for li in ul:
                span = li.find_all('span', {attr: keyword}, limit=maximum)
                for kw in span:
                    results.append(kw)
        return results

    def extract(self, raw_data, option):
        """
        Method WebScraper.extract()'s docstring.
        Find and extract useful data
        """
        rule = {
            "ranking": "[0-9]+",
            "image": "(https?):(//)+[^\s]+\.(jpg|jpeg|jif|jfif|"
                     "gif|tif|tiff|png)",
            "album": ">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:"
                     "&quot;;'&lt;&gt;?,.\/ ]+<",
            "artist": ">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:"
                      "&quot;;'&lt;&gt;?,.\/ ]+<",
            "link": "((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)",
            "price": "[0-9]+\.[0-9]+"
        }
        results = []
        for item in raw_data:
            no_tags = str(item)
            if option == "ranking":
                try:
                    results.append(int(re.search(rule[option],
                                                 self.tag_content("strong",
                                                                  "strong",
                                                                  no_tags))
                                       .group(0)))
                except ValueError:
                    print("Error: Not an integer.")
                    return None
            elif option == "image":
                results.append(re.search(rule[option],
                                         self.tag_content("a href", "a",
                                                          no_tags), re.I)
                               .group(0))
            elif option == "album":
                no_tags = re.sub('(<strong>)(.*)'
                                 '(</strong>)', '', no_tags, re.I)
                data = (re.findall(rule[option], no_tags, re.I))
                results.append(self.clean(data, 0))
            elif option == "artist":
                no_tags = re.sub('(<strong>)(.*)'
                                 '(</strong>)', '', no_tags, re.I)
                data = (re.findall(rule[option], no_tags, re.I))
                results.append(self.clean(data, 1))
            elif option == "link":
                results.append(re.search(rule[option],
                                         self.tag_content("a href", "a",
                                                          no_tags), re.I)
                               .group(0))
            elif option == "price":
                results.append(Decimal(re.search(rule[option],
                                                 self.tag_content(
                                                     "span", "span", no_tags))
                                       .group(0)))
        return results

    def tag_content(self, open_tag, close_tag, data):
        """
        Method WebScraper.fetch()'s docstring.
        Should return a substring of string between and including tags
        """
        regex = r"(<" + \
                re.escape(open_tag) + r")(.*)(</" + \
                re.escape(close_tag) + ">)"
        return re.search(regex, data, re.I | re.M).group(0)

    def clean(self, data, x):
        """
        Method WebScraper.clean()'s docstring.
        Removes unwanted sequence of characters from a list of strings
        """
        chars = ['>', '<', "&amp;"]
        for i, items in enumerate(data):
            for c in chars:
                if c == "&amp;":
                    data[i] = data[i].replace(c, '&')
                else:
                    data[i] = data[i].replace(c, '')
        return data[x]
