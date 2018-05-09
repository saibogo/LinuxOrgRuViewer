from lor_lib.parser.config import Config as Cfg
from lor_lib.parser.LOR_news_parser import LorNewsParser as LOR_news
from tkinter import *
import webbrowser
import logging
from lor_lib.parser.constants import *
import lor_lib.parser.gui.create_tool_tip as ctp
import lor_lib.parser.gui.about_window as about_window
import lor_lib.parser.gui.update_time_set as ut_window
import lor_lib.parser.gui.colors_window as color_win
import lor_lib.parser.gui.len_news_window as len_window
from lor_lib.parser.LOR_tracker_parser import LorTrackerParser as LOR_track
from lor_lib.parser.gui.font_window import SelectFontWindow
from lor_lib.parser.gui.logging_window import LoggingWindowParam
from lor_lib.parser.gui.signals import GuiSignals


class MainGui:
    __instance = None
    __cfg = None
    __lor = None
    __root = None
    __main_frames = []
    __labels = []
    __ttp = []
    __active_frame = news()
    __gui_config = {}
    __frame_config = {}
    __menu = None
    __current_after = None

    def title_button(self, s):
        return s.upper() if s == self.__active_frame else s[0].upper() + s[1:]

    def __close_main_window(self):
        logging.info("Terminate run LOR viewer")
        self.__root.destroy()

    def __init__(self):
        if MainGui.__instance is None:
            MainGui.__instance = self
            self.__cfg = Cfg()
            if self.__active_frame == news():
                self.__lor = LOR_news()
            elif self.__active_frame == tracker():
                self.__lor = LOR_track()
            else:
                pass

            self.create_gui_config()
            self.create_frame_config()

            self.__root = Tk()
            self.__root.title(self.__lor.resource_name())
            self.__root.resizable(False, False)

            self.create_menu()

            self.__print_news()
            self.__root.protocol("WM_DELETE_WINDOW", self.__close_main_window)
            self.__root.mainloop()
        else:
            pass

    def __load_news(self):
        if self.__active_frame == news():
            return self.__lor.get_news()
        elif self.__active_frame == tracker():
            return self.__lor.get_tracker()
        else:
            pass

    def __max_len_label(self):
        max_chars = max(len(new_top.title()) for new_top in self.__lor)
        max_chars = min_width() if max_chars < min_width() else \
            (max_chars % max_width() + max_width() if max_chars > max_width() else max_chars)
        return max_chars

    @staticmethod
    def __open_link(link):
        logging.info("Open new link in webbrowser : " + str(link))
        webbrowser.open_new_tab(link)

    def __print_news(self):
        if self.__active_frame == news():
            logging.info("Update news database")
        elif self.__active_frame == tracker():
            logging.info("Update tracking info")
        else:
            pass

        def __leftclick(s):
            tmp = s.widget.get(1.0, END)
            tmp = tmp[:len(tmp) - 1]
            for news_top in self.__lor:
                if news_top.title() == tmp:
                    webbrowser.open_new_tab(news_top.link())
                    break

        self.__root.configure(background=Cfg.get_bg_color())
        self.__load_news()
        self.__main_frames = []
        self.__labels = []
        self.__ttp = []
        mll = self.__max_len_label()
        self.__main_frames.append(Frame(self.__root,
                                        cnf=self.__frame_config))

        frame_left = Frame(self.__main_frames[0],
                           cnf=self.__frame_config)
        frame_right = Frame(self.__main_frames[0],
                            cnf=self.__frame_config)
        btn1 = Button(frame_left,
                      text=self.title_button(news()),
                      command=self.__set_news_frame,
                      cnf=self.__gui_config)
        btn2 = Button(frame_right,
                      text=self.title_button(tracker()),
                      command=self.__set_tracker_frame,
                      cnf=self.__gui_config)
        frame_left.pack(fill=BOTH, side=LEFT)
        frame_right.pack(fill=BOTH, side=LEFT)
        btn1.pack(fill=BOTH)
        btn2.pack(fill=BOTH)

        for new_top in self.__lor:
            self.__main_frames.append(Frame(self.__root,
                                            cnf=self.__frame_config))
            self.__labels.append(Text(self.__main_frames[-1],
                                      width=mll,
                                      height=2,
                                      cursor="hand2"))
            self.__labels[-1].configure(cnf=self.__gui_config)
            self.__labels[-1].tag_configure(centred(), justify="center")
            self.__labels[-1].insert(1.0, new_top.title())
            self.__labels[-1].tag_add(centred(), 1.0, END)
            self.__labels[-1].bind('<Button-1>', __leftclick)
            self.__ttp.append(ctp.CreateToolTip(self.__labels[-1], new_top.text()))

        for frame in self.__main_frames:
            frame.pack()
        for label in self.__labels:
            label.pack()
        self.__current_after = self.__root.after(self.__cfg.get_time_to_update(), self.__update)

    def __update(self):
        if not (self.__current_after is None):
            self.__root.after_cancel(self.__current_after)
        for frame in self.__main_frames:
            frame.destroy()
        self.create_frame_config()
        self.create_gui_config()
        if GuiSignals.update_gui_menu_flag():
            self.__menu.destroy()
            self.create_menu()
            GuiSignals.set_update_gui_menu_flag(False)
        self.__print_news()

    def __set_news_frame(self):
        self.__active_frame = news()
        self.__root.title(LOR_news.resource_name())
        self.__lor = LOR_news()
        self.__update()

    def __set_tracker_frame(self):
        self.__active_frame = tracker()
        self.__root.title(LOR_track.resource_name())
        self.__lor = LOR_track()
        self.__update()

    def create_gui_config(self):
        self.__gui_config = {"bg": Cfg.get_bg_color(),
                             "fg": Cfg.get_font_label_color(),
                             "font": Cfg.get_font_label()}

    def create_menu(self):
        self.__menu = Menu(self.__root,
                           font=Cfg.get_font_label(),
                           bg=Cfg.get_bg_color(),
                           fg=Cfg.get_font_label_color())
        self.__root.config(menu=self.__menu)

        action_menu = Menu(self.__menu)
        action_menu.configure(cnf=self.__gui_config)
        self.__menu.add_cascade(label="Action", menu=action_menu)
        action_menu.add_command(label="Update", command=self.__update)
        action_menu.add_separator()
        action_menu.add_command(label="Exit", command=self.__close_main_window)

        settings_menu = Menu(self.__menu)
        settings_menu.configure(cnf=self.__gui_config)
        self.__menu.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Update interval", command=ut_window.UpdateTimeWindow)
        settings_menu.add_command(label="Max news in frame", command=len_window.LenNewsWindow)
        settings_menu.add_separator()
        settings_menu.add_command(label="Colors", command=color_win.SettingsColorWindows)
        settings_menu.add_command(label="Fonts", command=SelectFontWindow)
        settings_menu.add_separator()
        settings_menu.add_command(label="Logfile", command=LoggingWindowParam)

        help_menu = Menu(self.__menu)
        help_menu.configure(cnf=self.__gui_config)
        self.__menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=about_window.AboutWindow)

    def create_frame_config(self):
        self.__frame_config = {"bg": Cfg.get_bg_color(),
                               "bd": 2,
                               "relief": SUNKEN}
