import tkinter as tk
import logging
from lor_lib.parser.constants import *
from lor_lib.parser.config import Config as Cfg


# noinspection PyUnusedLocal,PyUnusedLocal
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = Cfg.get_waittime_tooltip()  # miliseconds
        self.wraplength = Cfg.get_wraplength_tool_tip()  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        x = y = 0
        try:
            x, y, cx, cy = self.widget.bbox("insert")
        except TypeError:
            logging.error("Type Error Exception. Tkinter ToolTip object not iterable")

        try:
            x += self.widget.winfo_rootx() + delta_x()
            y += self.widget.winfo_rooty() + delta_y()
            self.tw = tk.Toplevel(self.widget)
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(self.tw,
                             text=self.text,
                             justify='left',
                             background=Cfg.get_tool_tip_bg(),
                             relief='solid',
                             borderwidth=1,
                             wraplength=self.wraplength,
                             fg=Cfg.get_tool_tip_font_color(),
                             font=Cfg.get_font_label())
            label.pack(ipadx=1)
        except tk.TclError:
            logging.error("Except in create tooltip window")

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
