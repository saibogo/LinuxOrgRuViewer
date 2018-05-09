import tkinter as tk
from lor_lib.parser.config import Config as Cfg


class LoggingWindowParam(object):
    """
    Create window to select param logging file
    """

    def __init__(self):
        def submit():
            Cfg.set_backup_count(val_bac.get())
            Cfg.update_handler()
            win.destroy()

        gui_cfg = {"bg": Cfg.get_bg_color(),
                   "fg": Cfg.get_font_label_color(),
                   "font": Cfg.get_font_label()}
        frame_cfg = {"bg": Cfg.get_bg_color(),
                     "relief": tk.SUNKEN,
                     "bd": 2}

        win = tk.Toplevel()
        win.configure(background=Cfg.get_bg_color())
        win.resizable(False, False)

        frame1 = tk.Frame(win,
                          cnf=frame_cfg)
        label1 = tk.Label(frame1,
                          cnf=gui_cfg,
                          text="Select the number of backups:")
        label1.pack(fill=tk.BOTH)
        val_bac = tk.IntVar()
        frame2 = tk.Frame(win,
                          cnf=frame_cfg)
        ent1 = tk.Entry(frame2,
                        cnf=gui_cfg,
                        justify=tk.CENTER,
                        textvariable=val_bac)
        val_bac.set(Cfg.get_backup_count())
        ent1.pack(fill=tk.BOTH)
        frame3 = tk.Frame(win,
                          cnf=frame_cfg)
        but1 = tk.Button(frame3,
                         cnf=gui_cfg,
                         text="Submit",
                         command=submit)
        but1.pack(fill=tk.BOTH)
        frame1.pack(fill=tk.BOTH)
        frame2.pack(fill=tk.BOTH)
        frame3.pack(fill=tk.BOTH)
        win.mainloop()
