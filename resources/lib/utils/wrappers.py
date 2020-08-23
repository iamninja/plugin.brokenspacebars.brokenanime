# -*- coding: utf-8 -*-

from xbmcgui import DialogProgress

class Progress:
    def __init__(self, title, prefix_string):
        self.__dialog = DialogProgress()
        self.__prefix_string = prefix_string
        self.__dialog.create(title)
        self.count = 0
        self.max = 0

    def update(self, percent, text):
        new_text = str(self.__prefix_string) + str(text)
        return self.__dialog.update(percent, new_text)

    def iscanceled(self):
        return self.__dialog.iscanceled()

    def close(self):
        return self.__dialog.close()

    def addCount(self):
        self.count += 1

    def getPercent(self):
        if self.max != 0:
            return int((self.count / self.max) * 100)
        else:
            return 0

    def getText(self):
        return str(self.count) + "/" + str(self.max)

    def easyUpdate(self, extraInfo = None):
        self.addCount()
        if extraInfo != None:
            self.update(self.getPercent(),
                self.getText() + "[CR]" + str(extraInfo))
        else:
            self.update(self.getPercent(), self.getText())