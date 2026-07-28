# -*- coding: utf-8 -*-

from ..util import LunarUtil


class LiuYue:
    """
    Liu Yue (Monthly Cycle)
    """

    def __init__(self, liu_nian, index):
        self.__liuNian = liu_nian
        self.__index = index

    def getIndex(self):
        return self.__index

    def getMonthInChinese(self):
        """
        Get month in Chinese
        :return: Chinese month, e.g. First
        """
        return LunarUtil.MONTH[self.__index + 1]

    def getGanZhi(self):
        """
        Get GanZhi (Heavenly Stem & Earthly Branch)
        <p>
        "Five Tiger Escape" formula:
        Jia-Ki year Bing is first,
        Yi-Geng year Wu is head,
        Bing-Xin year find Geng above,
        Ding-Ren Nham-Yin flows downstream,
        If asked where Wu-Qui goes,
        Jia-Yin above is good pursuit.
        :return: GanZhi
        """
        offset = 0
        year_gan_zhi = self.__liuNian.getGanZhi()
        year_gan = year_gan_zhi.split()[0] if " " in year_gan_zhi else year_gan_zhi[:1]
        if year_gan in ["Giáp", "Kỷ"]:
            offset = 2
        elif year_gan in ["Ất", "Canh"]:
            offset = 4
        elif year_gan in ["Bính", "Tân"]:
            offset = 6
        elif year_gan in ["Đinh", "Nhâm"]:
            offset = 8
        gan = LunarUtil.GAN[(self.__index + offset) % 10 + 1]
        zhi = LunarUtil.ZHI[(self.__index + LunarUtil.BASE_MONTH_ZHI_INDEX) % 12 + 1]
        return f"{gan} {zhi}"


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
