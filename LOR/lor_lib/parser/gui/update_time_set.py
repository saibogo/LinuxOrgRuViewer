import tkinter as tk
from lor_lib.parser.config import Config as Cfg
from lor_lib.parser.constants import *


class UpdateTimeWindow(object):

    def __init__(self):
        ut_window = tk.Toplevel()
        gui_cfg = {"bg": Cfg.get_bg_color(),
                   "fg": Cfg.get_font_label_color(),
                   "font": Cfg.get_font_label()}

        def close_window():
            Cfg.set_time_to_update(v.get())
            ut_window.destroy()

        ut_window.title("Setting time updates")
        ut_window.resizable(False, False)
        frame = tk.Frame(ut_window,
                         bg=Cfg.get_bg_color())
        frame.pack()
        tk.Label(frame, text="Select time:",
                 cnf=gui_cfg).pack()
        v = tk.IntVar()

        for txt, num in update_intervals():
            tk.Radiobutton(frame,
                           text=txt,
                           variable=v,
                           value=num,
                           cnf=gui_cfg).pack()

        v.set(5 * 60 * 1000)
        bt = tk.Button(ut_window,
                       text="Submit",
                       cnf=gui_cfg,
                       command=close_window)
        bt.pack()
        ut_window.mainloop()
