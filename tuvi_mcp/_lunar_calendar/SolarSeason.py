# -*- coding: utf-8 -*-
from math import ceil

from . import SolarMonth


class SolarSeason:
    """
    Solar season (quarter)
    """

    MONTH_COUNT = 3

    def __init__(self, year, month):
        self.__year = year
        self.__month = month

    @staticmethod
    def fromDate(date):
        return SolarSeason(date.year, date.month)

    @staticmethod
    def fromYm(year, month):
        return SolarSeason(year, month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def toString(self):
        return "%d.%d" % (self.__year, self.getIndex())

    def toFullString(self):
        return "Quý %d năm %d" % (self.getIndex(), self.__year)

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        Get which quarter the month falls in
        :return: Quarter index, starting from 1
        """
        return int(ceil(self.__month * 1.0 / SolarSeason.MONTH_COUNT))

    def getMonths(self):
        """
        Get solar months of this quarter
        :return: List of solar months
        """
        months = []
        index = self.getIndex() - 1
        for i in range(0, SolarSeason.MONTH_COUNT):
            months.append(SolarMonth.fromYm(self.__year, SolarSeason.MONTH_COUNT * index + i + 1))
        return months

    def next(self, seasons):
        """
        Quarter shift
        :param seasons: Seasons to shift, negative for backward
        :return: Shifted quarter
        """
        m = SolarMonth.fromYm(self.__year, self.__month).next(SolarSeason.MONTH_COUNT * seasons)
        return SolarSeason.fromYm(m.getYear(), m.getMonth())
