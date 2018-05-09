import tkinter as tk
from lor_lib.parser.config import Config as Cfg
from lor_lib import parser


class AboutWindow(object):
    """
    Create window include main information to program

    """

    def __init__(self):
        a_window = tk.Toplevel()
        a_window.title("About LOR Viewer")
        frame = tk.Frame(a_window, bg=Cfg.get_bg_color())
        frame.pack()
        info = "\n" + "Version: " + str(parser.__version__) + "\n" + \
               "Author: " + str(parser.__author__) + "\n" + \
               str(parser.__email__) + "\n" + \
               "License: " + str(parser.__copyright__) + "\n"
        label = tk.Label(frame, text=info,
                         bg=Cfg.get_bg_color(),
                         fg=Cfg.get_font_label_color())
        label.pack()
