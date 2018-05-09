import tkinter as tk
from lor_lib.parser.config import Config as Cfg


class LenNewsWindow(object):
    """
    Create window select len list include topicks or news
    """

    def __init__(self):
        def submit():
            Cfg.set_max_len_news_stack(val.get())
            win.destroy()

        gui_cfg = {"bg": Cfg.get_bg_color(),
                   "fg": Cfg.get_font_label_color(),
                   "font": Cfg.get_font_label()}
        win = tk.Toplevel()
        win.title("Select max news in frame")
        win.resizable(False, False)
        frame = tk.Frame(win,
                         bg=Cfg.get_bg_color(),
                         bd=2,
                         relief=tk.SUNKEN)
        frame.pack()
        val = tk.IntVar()
        tk.Label(frame,
                 text="Select new value to maximum news in frame:",
                 cnf=gui_cfg).pack(fill=tk.BOTH)

        tk.Entry(frame,
                 justify=tk.CENTER,
                 textvariable=val,
                 cnf=gui_cfg).pack(fill=tk.BOTH)
        val.set(Cfg.get_max_len_stack())
        tk.Button(frame,
                  text="Submit",
                  command=submit,
                  cnf=gui_cfg).pack(fill=tk.BOTH)

        win.mainloop()
