# -*- coding: utf-8 -*-

from . import SolarMonth


class SolarYear:
    """
    Solar year
    """

    MONTH_COUNT = 12

    def __init__(self, year):
        self.__year = year

    @staticmethod
    def fromDate(date):
        return SolarYear(date.year)

    @staticmethod
    def fromYear(year):
        return SolarYear(year)

    def getYear(self):
        return self.__year

    def toString(self):
        return str(self.__year)

    def toFullString(self):
        return "Năm %d" % self.__year

    def __str__(self):
        return self.toString()

    def getMonths(self):
        """
        Get solar months of this year
        :return: List of solar months
        """
        months = []
        m = SolarMonth.fromYm(self.__year, 1)
        months.append(m)
        for i in range(1, SolarYear.MONTH_COUNT):
            months.append(m.next(i))
        return months

    def next(self, years):
        """
        Get solar year pushed forward by years, use negative for backward
        :param years: Years
        :return: Solar year
        """
        return SolarYear.fromYear(self.__year + years)
