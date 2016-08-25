from abc import ABC, abstractmethod, ABCMeta


class Controller(ABC):
    __metaclass__ = ABCMeta
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._data = []
        self._url = 'http://www.blog.pythonlibrary.org/'

    @abstractmethod
    def go(self):
        return "Start your engines!"


class WebScrapingController(Controller):
    def __init__(self, view, model):
        super(WebScrapingController, self).__init__(view, model)

    def go(self):
        self._view.start()
        #self._url = self._view.get("How may I be of service to you?")
        self._url = self._model.is_correct(self._url)
        if self._model.is_connected(self._url):
            self._data = self._model.fetch(self._url)
            self._view.say_list(self._data)
        self._view.stop()

        #is_valid tests
        self._model.is_valid("http://www.google.com") #good
        self._model.is_valid("https://www.google.com") #good
        self._model.is_valid("www.google.com")
        self._model.is_valid("google.com")
        self._model.is_valid("com.google.www//:http")
        self._model.is_valid("https://google.com") #good
        self._model.is_valid("google.http://www.com")
        self._model.is_valid("www.http://.com")
        self._model.is_valid("http:\\\\www.google.com")
        self._model.is_valid("htps://www.google.com")
        self._model.is_valid("http://WWW.GoOgLe.cOm") #good
        self._model.is_valid("http://www.google.com/maps") #good
        self._model.is_valid("http://maps.google.com") #good
        self._model.is_valid("http://www.google.domain.com") #good
        self._model.is_valid(" ")

