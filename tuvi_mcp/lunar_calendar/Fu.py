# -*- coding: utf-8 -*-


class Fu:
    """
    San Fu (3 ten-day periods of summer)
    <p>Counting from the 3rd Geng day after Summer Solstice: first Fu is 10 days, middle Fu is 10 or 20 days, last Fu is 10 days. When there are 4 Geng days between Summer Solstice and Start of Autumn, middle Fu is 10 days; when 5 Geng days, it is 20 days.</p>
    """

    def __init__(self, name, index):
        self.__name = name
        self.__index = index

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getIndex(self):
        return self.__index

    def setIndex(self, index):
        self.__index = index

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.__name

    def toFullString(self):
        return "%s ngày %d" % (self.__name, self.__index)
