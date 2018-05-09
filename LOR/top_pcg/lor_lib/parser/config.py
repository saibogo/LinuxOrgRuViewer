import logging
import os
from lor_lib import parser
from logging.handlers import RotatingFileHandler
from lor_lib.parser.dict_to_file import *


class Config:
    __instance = None
    __max_len_news_stack = None
    __file_to_save_news = None
    __filename = "all_LOR_news.save"
    __path_to_database_dir = "~/.config/LOR/"
    __config_filename = "config"
    __bg_color = "black"
    __font_label = ("Arial", 10, "bold italic")
    __font_label_color = '#BABDB6'
    __time_to_update = 10 * 60 * 1000
    __logging_filename = "lorviewer.log"
    __tool_tip_bg = '#FFEBCD'
    __tool_tip_font_color = "#8B7765"
    __max_size_logfile = 1024 * 1024
    __wait_time_tooltip = 500
    __wraplength_tool_tip = 300
    __backUpCount = 2

    def __init__(self):
        """This class is pattern singleton
        Config load in filesystem. if not or version not equal to version in packet parser
        create new config"""
        if Config.__instance is None:
            Config.__instance = True
            tmp = Config.__load_config()
            if len(tmp) == 0 or \
                    version() not in tmp.keys() or \
                    tmp[version()] != parser.__version__:
                Config.logging_base_config()
                logging.info("No correct config file. Create new config file.")
                Config.__max_len_news_stack = 15
            else:
                try:
                    Config.__max_len_news_stack = tmp[max_len_new_stack()]
                    Config.__file_to_save_news = tmp[file_to_save_news()]
                    Config.__filename = tmp[filename()]
                    Config.__path_to_database_dir = tmp[path_to_database_dir()]
                    Config.__config_filename = tmp[config_filename()]
                    Config.__bg_color = tmp[bg_color()]
                    Config.__font_label = tmp[font_label()]
                    Config.__font_label_color = tmp[font_label_color()]
                    Config.__time_to_update = tmp[time_to_update()]
                    Config.__logging_filename = tmp[logging_filename()]
                    Config.__tool_tip_bg = tmp[tool_tip_bg()]
                    Config.__tool_tip_font_color = tmp[tool_tip_font_color()]
                    Config.__max_size_logfile = tmp[max_size_log_file()]
                    Config.__wait_time_tooltip = tmp[waittime_tool_tip()]
                    Config.__wraplength_tool_tip = tmp[wraplength_tool_tip()]
                    Config.__backUpCount = tmp[backup_count()]
                    Config.logging_base_config()
                except KeyError:
                    Config.logging_base_config()
                    logging.error("Error load config file. Create new config file")
                    Config.__max_len_news_stack = 15

            Config.__file_to_save_news = os.path.expanduser(
                Config.__path_to_database_dir + Config.__filename)
            logging.info("Lor Viewer version " + str(parser.__version__) + " started")
            Config.__save_config()
        else:
            pass

    @staticmethod
    def get_max_len_stack():
        """This method return max len news databases"""
        return Config.__max_len_news_stack

    @staticmethod
    def get_filename_database():
        """() -> str. This method return name of file, contains news database"""
        return Config.__file_to_save_news

    @staticmethod
    def get_path_to_dir_database():
        """() -> str. This method return path to dir, contains configfile and news databases"""
        return os.path.expanduser(Config.__path_to_database_dir)

    @staticmethod
    def __save_config():
        """() -> (). Save current config"""
        tmp = {version(): parser.__version__,
               max_len_new_stack(): Config.__max_len_news_stack,
               file_to_save_news(): Config.__file_to_save_news,
               filename(): Config.__filename,
               path_to_database_dir(): Config.__path_to_database_dir,
               config_filename(): Config.__config_filename,
               bg_color(): Config.__bg_color,
               font_label(): Config.__font_label,
               font_label_color(): Config.__font_label_color,
               time_to_update(): Config.__time_to_update,
               logging_filename(): Config.__logging_filename,
               tool_tip_bg(): Config.__tool_tip_bg,
               tool_tip_font_color(): Config.__tool_tip_font_color,
               max_size_log_file(): Config.__max_size_logfile,
               waittime_tool_tip(): Config.__wait_time_tooltip,
               wraplength_tool_tip(): Config.__wraplength_tool_tip,
               backup_count(): Config.__backUpCount}
        save_config_name = os.path.expanduser(Config.__path_to_database_dir + Config.__config_filename)
        if save_dict(tmp, save_config_name):
            logging.info("Saved current config to file " + save_config_name)
        else:
            logging.error("Not found directory or file to save config file. Create full path to new config file")
            os.makedirs(Config.__path_to_database_dir)
            Config.__save_config()

    @staticmethod
    def __load_config():
        """()->dict(str, any) This method try load old config file or return empty dict"""
        save_config_name = os.path.expanduser(Config.__path_to_database_dir + Config.__config_filename)
        tmp = load_dict(save_config_name)
        if tmp is None:
            tmp = {}
            try:
                os.makedirs(os.path.expanduser(Config.__path_to_database_dir))
            except FileExistsError:
                pass
        return tmp

    @staticmethod
    def get_bg_color():
        return Config.__bg_color

    @staticmethod
    def get_font_label():
        return Config.__font_label

    @staticmethod
    def get_font_label_color():
        return Config.__font_label_color

    @staticmethod
    def get_time_to_update():
        return Config.__time_to_update

    @staticmethod
    def get_logging_filename():
        return os.path.expanduser(Config.__path_to_database_dir + Config.__logging_filename)

    @staticmethod
    def logging_base_config():
        logging.basicConfig(filename=Config.get_logging_filename(),
                            level=logging.DEBUG,
                            format="%(asctime)s : %(levelname)s : %(message)s")
        log = logging.getLogger()
        handler = RotatingFileHandler(Config.get_logging_filename(),
                                      maxBytes=Config.__max_size_logfile,
                                      backupCount=2)
        log.addHandler(handler)

    @staticmethod
    def update_handler():
        log = logging.getLogger()
        for hnd in log.handlers:
            log.removeHandler(hnd)
        Config.logging_base_config()
        Config.__save_config()

    @staticmethod
    def get_tool_tip_bg():
        return Config.__tool_tip_bg

    @staticmethod
    def get_tool_tip_font_color():
        return Config.__tool_tip_font_color

    @staticmethod
    def set_time_to_update(t):
        Config.__time_to_update = t
        logging.info("Select update time in " + str(t) + "ms.")
        Config.__save_config()

    @staticmethod
    def set_font_color(col):
        Config.__font_label_color = col
        logging.info("Select font color " + col)
        Config.__save_config()

    @staticmethod
    def set_bg_color(col):
        Config.__bg_color = col
        logging.info("Select text label and button background color " + col)
        Config.__save_config()

    @staticmethod
    def set_tool_tip_bg(col):
        Config.__tool_tip_bg = col
        logging.info("Select tooltip background color " + col)
        Config.__save_config()

    @staticmethod
    def set_tool_tip_font_color(col):
        Config.__tool_tip_font_color = col
        logging.info("Select tooltip font color " + col)
        Config.__save_config()

    @staticmethod
    def set_max_len_news_stack(ln):
        Config.__max_len_news_stack = ln
        logging.info("Select len news stack is " + str(ln) + " elements")
        Config.__save_config()

    @staticmethod
    def get_waittime_tooltip():
        return Config.__wait_time_tooltip

    @staticmethod
    def get_wraplength_tool_tip():
        return Config.__wraplength_tool_tip

    @staticmethod
    def set_font_label(name, size, ext_param=""):
        Config.__font_label = (name, int(size)) if ext_param == "" else (name, int(size), ext_param)

    @staticmethod
    def get_backup_count():
        return Config.__backUpCount

    @staticmethod
    def set_backup_count(n):
        Config.__backUpCount = n
