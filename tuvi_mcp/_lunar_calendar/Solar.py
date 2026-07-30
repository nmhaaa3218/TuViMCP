# -*- coding: utf-8 -*-
from datetime import datetime
from math import ceil

from .util import LunarUtil, SolarUtil


class Solar:
    """
    Solar date
    """

    # Julian day number for year 2000 (2000-1-1 12:00:00 UTC)
    J2000 = 2451545

    def __init__(self, year, month, day, hour, minute, second):
        if month < 1 or month > 12:
            raise Exception("wrong month %d" % month)
        # Special handling for October 1582 (Julian calendar gap)
        # Valid days are 1-4 and 15-31, not continuous 1-21
        if year == 1582 and month == 10:
            if day < 1 or day > 31:
                raise Exception("wrong day %d" % day)
            if 4 < day < 15:
                raise Exception("wrong solar year %d month %d day %d" % (year, month, day))
        elif day < 1 or day > SolarUtil.getDaysOfMonth(year, month):
            raise Exception("wrong day %d" % day)
        if hour < 0 or hour > 23:
            raise Exception("wrong hour %d" % hour)
        if minute < 0 or minute > 59:
            raise Exception("wrong minute %d" % minute)
        if second < 0 or second > 59:
            raise Exception("wrong second %d" % second)
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
        self.__second = second

    @staticmethod
    def fromDate(date):
        return Solar(date.year, date.month, date.day, date.hour, date.minute, date.second)

    @staticmethod
    def fromJulianDay(julian_day):
        d = int(julian_day + 0.5)
        f = julian_day + 0.5 - d
        if d >= 2299161:
            c = int((d - 1867216.25) / 36524.25)
            d += 1 + c - int(c / 4)
        d += 1524
        year = int((d - 122.1) / 365.25)
        d -= int(365.25 * year)
        month = int(d / 30.601)
        d -= int(30.601 * month)
        day = d
        if month > 13:
            month -= 13
            year -= 4715
        else:
            month -= 1
            year -= 4716
        f *= 24
        hour = int(f)

        f -= hour
        f *= 60
        minute = int(f)

        f -= minute
        f *= 60
        second = int(round(f))
        if second > 59:
            second -= 60
            minute += 1
        if minute > 59:
            minute -= 60
            hour += 1
        if hour > 23:
            hour -= 24
            day += 1
            # Handle month overflow
            days_in_month = SolarUtil.getDaysOfMonth(year, month)
            if day > days_in_month:
                day -= days_in_month
                month += 1
                if month > 12:
                    month = 1
                    year += 1
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return Solar(year, month, day, hour, minute, second)

    @staticmethod
    def fromYmd(year, month, day):
        return Solar(year, month, day, 0, 0, 0)

    @staticmethod
    def fromBaZi(year_gan_zhi, month_gan_zhi, day_gan_zhi, time_gan_zhi, sect=2, base_year=1900):
        from . import Lunar
        sect = 1 if 1 == sect else 2
        solar_list = []
        # Offset of month Zhi from Yin month
        _, month_zhi = LunarUtil.splitGanZhi(month_gan_zhi)
        m = LunarUtil.find(month_zhi, LunarUtil.ZHI, -1) - 2
        if m < 0:
            m += 12
        # Month Gan must match
        year_gan, _ = LunarUtil.splitGanZhi(year_gan_zhi)
        month_gan, _ = LunarUtil.splitGanZhi(month_gan_zhi)
        if ((LunarUtil.find(year_gan, LunarUtil.GAN, -1) + 1) * 2 + m) % 10 != LunarUtil.find(month_gan, LunarUtil.GAN, -1):
            return solar_list
        # Li Chun (Start of Spring) of year 1 is Xin You, index 57
        y = LunarUtil.getJiaZiIndex(year_gan_zhi) - 57
        if y < 0:
            y += 60
        y += 1
        # Solar term offset
        m *= 2
        # Time Zhi to hour, Zi (0th hour) treated as midnight
        _, time_zhi = LunarUtil.splitGanZhi(time_gan_zhi)
        h = LunarUtil.find(time_zhi, LunarUtil.ZHI, -1) * 2
        hours = [h]
        if 0 == h and 2 == sect:
            hours.append(23)
        start_year = base_year - 1

        # End year
        end_year = datetime.now().year

        while y <= end_year:
            if y >= start_year:
                # Li Chun (Start of Spring) marks the start of Yin month
                jie_qi_table = Lunar.fromYmd(y, 1, 1).getJieQiTable()
                # Advance solar term, year and month GanZhi will match
                solar_time = jie_qi_table[Lunar.JIE_QI_IN_USE[4 + m]]
                if solar_time.getYear() >= base_year:
                    # Day GanZhi offset from solar term GanZhi
                    d = LunarUtil.getJiaZiIndex(day_gan_zhi) - LunarUtil.getJiaZiIndex(solar_time.getLunar().getDayInGanZhiExact2())
                    if d < 0:
                        d += 60
                    if d > 0:
                        # Advance days from solar term
                        solar_time = solar_time.next(d)
                    for hour in hours:
                        mi = 0
                        s = 0
                        if d == 0 and hour == solar_time.getHour():
                            # If exactly on the solar term day with matching hour, carry minutes and seconds
                            mi = solar_time.getMinute()
                            s = solar_time.getSecond()
                        # Validate
                        solar = Solar.fromYmdHms(solar_time.getYear(), solar_time.getMonth(), solar_time.getDay(), hour, mi, s)
                        if d == 30:
                            solar = solar.nextHour(-1)
                        lunar = solar.getLunar()
                        dgz = lunar.getDayInGanZhiExact2() if 2 == sect else lunar.getDayInGanZhiExact()
                        if lunar.getYearInGanZhiExact() == year_gan_zhi and lunar.getMonthInGanZhiExact() == month_gan_zhi and dgz == day_gan_zhi and lunar.getTimeInGanZhi() == time_gan_zhi:
                            solar_list.append(solar)
            y += 60
        return solar_list

    def isLeapYear(self):
        """
        Whether leap year
        :return: True/False leap year/not leap year
        """
        return SolarUtil.isLeapYear(self.__year)

    def getWeek(self):
        """
        Get weekday, 0 for Sunday, 1 for Monday
        :return: 0123456
        """
        return (int(self.getJulianDay() + 0.5) + 7000001) % 7

    def getWeekInChinese(self):
        """
        Get week in Chinese
        :return: Sun-Sat (日一二三四五六)
        """
        return SolarUtil.WEEK[self.getWeek()]

    def getFestivals(self):
        """
        Get festivals, possibly multiple in one day
        :return: e.g. Labor Day
        """
        festivals = []
        key = "%d-%d" % (self.__month, self.__day)
        if key in SolarUtil.FESTIVAL:
            festivals.append(SolarUtil.FESTIVAL[key])
        week = self.getWeek()
        key = "%d-%d-%d" % (self.__month, int(ceil(self.__day / 7.0)), week)
        if key in SolarUtil.WEEK_FESTIVAL:
            festivals.append(SolarUtil.WEEK_FESTIVAL[key])
        if self.__day + 7 > SolarUtil.getDaysOfMonth(self.__year, self.__month):
            key = "%d-0-%d" % (self.__month, week)
            if key in SolarUtil.WEEK_FESTIVAL:
                festivals.append(SolarUtil.WEEK_FESTIVAL[key])
        return festivals

    def getOtherFestivals(self):
        """
        Get unofficial festivals, possibly multiple in one day
        :return: Unofficial festival list, e.g. Hungry Ghost Festival
        """
        festivals = []
        key = "%d-%d" % (self.__month, self.__day)
        if key in SolarUtil.OTHER_FESTIVAL:
            for f in SolarUtil.OTHER_FESTIVAL[key]:
                festivals.append(f)
        return festivals

    def getXingZuo(self):
        """
        Get constellation/zodiac
        :return: Constellation
        """
        index = 11
        y = self.__month * 100 + self.__day
        if 321 <= y <= 419:
            index = 0
        elif 420 <= y <= 520:
            index = 1
        elif 521 <= y <= 621:
            index = 2
        elif 622 <= y <= 722:
            index = 3
        elif 723 <= y <= 822:
            index = 4
        elif 823 <= y <= 922:
            index = 5
        elif 923 <= y <= 1023:
            index = 6
        elif 1024 <= y <= 1122:
            index = 7
        elif 1123 <= y <= 1221:
            index = 8
        elif y >= 1222 or y <= 119:
            index = 9
        elif y <= 218:
            index = 10
        return SolarUtil.XING_ZUO[index]

    def getJulianDay(self):
        """
        Get Julian day
        :return: Julian day
        """
        y = self.__year
        m = self.__month
        d = self.__day + ((self.__second / 60.0 + self.__minute) / 60 + self.__hour) / 24
        n = 0
        g = False
        if y * 372 + m * 31 + int(d) >= 588829:
            g = True
        if m <= 2:
            m += 12
            y -= 1
        if g:
            n = int(y / 100)
            n = 2 - n + int(n / 4)
        return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + n - 1524.5

    def getLunar(self):
        """
        Get lunar calendar
        :return: Lunar
        """
        from .Lunar import Lunar
        return Lunar.fromSolar(self)

    def nextDay(self, days):
        y = self.__year
        m = self.__month
        d = self.__day
        if 1582 == y and 10 == m:
            if d > 4:
                d -= 10
        if days > 0:
            d += days
            days_in_month = SolarUtil.getDaysOfMonth(y, m)
            while d > days_in_month:
                d -= days_in_month
                m += 1
                if m > 12:
                    m = 1
                    y += 1
                days_in_month = SolarUtil.getDaysOfMonth(y, m)
        elif days < 0:
            while d + days <= 0:
                m -= 1
                if m < 1:
                    m = 12
                    y -= 1
                d += SolarUtil.getDaysOfMonth(y, m)
            d += days
        if 1582 == y and 10 == m:
            if d > 4:
                d += 10
        return Solar.fromYmdHms(y, m, d, self.__hour, self.__minute, self.__second)

    def next(self, days, only_work_day=False):
        """
        Get solar date pushed forward by days, use negative for backward.
        NOTE: only_work_day=True falls back to weekend-skip behavior because the
        legacy PRC statutory schedule (HolidayUtil) was removed in v1.4.9.
        A Vietnamese government-schedule implementation is TODO.
        """
        if not only_work_day:
            return self.nextDay(days)
        solar = Solar.fromYmdHms(self.__year, self.__month, self.__day, self.__hour, self.__minute, self.__second)
        if days != 0:
            rest = abs(days)
            add = 1
            if days < 0:
                add = -1
            while rest > 0:
                solar = solar.next(add)
                week = solar.getWeek()
                if 0 != week and 6 != week:
                    rest -= 1
        return solar

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getDay(self):
        return self.__day

    def getHour(self):
        return self.__hour

    def getMinute(self):
        return self.__minute

    def getSecond(self):
        return self.__second

    def toYmd(self):
        return "%04d-%02d-%02d" % (self.__year, self.__month, self.__day)

    def toYmdHms(self):
        return "%s %02d:%02d:%02d" % (self.toYmd(), self.__hour, self.__minute, self.__second)

    def toFullString(self):
        s = self.toYmdHms()
        if self.isLeapYear():
            s += " Năm nhuận"
        s += " Thứ "
        s += self.getWeekInChinese()
        for f in self.getFestivals():
            s += " (" + f + ")"
        for f in self.getOtherFestivals():
            s += " (" + f + ")"
        s += " "
        s += self.getXingZuo()
        return s

    def toString(self):
        return self.toYmd()

    def __str__(self):
        return self.toString()

    def subtract(self, solar):
        return SolarUtil.getDaysBetween(solar.getYear(), solar.getMonth(), solar.getDay(), self.__year, self.__month, self.__day)

    def subtractMinute(self, solar):
        days = self.subtract(solar)
        cm = self.__hour * 60 + self.__minute
        sm = solar.getHour() * 60 + solar.getMinute()
        m = cm - sm
        if m < 0:
            m += 1440
            days -= 1
        m += days * 1440
        return m

    def isAfter(self, solar):
        if self.__year > solar.getYear():
            return True
        if self.__year < solar.getYear():
            return False
        if self.__month > solar.getMonth():
            return True
        if self.__month < solar.getMonth():
            return False
        if self.__day > solar.getDay():
            return True
        if self.__day < solar.getDay():
            return False
        if self.__hour > solar.getHour():
            return True
        if self.__hour < solar.getHour():
            return False
        if self.__minute > solar.getMinute():
            return True
        if self.__minute < solar.getMinute():
            return False
        return self.__second > solar.getSecond()

    def isBefore(self, solar):
        if self.__year > solar.getYear():
            return False
        if self.__year < solar.getYear():
            return True
        if self.__month > solar.getMonth():
            return False
        if self.__month < solar.getMonth():
            return True
        if self.__day > solar.getDay():
            return False
        if self.__day < solar.getDay():
            return True
        if self.__hour > solar.getHour():
            return False
        if self.__hour < solar.getHour():
            return True
        if self.__minute > solar.getMinute():
            return False
        if self.__minute < solar.getMinute():
            return True
        return self.__second < solar.getSecond()

    def nextYear(self, years):
        y = self.__year + years
        m = self.__month
        d = self.__day
        if 1582 == y and 10 == m:
            if 4 < d < 15:
                d += 10
        elif 2 == m:
            if d > 28:
                if not SolarUtil.isLeapYear(y):
                    d = 28
        return Solar.fromYmdHms(y, m, d, self.__hour, self.__minute, self.__second)

    def nextMonth(self, months):
        from . import SolarMonth
        month = SolarMonth.fromYm(self.__year, self.__month).next(months)
        y = month.getYear()
        m = month.getMonth()
        d = self.__day
        if 1582 == y and 10 == m:
            if 4 < d < 15:
                d += 10
        else:
            days = SolarUtil.getDaysOfMonth(y, m)
            if d > days:
                d = days
        return Solar.fromYmdHms(y, m, d, self.__hour, self.__minute, self.__second)

    def nextHour(self, hours):
        h = self.__hour + hours
        n = 1
        if h < 0:
            n = -1
        hour = abs(h)
        days = int(hour / 24) * n
        hour = (hour % 24) * n
        if hour < 0:
            hour += 24
            days -= 1
        solar = self.next(days)
        return Solar.fromYmdHms(solar.getYear(), solar.getMonth(), solar.getDay(), hour, solar.getMinute(), solar.getSecond())
