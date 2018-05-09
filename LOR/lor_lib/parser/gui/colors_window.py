import tkinter as tk
import lor_lib.parser.config as cfg
from tkinter.colorchooser import *
from lor_lib.parser.gui.signals import GuiSignals


class SettingsColorWindows(object):
    """
    Create window setting colors for elements GUI
    """

    def __init__(self):
        win = tk.Toplevel()
        win.title("Set colors font and background")
        win.resizable(False, False)
        gui_cfg = {"bg": cfg.Config.get_bg_color(),
                   "fg": cfg.Config.get_font_label_color(),
                   "font": cfg.Config.get_font_label()}

        frame = tk.Frame(win,
                         bg=cfg.Config.get_bg_color(),
                         relief=tk.SUNKEN,
                         bd=2)
        btn1 = tk.Button(frame,
                         cnf=gui_cfg,
                         text="Set font color",
                         command=SettingsColorWindows.font_color)
        btn2 = tk.Button(frame,
                         text="Color backgrounds",
                         cnf=gui_cfg,
                         command=SettingsColorWindows.bg_color)
        btn3 = tk.Button(frame,
                         text="News background",
                         cnf=gui_cfg,
                         command=SettingsColorWindows.tool_tip_bg)

        btn4 = tk.Button(frame,
                         text="News text color",
                         cnf=gui_cfg,
                         command=SettingsColorWindows.tool_tip_font_color)

        btn1.pack(fill=tk.BOTH)
        btn2.pack(fill=tk.BOTH)
        btn3.pack(fill=tk.BOTH)
        btn4.pack(fill=tk.BOTH)
        frame.pack()
        win.mainloop()

    @staticmethod
    def font_color():
        """()->() Set color fonts to all elements include text in main window"""
        try:
            rgb, h = askcolor(color=cfg.Config.get_font_label_color())
            cfg.Config.set_font_color(h)
            GuiSignals.set_update_gui_menu_flag()
        except TypeError:
            pass

    @staticmethod
    def bg_color():
        """()->() Set color background to all elements GUI main window"""
        try:
            rgb, h = askcolor(color=cfg.Config.get_bg_color())
            cfg.Config.set_bg_color(h)
            GuiSignals.set_update_gui_menu_flag()
        except TypeError:
            pass

    @staticmethod
    def tool_tip_bg():
        """()->() Set backgrounds color for tooltip window"""
        try:
            rgb, h = askcolor(color=cfg.Config.get_tool_tip_bg())
            cfg.Config.set_tool_tip_bg(h)
        except TypeError:
            pass

    @staticmethod
    def tool_tip_font_color():
        """()->() Set fonts color to text in tooltip window"""
        try:
            rgb, h = askcolor(color=cfg.Config.get_tool_tip_font_color())
            cfg.Config.set_tool_tip_font_color(h)
        except TypeError:
            pass
