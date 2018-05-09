class Topic:
    """
    Create new Topic element include title, link and text message
    """
    __title = None
    __link = None
    __text = None

    def __init__(self, title, link, text):
        self.__title = title if type(title) == str else ""
        self.__link = link if type(link) == str else ""
        self.__text = text if type(text) == str else ""

    def title(self):
        return self.__title

    def link(self):
        return self.__link

    def text(self):
        return self.__text

    def __eq__(self, other):
        return self.__link == other.link()

    def __ne__(self, other):
        return self.__link != other.link()
