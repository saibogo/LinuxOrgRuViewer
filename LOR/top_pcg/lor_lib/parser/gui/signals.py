class GuiSignals:
    __update_gui_menu = False
    __instance = None

    def __init__(self):
        if GuiSignals.__instance is None:
            GuiSignals.__update_gui_menu = False
            GuiSignals.__instance = self
        else:
            pass

    @staticmethod
    def update_gui_menu_flag():
        return GuiSignals.__update_gui_menu

    @staticmethod
    def set_update_gui_menu_flag(flag=True):
        GuiSignals.__update_gui_menu = flag
