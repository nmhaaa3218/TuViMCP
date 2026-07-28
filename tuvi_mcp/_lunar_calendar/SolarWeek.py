# -*- coding: utf-8 -*-
from math import ceil

from . import Solar
from .util import SolarUtil


class SolarWeek:
    """
    Solar week
    """

    def __init__(self, year, month, day, start):
        """
        Initialize by year, month, day
        :param year: Year
        :param month: Month, 1 to 12
        :param day: Day, 1 to 31
        :param start: Day of week as start, 1234560 for Monday to Sunday
        """
        self.__year = year
        self.__month = month
        self.__day = day
        self.__start = start

    @staticmethod
    def fromDate(date, start):
        return SolarWeek(date.year, date.month, date.day, start)

    @staticmethod
    def fromYmd(year, month, day, start):
        return SolarWeek(year, month, day, start)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

    def getStart(self):
        return self.__start

    def toString(self):
        return "%d.%d.%d" % (self.__year, self.__month, self.getIndex())

    def toFullString(self):
        return "Tuần %d tháng %d năm %d" % (self.getIndex(), self.__month, self.__year)

    def __str__(self):
        return self.toString()

    def getIndex(self):
        """
        Get which week of the month the current date falls in
        :return: Week index, starting from 1
        """
        offset = Solar.fromYmd(self.__year, self.__month, 1).getWeek() - self.__start
        if offset < 0:
            offset += 7
        return int(ceil((self.__day + offset) * 1.0 / 7))

    def getIndexInYear(self):
        """
        Get which week of the year the current date falls in
        :return: Week index, starting from 1
        """
        offset = Solar.fromYmd(self.__year, 1, 1).getWeek() - self.__start
        if offset < 0:
            offset += 7
        return int(ceil((SolarUtil.getDaysInYear(self.__year, self.__month, self.__day) + offset) * 1.0 / 7))

    def getFirstDay(self):
        """
        Get first day of this week (may cross month)
        :return: First day's solar date
        """
        solar = Solar.fromYmd(self.__year, self.__month, self.__day)
        prev = solar.getWeek() - self.__start
        if prev < 0:
            prev += 7
        return solar.next(-prev)

    def getFirstDayInMonth(self):
        """
        Get first day of this week (current month only)
        :return: First day's solar date
        """
        for day in self.getDays():
            if self.__month == day.getMonth():
                return day
        return None

    def getDays(self):
        """
        Get solar dates of this week (may cross month)
        :return: List of solar dates
        """
        days = []
        first = self.getFirstDay()
        days.append(first)
        for i in range(1, 7):
            days.append(first.next(i))
        return days

    def getDaysInMonth(self):
        """
        Get solar dates of this week (current month only)
        :return: List of solar dates (current month only)
        """
        days = []
        for day in self.getDays():
            if self.__month == day.getMonth():
                days.append(day)
        return days

    def next(self, weeks, separate_month):
        """
        Week shift
        :param weeks: Weeks to shift, negative for backward
        :param separate_month: Whether to calculate per month separately
        :return: Shifted solar week
        """
        if 0 == weeks:
            return SolarWeek.fromYmd(self.__year, self.__month, self.__day, self.__start)
        solar = Solar.fromYmd(self.__year, self.__month, self.__day)
        if separate_month:
            n = weeks
            week = SolarWeek.fromYmd(solar.getYear(), solar.getMonth(), solar.getDay(), self.__start)
            month = self.__month
            plus = n > 0
            days = 7 if plus else -7
            while 0 != n:
                solar = solar.next(days)
                week = SolarWeek.fromYmd(solar.getYear(), solar.getMonth(), solar.getDay(), self.__start)
                week_month = week.getMonth()
                if month != week_month:
                    index = week.getIndex()
                    if plus:
                        if 1 == index:
                            first_day = week.getFirstDay()
                            week = SolarWeek.fromYmd(first_day.getYear(), first_day.getMonth(), first_day.getDay(), self.__start)
                            week_month = week.getMonth()
                        else:
                            solar = Solar.fromYmd(week.getYear(), week.getMonth(), 1)
                            week = SolarWeek.fromYmd(solar.getYear(), solar.getMonth(), solar.getDay(), self.__start)
                    else:
                        if SolarUtil.getWeeksOfMonth(week.getYear(), week.getMonth(), self.__start) == index:
                            last_day = week.getFirstDay().next(6)
                            week = SolarWeek.fromYmd(last_day.getYear(), last_day.getMonth(), last_day.getDay(), self.__start)
                            week_month = week.getMonth()
                        else:
                            solar = Solar.fromYmd(week.getYear(), week.getMonth(), SolarUtil.getDaysOfMonth(week.getYear(), week.getMonth()))
                            week = SolarWeek.fromYmd(solar.getYear(), solar.getMonth(), solar.getDay(), self.__start)
                    month = week_month
                n -= 1 if plus else -1
            return week
        else:
            solar = solar.next(weeks * 7)
            return SolarWeek.fromYmd(solar.getYear(), solar.getMonth(), solar.getDay(), self.__start)
