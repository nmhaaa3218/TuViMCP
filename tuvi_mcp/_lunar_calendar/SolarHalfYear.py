# -*- coding: utf-8 -*-
from math import ceil

from . import SolarMonth


class SolarHalfYear:
    """
    Solar half year
    """

    MONTH_COUNT = 6

    def __init__(self, year, month):
        self.__year = year
        self.__month = month

    @staticmethod
    def fromDate(date):
        return SolarHalfYear(date.year, date.month)

    @staticmethod
    def fromYm(year, month):
        return SolarHalfYear(year, month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def toString(self):
        return "%d.%d" % (self.__year, self.getIndex())

    def toFullString(self):
        return "Năm %s nửa %s năm" % (self.__year, ("đầu" if 1 == self.getIndex() else "cuối"))

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        Get which half of the year the month falls in
        :return: Half year index, starting from 1
        """
        return int(ceil(self.__month * 1.0 / SolarHalfYear.MONTH_COUNT))

    def getMonths(self):
        """
        Get solar months of this half year
        :return: List of solar months
        """
        months = []
        index = self.getIndex() - 1
        for i in range(0, SolarHalfYear.MONTH_COUNT):
            months.append(SolarMonth.fromYm(self.__year, SolarHalfYear.MONTH_COUNT * index + i + 1))
        return months

    def next(self, half_years):
        """
        Half year shift
        :param half_years: Half years to shift, negative for backward
        :return: Shifted half year
        """
        m = SolarMonth.fromYm(self.__year, self.__month).next(SolarHalfYear.MONTH_COUNT * half_years)
        return SolarHalfYear.fromYm(m.getYear(), m.getMonth())
