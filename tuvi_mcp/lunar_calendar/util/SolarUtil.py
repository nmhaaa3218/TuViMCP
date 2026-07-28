# -*- coding: utf-8 -*-
from math import ceil


class SolarUtil:
    """
    Solar calendar utility
    """

    # Weekday names
    WEEK = ("Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy")

    # Days per month
    DAYS_OF_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    # Zodiac signs
    XING_ZUO = ("Bạch Dương", "Kim Ngưu", "Song Tử", "Cự Giải", "Sư Tử", "Xử Nữ", "Thiên Bình", "Bọ Cạp", "Nhân Mã", "Ma Kết", "Bảo Bình", "Song Ngư")

    # Date festivals (Vietnamese solar calendar holidays)
    FESTIVAL = {
        "1-1": "Tết Dương Lịch",
        "2-14": "Lễ Tình Nhân (Valentine)",
        "3-8": "Quốc tế Phụ nữ",
        "4-30": "Ngày Giải phóng miền Nam",
        "5-1": "Quốc tế Lao động",
        "6-1": "Quốc tế Thiếu nhi",
        "9-2": "Quốc khánh Việt Nam",
        "10-20": "Ngày Phụ nữ Việt Nam",
        "11-20": "Ngày Nhà giáo Việt Nam",
        "12-22": "Ngày Thành lập QĐND Việt Nam",
        "12-25": "Lễ Giáng sinh"
    }


    # Nth weekday of month festivals
    WEEK_FESTIVAL = {
        "5-2-0": "Ngày của Mẹ",
        "6-3-0": "Ngày của Cha",
        "11-4-4": "Lễ Tạ Ơn"
    }

    # Unofficial date festivals
    OTHER_FESTIVAL = {}

    def __init__(self):
        pass

    @staticmethod
    def isLeapYear(year):
        """
        Is leap year
        :param year: Year
        :return: True/False leap year/not leap year
        """
        if year < 1600:
            return year % 4 == 0
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def getDaysOfYear(year):
        if 1582 == year:
            return 355
        d = 365
        if SolarUtil.isLeapYear(year):
            d = 366
        return d

    @staticmethod
    def getDaysOfMonth(year, month):
        """
        Get days of a specific month in a specific year
        :param year: Year
        :param month: Month
        :return: Day count
        """
        if 1582 == year and 10 == month:
            return 21
        d = SolarUtil.DAYS_OF_MONTH[month - 1]
        # Leap year February has one extra day
        if month == 2 and SolarUtil.isLeapYear(year):
            d += 1
        return d

    @staticmethod
    def getDaysInYear(year, month, day):
        days = 0
        for i in range(1, month):
            days += SolarUtil.getDaysOfMonth(year, i)
        d = day
        if 1582 == year and 10 == month:
            if day >= 15:
                d -= 10
            elif day > 4:
                raise Exception("wrong solar year %d  month %d day %d" % (year, month, day))
        days += d
        return days

    @staticmethod
    def getWeeksOfMonth(year, month, start):
        """
        Get weeks of a specific month in a specific year
        :param year: Year
        :param month: Month
        :param start: Weekday as start of week, 1234560 = Monday to Sunday
        :return: Week count
        """
        from .. import Solar
        return int(ceil((SolarUtil.getDaysOfMonth(year, month) + Solar.fromYmd(year, month, 1).getWeek() - start) * 1.0 / len(SolarUtil.WEEK)))

    @staticmethod
    def getDaysBetween(ay: int, am: int, ad: int, by: int, bm: int, bd: int):
        if ay == by:
            n = SolarUtil.getDaysInYear(by, bm, bd) - SolarUtil.getDaysInYear(ay, am, ad)
        elif ay > by:
            days = SolarUtil.getDaysOfYear(by) - SolarUtil.getDaysInYear(by, bm, bd)
            for i in range(by + 1, ay):
                days += SolarUtil.getDaysOfYear(i)
            days += SolarUtil.getDaysInYear(ay, am, ad)
            n = -days
        else:
            days = SolarUtil.getDaysOfYear(ay) - SolarUtil.getDaysInYear(ay, am, ad)
            for i in range(ay + 1, by):
                days += SolarUtil.getDaysOfYear(i)
            days += SolarUtil.getDaysInYear(by, bm, bd)
            n = days
        return n
