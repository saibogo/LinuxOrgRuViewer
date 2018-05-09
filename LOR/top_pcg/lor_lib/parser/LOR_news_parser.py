import bs4
import requests
import pickle
from lor_lib.parser.config import Config as Cfg
import os
import logging
import lor_lib.parser.topic_from_tracker as urlreader


class LorNewsParser:
    __server_name = 'https://www.linux.org.ru'
    __filename = None
    __lor_news = []
    __current_index = None

    def __init__(self):
        self.__filename = Cfg.get_filename_database()
        self.__load_database()

    def __get_news(self):
        """()-> list(Topic)
        This method return all news in linux.org.ru"""
        req1 = requests.get(self.__server_name + '/news/')
        data = bs4.BeautifulSoup(req1.text, "html.parser")
        all_news = data.select('.news')
        result = []
        threads = []

        for news_elem in all_news:
            tmp = str(news_elem.select("a")[0])

            ind0 = tmp.find('"')
            ind1 = tmp.find('"', ind0 + 1)
            link = self.__server_name + tmp[ind0 + 1:ind1]

            ind0 = tmp.find('">')
            ind1 = tmp.find("</a>")
            title = tmp[ind0 + 2:ind1]

            threads.append(urlreader.TopicFromTracker(title, link))
            threads[-1].start()

        for elem in threads:
            result.append(elem.join())

        return result

    def __save_database(self):
        """() -> None
        This method save database LOR news in filesystem"""
        try:
            with open(self.__filename, "wb") as file1:
                pickle.dump(self.__lor_news, file1)
        except FileNotFoundError:
            logging.error("Not found directory or file to save news databases. Create full path to saved file")
            os.makedirs(Cfg.get_path_to_dir_database())
            self.__save_database()

    def __load_database(self):
        """() -> ()
        This method load old database LOR news from filesystem"""
        try:
            with open(self.__filename, "rb") as file1:
                self.__lor_news = pickle.load(file1)
        except FileNotFoundError:
            logging.error("Not found correct saved news database. Create new database")
            self.__lor_news = []

    def get_news(self):
        """() -> None
        This method insert new LOR news messages to database"""
        tmp = self.__get_news()
        for elem in tmp:
            if elem not in self.__lor_news:
                self.__lor_news.append(elem)

        self.__lor_news = self.__lor_news[:Cfg.get_max_len_stack()]
        self.__save_database()
        if len(self.__lor_news) > 0:
            self.__current_index = 0

    def __next__(self):
        if self.__current_index < len(self.__lor_news):
            self.__current_index += 1
            return self.__lor_news[self.__current_index - 1]
        else:
            self.__current_index = 0
            raise StopIteration

    def __iter__(self):
        return self

    @staticmethod
    def resource_name():
        return "Linux.Org.Ru (LOR) News"
