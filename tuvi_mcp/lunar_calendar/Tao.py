# -*- coding: utf-8 -*-
from . import Lunar, TaoFestival
from .util import LunarUtil, TaoUtil


class Tao:
    """
    Taoist calendar
    """

    BIRTH_YEAR = -2697

    def __init__(self, lunar):
        self.__lunar = lunar

    @staticmethod
    def fromLunar(lunar):
        return Tao(lunar)

    @staticmethod
    def fromYmdHms(year, month, day, hour, minute, second):
        return Tao.fromLunar(Lunar.fromYmdHms(year + Tao.BIRTH_YEAR, month, day, hour, minute, second))

    @staticmethod
    def fromYmd(year, month, day):
        return Tao.fromYmdHms(year, month, day, 0, 0, 0)

    def getLunar(self):
        return self.__lunar

    def getYear(self):
        return self.__lunar.getYear() - Tao.BIRTH_YEAR

    def getMonth(self):
        return self.__lunar.getMonth()

    def getDay(self):
        return self.__lunar.getDay()

    def getYearInChinese(self):
        y = str(self.getYear())
        s = ""
        for i in range(0, len(y)):
            s += LunarUtil.NUMBER[ord(y[i]) - 48]
        return s

    def getMonthInChinese(self):
        return self.__lunar.getMonthInChinese()

    def getDayInChinese(self):
        return self.__lunar.getDayInChinese()

    def getFestivals(self):
        festivals = []
        md = "%d-%d" % (self.getMonth(), self.getDay())
        if md in TaoUtil.FESTIVAL:
            fs = TaoUtil.FESTIVAL[md]
            for f in fs:
                festivals.append(f)
        jq = self.__lunar.getJieQi()
        if "Đông Chí" == jq:
            festivals.append(TaoFestival("元始天尊圣诞"))
        elif "Hạ Chí" == jq:
            festivals.append(TaoFestival("灵宝天尊圣诞"))
        # Eight Festivals (Ba Jie)
        if jq in TaoUtil.BA_JIE:
            festivals.append(TaoFestival(TaoUtil.BA_JIE[jq]))
        # Eight Meeting Days (Ba Hui)
        gz = self.__lunar.getDayInGanZhi()
        if gz in TaoUtil.BA_HUI:
            festivals.append(TaoFestival(TaoUtil.BA_HUI[gz]))
        return festivals

    def __isDayIn(self, days):
        md = "%d-%d" % (self.getMonth(), self.getDay())
        for d in days:
            if md == d:
                return True
        return False

    def isDaySanHui(self):
        return self.__isDayIn(TaoUtil.SAN_HUI)

    def isDaySanYuan(self):
        return self.__isDayIn(TaoUtil.SAN_YUAN)

    def isDayBaJie(self):
        return self.__lunar.getJieQi() in TaoUtil.BA_JIE

    def isDayWuLa(self):
        return self.__isDayIn(TaoUtil.WU_LA)

    def isDayBaHui(self):
        return self.__lunar.getDayInGanZhi() in TaoUtil.BA_HUI

    def isDayMingWu(self):
        return "Mậu" == self.__lunar.getDayGan()

    def isDayAnWu(self):
        return self.__lunar.getDayZhi() == TaoUtil.AN_WU[abs(self.getMonth()) - 1]

    def isDayWu(self):
        return self.isDayMingWu() or self.isDayAnWu()

    def isDayTianShe(self):
        ret = False
        mz = self.__lunar.getMonthZhi()
        dgz = self.__lunar.getDayInGanZhi()
        if mz in ("Dần", "Mão", "Thìn"):
            if "Mậu Dần" == dgz:
                ret = True
        elif mz in ("Tỵ", "Ngọ", "Mùi"):
            if "Giáp Ngọ" == dgz:
                ret = True
        elif mz in ("Thân", "Dậu", "Tuất"):
            if "Mậu Thân" == dgz:
                ret = True
        elif mz in ("Hợi", "Tý", "Sửu"):
            if "Giáp Tý" == dgz:
                ret = True
        return ret

    def __str__(self):
        return self.toString()

    def toString(self):
        return "%s年%s月%s" % (self.getYearInChinese(), self.getMonthInChinese(), self.getDayInChinese())

    def toFullString(self):
        return "Đạo lịch %s năm, Thiên vận %s năm, %s tháng, %s ngày. %s tháng %s ngày, %s giờ." % (self.getYearInChinese(), self.__lunar.getYearInGanZhi(), self.__lunar.getMonthInGanZhi(), self.__lunar.getDayInGanZhi(), self.getMonthInChinese(), self.getDayInChinese(), self.__lunar.getTimeZhi())
