# -*- coding: utf-8 -*-

from . import Solar, SolarWeek
from .util import SolarUtil


class SolarMonth:
    """
    Solar month
    """

    def __init__(self, year, month):
        self.__year = year
        self.__month = month

    @staticmethod
    def fromDate(date):
        return SolarMonth(date.year, date.month)

    @staticmethod
    def fromYm(year: int, month: int):
        return SolarMonth(year, month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def toString(self):
        return "%d-%d" % (self.__year, self.__month)

    def toFullString(self):
        return "Tháng %d năm %d" % (self.__month, self.__year)

    def __str__(self):
        return self.toString()

    def getDays(self):
        """
        Get solar dates of this month
        :return: List of solar dates
        """
        days = []
        d = Solar.fromYmd(self.__year, self.__month, 1)
        days.append(d)
        for i in range(1, SolarUtil.getDaysOfMonth(self.__year, self.__month)):
            days.append(d.next(i))
        return days

    def getWeeks(self, start):
        """
        Get solar date list of this month
        :param start: Day of week as start, 1234560 for Monday to Sunday
        :return: List of solar dates
        """
        weeks = []
        week = SolarWeek.fromYmd(self.__year, self.__month, 1, start)
        while True:
            weeks.append(week)
            week = week.next(1, False)
            first_day = week.getFirstDay()
            if first_day.getYear() > self.__year or first_day.getMonth() > self.__month:
                break
        return weeks

    def next(self, months):
        """
        Get solar month pushed forward by months, use negative for backward
        :param months: Months
        :return: Solar month
        """
        n = 1
        if months < 0:
            n = -1
        m = abs(months)
        y = self.__year + int(m / 12) * n
        m = self.__month + m % 12 * n
        if m > 12:
            m -= 12
            y += 1
        elif m < 1:
            m += 12
            y -= 1
        return SolarMonth.fromYm(y, m)
