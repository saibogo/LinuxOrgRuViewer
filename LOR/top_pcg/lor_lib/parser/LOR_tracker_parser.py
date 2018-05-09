import bs4
import requests
from lor_lib.parser.config import Config as Cfg
import lor_lib.parser.topic_from_tracker as urlreader


class LorTrackerParser:
    __server_name = "https://www.linux.org.ru"
    __topicks = []
    __current_index = 0

    def __init__(self):
        self.__get_tracker()

    def __get_tracker(self):
        self.__topicks = []

        req = requests.get(self.__server_name + "/tracker/")
        data = bs4.BeautifulSoup(req.text, "html.parser")
        all_msgs = str(data.select(".forum")[0])
        ind = all_msgs.index("<tbody>") + len("<tbody>")
        all_msgs = all_msgs[ind:]

        threads = []

        while "<tr>" in all_msgs:
            ind = all_msgs.index("<tr>")
            all_msgs = all_msgs[ind + len("<tr>"):]
            ind = all_msgs.index("</tr>")
            tmp = all_msgs[:ind]

            ind0 = tmp.index("</a></td>")
            tmp = tmp[ind0 + len("</a></td>"):]

            ind1 = tmp.index("<a href=")
            ind2 = tmp[ind1:].index(">")
            link = self.__server_name + tmp[ind1 + len("<a href=") + 1: ind1 + ind2 - 1].strip()

            ind4 = tmp.index("</a>")
            ind3 = ind4 - 1
            while tmp[ind3] != ">":
                ind3 -= 1
            title = tmp[ind3 + 1:ind4].strip()

            threads.append(urlreader.TopicFromTracker(title, link))
            threads[-1].start()

        for elem in threads:
            self.__topicks.append(elem.join())

        if len(self.__topicks) > Cfg.get_max_len_stack():
            self.__topicks = self.__topicks[:Cfg.get_max_len_stack()]

    def __next__(self):
        if self.__current_index < len(self.__topicks):
            self.__current_index += 1
            return self.__topicks[self.__current_index - 1]
        else:
            self.__current_index = 0
            raise StopIteration

    def __iter__(self):
        return self

    def get_tracker(self):
        self.__get_tracker()

    @staticmethod
    def resource_name():
        return "Linux Org Ru (LOR) tracker"
