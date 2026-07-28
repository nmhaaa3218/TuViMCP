# -*- coding: utf-8 -*-
from .util import LunarUtil


class EightChar:
    """
    Eight Characters (Ba Zi)
    """

    MONTH_ZHI = ("", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu")

    CHANG_SHENG = ("Tràng Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng")

    __CHANG_SHENG_OFFSET = {
        "Giáp": 1, "Ất": 6, "Bính": 10, "Đinh": 9, "Mậu": 10,
        "Kỷ": 9, "Canh": 7, "Tân": 0, "Nhâm": 4, "Quý": 3
    }


    def __init__(self, lunar):
        self.__sect = 2
        self.__lunar = lunar

    @staticmethod
    def fromLunar(lunar):
        return EightChar(lunar)

    def toString(self):
        return self.getYear() + " " + self.getMonth() + " " + self.getDay() + " " + self.getTime()

    def __str__(self):
        return self.toString()

    def getSect(self):
        return self.__sect

    def setSect(self, sect):
        self.__sect = sect

    def getYear(self):
        """
        Get year pillar
        :return: Year pillar
        """
        return self.__lunar.getYearInGanZhiExact()

    def getYearGan(self):
        """
        Get year heavenly stem
        :return: Heavenly stem
        """
        return self.__lunar.getYearGanExact()

    def getYearZhi(self):
        """
        Get year earthly branch
        :return: Earthly branch
        """
        return self.__lunar.getYearZhiExact()

    def getYearHideGan(self):
        """
        Get hidden stems in year pillar's earthly branch, may contain 1-3 elements (primary, secondary, tertiary)
        :return: Heavenly stems
        """
        return LunarUtil.ZHI_HIDE_GAN.get(self.getYearZhi())

    def getYearWuXing(self):
        """
        Get year pillar's five elements
        :return: Five elements
        """
        return LunarUtil.WU_XING_GAN.get(self.getYearGan()) + LunarUtil.WU_XING_ZHI.get(self.getYearZhi())

    def getYearNaYin(self):
        """
        Get year pillar's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getYear())

    def getYearShiShenGan(self):
        """
        Get year pillar's heavenly stem Shi Shen (10 Spirits)
        :return: Shi Shen
        """
        return LunarUtil.SHI_SHEN.get(self.getDayGan() + self.getYearGan())

    def __getShiShenZhi(self, zhi):
        hide_gan = LunarUtil.ZHI_HIDE_GAN.get(zhi)
        arr = []
        for gan in hide_gan:
            arr.append(LunarUtil.SHI_SHEN.get(self.getDayGan() + gan))
        return arr

    def getYearShiShenZhi(self):
        """
        Get year pillar's earthly branch Shi Shen (10 Spirits), may contain 1-3 elements
        :return: Shi Shen
        """
        return self.__getShiShenZhi(self.getYearZhi())

    def getDayGanIndex(self):
        return self.__lunar.getDayGanIndexExact2() if 2 == self.__sect else self.__lunar.getDayGanIndexExact()

    def getDayZhiIndex(self):
        return self.__lunar.getDayZhiIndexExact2() if 2 == self.__sect else self.__lunar.getDayZhiIndexExact()

    def __getDiShi(self, zhi_index):
        index = self.__CHANG_SHENG_OFFSET.get(self.getDayGan()) + (zhi_index if self.getDayGanIndex() % 2 == 0 else -zhi_index)
        if index >= 12:
            index -= 12
        if index < 0:
            index += 12
        return EightChar.CHANG_SHENG[index]

    def getYearDiShi(self):
        """
        Get year pillar's Di Shi (12 Growth Stages)
        :return: Di Shi
        """
        return self.__getDiShi(self.__lunar.getYearZhiIndexExact())

    def getMonth(self):
        """
        Get month pillar
        :return: Month pillar
        """
        return self.__lunar.getMonthInGanZhiExact()

    def getMonthGan(self):
        """
        Get month heavenly stem
        :return: Heavenly stem
        """
        return self.__lunar.getMonthGanExact()

    def getMonthZhi(self):
        """
        Get month earthly branch
        :return: Earthly branch
        """
        return self.__lunar.getMonthZhiExact()

    def getMonthHideGan(self):
        """
        Get hidden stems in month pillar's earthly branch, may contain 1-3 elements (primary, secondary, tertiary)
        :return: Heavenly stems
        """
        return LunarUtil.ZHI_HIDE_GAN.get(self.getMonthZhi())

    def getMonthWuXing(self):
        """
        Get month pillar's five elements
        :return: Five elements
        """
        return LunarUtil.WU_XING_GAN.get(self.getMonthGan()) + LunarUtil.WU_XING_ZHI.get(self.getMonthZhi())

    def getMonthNaYin(self):
        """
        Get month pillar's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getMonth())

    def getMonthShiShenGan(self):
        """
        Get month pillar's heavenly stem Shi Shen (10 Spirits)
        :return: Shi Shen
        """
        return LunarUtil.SHI_SHEN.get(self.getDayGan() + self.getMonthGan())

    def getMonthShiShenZhi(self):
        """
        Get month pillar's earthly branch Shi Shen (10 Spirits), may contain 1-3 elements
        :return: Shi Shen
        """
        return self.__getShiShenZhi(self.getMonthZhi())

    def getMonthDiShi(self):
        """
        Get month pillar's Di Shi (12 Growth Stages)
        :return: Di Shi
        """
        return self.__getDiShi(self.__lunar.getMonthZhiIndexExact())

    def getDay(self):
        """
        Get day pillar
        :return: Day pillar
        """
        return self.__lunar.getDayInGanZhiExact2() if 2 == self.__sect else self.__lunar.getDayInGanZhiExact()

    def getDayGan(self):
        """
        Get day heavenly stem
        :return: Heavenly stem
        """
        return self.__lunar.getDayGanExact2() if 2 == self.__sect else self.__lunar.getDayGanExact()

    def getDayZhi(self):
        """
        Get day earthly branch
        :return: Earthly branch
        """
        return self.__lunar.getDayZhiExact2() if 2 == self.__sect else self.__lunar.getDayZhiExact()

    def getDayHideGan(self):
        """
        Get hidden stems in day pillar's earthly branch, may contain 1-3 elements (primary, secondary, tertiary)
        :return: Heavenly stems
        """
        return LunarUtil.ZHI_HIDE_GAN.get(self.getDayZhi())

    def getDayWuXing(self):
        """
        Get day pillar's five elements
        :return: Five elements
        """
        return LunarUtil.WU_XING_GAN.get(self.getDayGan()) + LunarUtil.WU_XING_ZHI.get(self.getDayZhi())

    def getDayNaYin(self):
        """
        Get day pillar's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getDay())

    def getDayShiShenGan(self):
        """
        Get day pillar's heavenly stem Shi Shen (10 Spirits), also known as Day Master, Day Stem
        :return: Shi Shen (Nhật Chủ)
        """
        return "Nhật Chủ"

    def getDayShiShenZhi(self):
        """
        Get day pillar's earthly branch Shi Shen (10 Spirits), may contain 1-3 elements
        :return: Shi Shen
        """
        return self.__getShiShenZhi(self.getDayZhi())

    def getDayDiShi(self):
        """
        Get day pillar's Di Shi (12 Growth Stages)
        :return: Di Shi
        """
        return self.__getDiShi(self.getDayZhiIndex())

    def getTime(self):
        """
        Get time pillar
        :return: Time pillar
        """
        return self.__lunar.getTimeInGanZhi()

    def getTimeGan(self):
        """
        Get time heavenly stem
        :return: Heavenly stem
        """
        return self.__lunar.getTimeGan()

    def getTimeZhi(self):
        """
        Get time earthly branch
        :return: Earthly branch
        """
        return self.__lunar.getTimeZhi()

    def getTimeHideGan(self):
        """
        Get hidden stems in time pillar's earthly branch, may contain 1-3 elements (primary, secondary, tertiary)
        :return: Heavenly stems
        """
        return LunarUtil.ZHI_HIDE_GAN.get(self.getTimeZhi())

    def getTimeWuXing(self):
        """
        Get time pillar's five elements
        :return: Five elements
        """
        return LunarUtil.WU_XING_GAN.get(self.getTimeGan()) + LunarUtil.WU_XING_ZHI.get(self.getTimeZhi())

    def getTimeNaYin(self):
        """
        Get time pillar's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getTime())

    def getTimeShiShenGan(self):
        """
        Get time pillar's heavenly stem Shi Shen (10 Spirits)
        :return: Shi Shen
        """
        return LunarUtil.SHI_SHEN.get(self.getDayGan() + self.getTimeGan())

    def getTimeShiShenZhi(self):
        """
        Get time pillar's earthly branch Shi Shen (10 Spirits), may contain 1-3 elements
        :return: Shi Shen
        """
        return self.__getShiShenZhi(self.getTimeZhi())

    def getTimeDiShi(self):
        """
        Get time pillar's Di Shi (12 Growth Stages)
        :return: Di Shi
        """
        return self.__getDiShi(self.__lunar.getTimeZhiIndex())

    def getTaiYuan(self):
        """
        Get Tai Yuan (Fetal Origin)
        :return: Tai Yuan
        """
        gan_index = self.__lunar.getMonthGanIndexExact() + 1
        if gan_index >= 10:
            gan_index -= 10
        zhi_index = self.__lunar.getMonthZhiIndexExact() + 3
        if zhi_index >= 12:
            zhi_index -= 12
        return f"{LunarUtil.GAN[gan_index + 1]} {LunarUtil.ZHI[zhi_index + 1]}"

    def getTaiYuanNaYin(self):
        """
        Get Tai Yuan's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getTaiYuan())

    def getTaiXi(self):
        """
        Get Tai Xi (Fetal Breath)
        :return: Tai Xi
        """
        gan_index = self.__lunar.getDayGanIndexExact2() if 2 == self.__sect else self.__lunar.getDayGanIndexExact()
        zhi_index = self.__lunar.getDayZhiIndexExact2() if 2 == self.__sect else self.__lunar.getDayZhiIndexExact()
        return f"{LunarUtil.HE_GAN_5[gan_index]} {LunarUtil.HE_ZHI_6[zhi_index]}"

    def getTaiXiNaYin(self):
        """
        Get Tai Xi's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getTaiXi())

    def getMingGong(self):
        """
        Get Ming Gong (Destiny Palace)
        :return: Ming Gong
        """
        month_zhi_index = 0
        time_zhi_index = 0
        month_zhi = self.getMonthZhi()
        time_zhi = self.getTimeZhi()
        for i in range(0, len(EightChar.MONTH_ZHI)):
            zhi = EightChar.MONTH_ZHI[i]
            if month_zhi == zhi:
                month_zhi_index = i
                break
        for i in range(0, len(EightChar.MONTH_ZHI)):
            zhi = EightChar.MONTH_ZHI[i]
            if time_zhi == zhi:
                time_zhi_index = i
                break
        offset = month_zhi_index + time_zhi_index
        if offset >= 14:
            offset = 26 - offset
        else:
            offset = 14 - offset
        gan_index = (self.__lunar.getYearGanIndexExact() + 1) * 2 + offset
        while gan_index > 10:
            gan_index -= 10
        return f"{LunarUtil.GAN[gan_index]} {EightChar.MONTH_ZHI[offset]}"

    def getMingGongNaYin(self):
        """
        Get Ming Gong's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getMingGong())

    def getShenGong(self):
        """
        Get Shen Gong (Body Palace)
        :return: Shen Gong
        """
        month_zhi_index = 0
        time_zhi_index = 0
        month_zhi = self.getMonthZhi()
        time_zhi = self.getTimeZhi()
        for i in range(0, len(EightChar.MONTH_ZHI)):
            zhi = EightChar.MONTH_ZHI[i]
            if month_zhi == zhi:
                month_zhi_index = i
                break
        for i in range(0, len(LunarUtil.ZHI)):
            zhi = LunarUtil.ZHI[i]
            if time_zhi == zhi:
                time_zhi_index = i
                break
        offset = month_zhi_index + time_zhi_index
        if offset > 12:
            offset -= 12
        gan_index = (self.__lunar.getYearGanIndexExact() + 1) * 2 + offset
        while gan_index > 10:
            gan_index -= 10
        return f"{LunarUtil.GAN[gan_index]} {EightChar.MONTH_ZHI[offset]}"

    def getShenGongNaYin(self):
        """
        Get Shen Gong's Na Yin (element)
        :return: Na Yin
        """
        return LunarUtil.NAYIN.get(self.getShenGong())

    def getLunar(self):
        return self.__lunar

    def getYun(self, gender, sect=1):
        """
        Get Fortune (Yun)
        :param gender: Gender: 1 male, 0 female
        :param sect School: 1 by days and hours (3 days = 1 year, 1 day = 4 months, 1 hour = 10 days); 2 by minutes
        :return: Yun (Fortune)
        """
        from .eightchar import Yun
        return Yun(self, gender, sect)

    def getYearXun(self):
        """
        Get year pillar's Xun (cycle)
        :return: Xun
        """
        return self.__lunar.getYearXunExact()

    def getYearXunKong(self):
        """
        Get year pillar's XunKong (Void)
        :return: XunKong (Void)
        """
        return self.__lunar.getYearXunKongExact()

    def getMonthXun(self):
        """
        Get month pillar's Xun (cycle)
        :return: Xun
        """
        return self.__lunar.getMonthXunExact()

    def getMonthXunKong(self):
        """
        Get month pillar's XunKong (Void)
        :return: XunKong (Void)
        """
        return self.__lunar.getMonthXunKongExact()

    def getDayXun(self):
        """
        Get day pillar's Xun (cycle)
        :return: Xun
        """
        return self.__lunar.getDayXunExact2() if 2 == self.__sect else self.__lunar.getDayXunExact()

    def getDayXunKong(self):
        """
        Get day pillar's XunKong (Void)
        :return: XunKong (Void)
        """
        return self.__lunar.getDayXunKongExact2() if 2 == self.__sect else self.__lunar.getDayXunKongExact()

    def getTimeXun(self):
        """
        Get time pillar's Xun (cycle)
        :return: Xun
        """
        return self.__lunar.getTimeXun()

    def getTimeXunKong(self):
        """
        Get time pillar's XunKong (Void)
        :return: XunKong (Void)
        """
        return self.__lunar.getTimeXunKong()
