from tkFontChooser import askfont
from lor_lib.parser.config import Config as Cfg
import logging
from lor_lib.parser.gui.signals import GuiSignals


class SelectFontWindow(object):
    """
    Create a window include font to GUI
    """

    def __init__(self):
        font = askfont()
        if font:
            param = ['bold' if font['weight'] == 'bold' else "",
                     'italic' if font['slant'] == 'italic' else "",
                     'underline' if font['underline'] != 0 else "",
                     'overstrike' if font['overstrike'] != 0 else ""]
            Cfg.set_font_label(font["family"], font["size"], " ".join(param))
            GuiSignals.set_update_gui_menu_flag()
        else:
            logging.error("Error in window set font")
