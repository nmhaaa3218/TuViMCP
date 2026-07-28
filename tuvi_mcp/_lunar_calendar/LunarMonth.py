# -*- coding: utf-8 -*-
from . import Solar, LunarYear, NineStar
from .util import LunarUtil


class LunarMonth:
    """
    Lunar month
    """

    def __init__(self, lunar_year, lunar_month, day_count, first_julian_day, index):
        self.__year = lunar_year
        self.__month = lunar_month
        self.__dayCount = day_count
        self.__firstJulianDay = first_julian_day
        self.__index = index
        self.__zhiIndex = (abs(lunar_month) - 1 + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12

    @staticmethod
    def fromYm(lunar_year, lunar_month):
        from . import LunarYear
        return LunarYear.fromYear(lunar_year).getMonth(lunar_month)

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month

    def getIndex(self):
        return self.__index

    def getZhiIndex(self):
        return self.__zhiIndex

    def getGanIndex(self):
        offset = (LunarYear.fromYear(self.__year).getGanIndex() + 1) % 5 * 2
        return (abs(self.__month) - 1 + offset) % 10

    def getGan(self):
        return LunarUtil.GAN[self.getGanIndex() + 1]

    def getZhi(self):
        return LunarUtil.ZHI[self.getZhiIndex() + 1]

    def getGanZhi(self):
        return "%s%s" % (self.getGan(), self.getZhi())

    def getPositionXi(self):
        return LunarUtil.POSITION_XI[self.getGanIndex() + 1]

    def getPositionXiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionXi()]

    def getPositionYangGui(self):
        return LunarUtil.POSITION_YANG_GUI[self.getGanIndex() + 1]

    def getPositionYangGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYangGui()]

    def getPositionYinGui(self):
        return LunarUtil.POSITION_YIN_GUI[self.getGanIndex() + 1]

    def getPositionYinGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYinGui()]

    def getPositionFu(self, sect=2):
        return (LunarUtil.POSITION_FU if 1 == sect else LunarUtil.POSITION_FU_2)[self.getGanIndex() + 1]

    def getPositionFuDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getPositionFu(sect)]

    def getPositionCai(self):
        return LunarUtil.POSITION_CAI[self.getGanIndex() + 1]

    def getPositionCaiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionCai()]

    def isLeap(self):
        return self.__month < 0

    def getDayCount(self):
        return self.__dayCount

    def getFirstJulianDay(self):
        return self.__firstJulianDay

    def getPositionTaiSui(self):
        m = abs(self.__month) % 4
        if 0 == m:
            p = "Tốn"
        elif 1 == m:
            p = "Cấn"
        elif 3 == m:
            p = "Khôn"
        else:
            p = LunarUtil.POSITION_GAN[Solar.fromJulianDay(self.getFirstJulianDay()).getLunar().getMonthGanIndex()]
        return p

    def getPositionTaiSuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionTaiSui()]

    def getNineStar(self):
        index = LunarYear.fromYear(self.__year).getZhiIndex() % 3
        m = abs(self.__month)
        month_zhi_index = (13 + m) % 12
        n = 27 - (index * 3)
        if month_zhi_index < LunarUtil.BASE_MONTH_ZHI_INDEX:
            n -= 3
        offset = (n - month_zhi_index) % 9
        return NineStar.fromIndex(offset)

    def toString(self):
        return "%d năm %s%s tháng (%d ngày)" % (self.__year, ("Nhuận " if self.isLeap() else ""), LunarUtil.MONTH[abs(self.__month)], self.__dayCount)

    def __str__(self):
        return self.toString()

    def next(self, n):
        """
        Get lunar month pushed forward by n months, use negative for backward
        :param n: Months
        :return: Lunar month
        """
        if 0 == n:
            return LunarMonth.fromYm(self.__year, self.__month)
        elif n > 0:
            rest = n
            ny = self.__year
            iy = ny
            im = self.__month
            index = 0
            months = LunarYear.fromYear(ny).getMonths()
            while True:
                size = len(months)
                for i in range(0, size):
                    m = months[i]
                    if m.getYear() == iy and m.getMonth() == im:
                        index = i
                        break
                more = size - index - 1
                if rest < more:
                    break
                rest -= more
                last_month = months[size - 1]
                iy = last_month.getYear()
                im = last_month.getMonth()
                ny += 1
                months = LunarYear.fromYear(ny).getMonths()
            return months[index + rest]
        else:
            rest = -n
            ny = self.__year
            iy = ny
            im = self.__month
            index = 0
            months = LunarYear.fromYear(ny).getMonths()
            while True:
                size = len(months)
                for i in range(0, size):
                    m = months[i]
                    if m.getYear() == iy and m.getMonth() == im:
                        index = i
                        break
                if rest <= index:
                    break
                rest -= index
                first_month = months[0]
                iy = first_month.getYear()
                im = first_month.getMonth()
                ny -= 1
                months = LunarYear.fromYear(ny).getMonths()
            return months[index - rest]
