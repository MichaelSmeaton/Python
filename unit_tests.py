import unittest
from src.controller import WebScrapingController
from src.model import WebScraper


class UnitTest(unittest.TestCase):

    def test_valid_url(self):
        self._model = WebScraper()
        self.expected = True
        self.assertEquals(self._model.is_valid("http://www.google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("https://www.google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("https://google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("http://WWW.GoOgLe.cOm"),
                          self.expected)
        self.assertEquals(self._model.is_valid("http://www.google.com/maps"),
                          self.expected)
        self.assertEquals(self._model.is_valid("http://maps.google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("http://www.google.domain.com"),
                          self.expected)
        self.expected = False
        self.assertEquals(self._model.is_valid("www.google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("com.google.www//:http"),
                          self.expected)
        self.assertEquals(self._model.is_valid("google.http://www.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("www.http://.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("http:\\\\www.google.com"),
                          self.expected)
        self.assertEquals(self._model.is_valid("htps://www.google.com"),
                          self.expected)

    def test_pickle(self):
        self.controller = WebScrapingController(WebScraper())
        self.controller.get_data()
        self.controller.save_pickle_data()
        self.controller._container = {}
        self.controller.load_pickle_data()
        self.expected = 10
        self.failUnlessEqual(len(self.controller.get_container(0)),
                             self.expected)

    def test_whitespace(self):
        self._model = WebScraper()
        self.expected = "http://www.google.com"
        self.assertEquals(self._model.is_correct("http://www.g o o g l e.com"),
                          self.expected)
        self.assertEquals(self._model.is_correct
                          ("http : / / www.google . com"), self.expected)
