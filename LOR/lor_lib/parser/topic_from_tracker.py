import bs4
import requests
from threading import Thread
from lor_lib.parser.topic import Topic as Tpc


# noinspection PyMethodOverriding
class TopicFromTracker(Thread):
    __string_start = '<div itemprop="articleBody">'
    __string_stop = '</div>'

    def __init__(self, title, url):
        Thread.__init__(self)
        self.title = title
        self.url = url
        self.__return = Tpc(self.title, self.url, "")

    def run(self):
        req = requests.get(self.url)
        data = str(bs4.BeautifulSoup(req.text, "html.parser"))
        ind0 = data.find(self.__string_start) + len(self.__string_start)
        ind1 = data.find(self.__string_stop, ind0 + 1)
        soup = data[ind0: ind1]
        text = ''.join(bs4.BeautifulSoup(soup, "html.parser").findAll(text=True))
        self.__return = Tpc(self.title, self.url, text)

    def join(self):
        Thread.join(self)
        return self.__return
