# -*- coding: utf-8 -*-
from ...util import LunarUtil
from . import LiuYue


class LiuNian:
    """
    Liu Nian (Yearly Cycle)
    """

    def __init__(self, da_yun, index):
        self.__daYun = da_yun
        self.__lunar = da_yun.getLunar()
        self.__index = index
        self.__year = da_yun.getStartYear() + index
        self.__age = da_yun.getStartAge() + index

    def getIndex(self):
        return self.__index

    def getYear(self):
        return self.__year

    def getAge(self):
        return self.__age

    def getGanZhi(self):
        """
        Get GanZhi (Heavenly Stem & Earthly Branch)
        :return: GanZhi
        """
        offset = LunarUtil.getJiaZiIndex(self.__lunar.getJieQiTable()["Lập Xuân"].getLunar().getYearInGanZhiExact()) + self.__index
        if self.__daYun.getIndex() > 0:
            offset += self.__daYun.getStartAge() - 1
        offset %= len(LunarUtil.JIA_ZI)
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

    def getLiuYue(self):
        """
        Get Liu Yue (Monthly Cycle)
        :return: Liu Yue
        """
        n = 12
        liu_yue = []
        for i in range(0, n):
            liu_yue.append(LiuYue(self, i))
        return liu_yue
