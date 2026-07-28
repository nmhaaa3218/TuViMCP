# -*- coding: utf-8 -*-
from . import XiaoYun, LiuNian
from ...util import LunarUtil


class DaYun:
    """
    Da Yun (Decade Fortune)
    """

    def __init__(self, yun, index: int):
        self.__yun = yun
        self.__lunar = yun.getLunar()
        self.__index = index
        birth_year = yun.getLunar().getSolar().getYear()
        year = yun.getStartSolar().getYear()
        if index < 1:
            self.__startYear = birth_year
            self.__startAge = 1
            self.__endYear = year - 1
            self.__endAge = year - birth_year
        else:
            add = (index - 1) * 10
            self.__startYear = year + add
            self.__startAge = self.__startYear - birth_year + 1
            self.__endYear = self.__startYear + 9
            self.__endAge = self.__startAge + 9

    def getStartYear(self):
        return self.__startYear

    def getEndYear(self):
        return self.__endYear

    def getStartAge(self):
        return self.__startAge

    def getEndAge(self):
        return self.__endAge

    def getIndex(self):
        return self.__index

    def getLunar(self):
        return self.__lunar

    def getGanZhi(self):
        """
        Get GanZhi (Heavenly Stem & Earthly Branch)
        :return: GanZhi
        """
        if self.__index < 1:
            return ""
        offset = LunarUtil.getJiaZiIndex(self.__lunar.getMonthInGanZhiExact())
        offset += self.__index if self.__yun.isForward() else -self.__index
        size = len(LunarUtil.JIA_ZI)
        if offset >= size:
            offset -= size
        if offset < 0:
            offset += size
        return LunarUtil.JIA_ZI[offset]

    def getXun(self):
        """
        Get Xun (cycle)
        :return: Xun
        """
        return LunarUtil.getXun(self.getGanZhi())

    def getXunKong(self):
        """
        Get XunKong (Void)
        :return: XunKong (Void)
        """
        return LunarUtil.getXunKong(self.getGanZhi())

    def getLiuNian(self, n=10):
        """
        Get Liu Nian (Yearly Cycle)
        :param n: Count
        :return: Liu Nian
        """
        if self.__index < 1:
            n = self.__endYear - self.__startYear + 1
        liu_nian = []
        for i in range(0, n):
            liu_nian.append(LiuNian(self, i))
        return liu_nian

    def getXiaoYun(self, n=10):
        """
        Get Xiao Yun (Yearly Fortune)
        :param n: Count
        :return: Xiao Yun
        """
        if self.__index < 1:
            n = self.__endYear - self.__startYear + 1
        xiao_yun = []
        for i in range(0, n):
            xiao_yun.append(XiaoYun(self, i, self.__yun.isForward()))
        return xiao_yun
