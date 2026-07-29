# -*- coding: utf-8 -*-
import threading
from math import floor

from . import NineStar, Solar
from .util import LunarUtil, ShouXingUtil


class LunarYear:
    """
    Lunar year
    """

    YUAN = ("Hạ", "Thượng", "Trung")

    YUN = ("Thất", "Bát", "Cửu", "Nhất", "Nhị", "Tam", "Tứ", "Ngũ", "Lục")

    __LEAP_11 = (75, 94, 170, 265, 322, 398, 469, 553, 583, 610, 678, 735, 754, 773, 849, 887, 936, 1050, 1069, 1126, 1145, 1164, 1183, 1259, 1278, 1308, 1373, 1403, 1441, 1460, 1498, 1555, 1593, 1612, 1631, 1642, 2033, 2128, 2147, 2242, 2614, 2728, 2910, 3062, 3244, 3339, 3616, 3711, 3730, 3825, 4007, 4159, 4197, 4322, 4341, 4379, 4417, 4531, 4599, 4694, 4713, 4789, 4808, 4971, 5085, 5104, 5161, 5180, 5199, 5294, 5305, 5476, 5677, 5696, 5772, 5791, 5848, 5886, 6049, 6068, 6144, 6163, 6258, 6402, 6440, 6497, 6516, 6630, 6641, 6660, 6679, 6736, 6774, 6850, 6869, 6899, 6918, 6994, 7013, 7032, 7051, 7070, 7089, 7108, 7127, 7146, 7222, 7271, 7290, 7309, 7366, 7385, 7404, 7442, 7461, 7480, 7491, 7499, 7594, 7624, 7643, 7662, 7681, 7719, 7738, 7814, 7863, 7882, 7901, 7939, 7958, 7977, 7996,
                 8034, 8053, 8072, 8091, 8121, 8159, 8186, 8216, 8235, 8254, 8273, 8311, 8330, 8341, 8349, 8368, 8444, 8463, 8474, 8493, 8531, 8569, 8588, 8626, 8664, 8683, 8694, 8702, 8713, 8721, 8751, 8789, 8808, 8816, 8827, 8846, 8884, 8903, 8922, 8941, 8971, 9036, 9066, 9085, 9104, 9123, 9142, 9161, 9180, 9199, 9218, 9256, 9294, 9313, 9324, 9343, 9362, 9381, 9419, 9438, 9476, 9514, 9533, 9544, 9552, 9563, 9571, 9582, 9601, 9639, 9658, 9666, 9677, 9696, 9734, 9753, 9772, 9791, 9802, 9821, 9886, 9897, 9916, 9935, 9954, 9973, 9992)

    __LEAP_12 = (37, 56, 113, 132, 151, 189, 208, 227, 246, 284, 303, 341, 360, 379, 417, 436, 458, 477, 496, 515, 534, 572, 591, 629, 648, 667, 697, 716, 792, 811, 830, 868, 906, 925, 944, 963, 982, 1001, 1020, 1039, 1058, 1088, 1153, 1202, 1221, 1240, 1297, 1335, 1392, 1411, 1422, 1430, 1517, 1525, 1536, 1574, 3358, 3472, 3806, 3988, 4751, 4941, 5066, 5123, 5275, 5343, 5438, 5457, 5495, 5533, 5552, 5715, 5810, 5829, 5905, 5924, 6421, 6535, 6793, 6812, 6888, 6907, 7002, 7184, 7260, 7279, 7374, 7556, 7746, 7757, 7776, 7833, 7852, 7871, 7966, 8015, 8110, 8129, 8148, 8224, 8243, 8338, 8406, 8425, 8482, 8501, 8520, 8558, 8596, 8607, 8615, 8645, 8740, 8778, 8835, 8865, 8930, 8960, 8979, 8998, 9017, 9055, 9074, 9093, 9112, 9150, 9188, 9237, 9275, 9332, 9351, 9370, 9408, 9427, 9446, 9457, 9465,
                 9495, 9560, 9590, 9628, 9647, 9685, 9715, 9742, 9780, 9810, 9818, 9829, 9848, 9867, 9905, 9924, 9943, 9962, 10000)

    __CACHE_YEAR = None

    __lock = threading.Lock()

    def __init__(self, lunar_year):
        self.__year = lunar_year
        offset = lunar_year - 4
        year_gan_index = offset % 10
        year_zhi_index = offset % 12
        if year_gan_index < 0:
            year_gan_index += 10
        if year_zhi_index < 0:
            year_zhi_index += 12
        self.__ganIndex = year_gan_index
        self.__zhiIndex = year_zhi_index
        self.__months = []
        self.__jieQiJulianDays = []
        self.compute()

    @staticmethod
    def fromYear(lunar_year):
        LunarYear.__lock.acquire()
        if LunarYear.__CACHE_YEAR is None or LunarYear.__CACHE_YEAR.getYear() != lunar_year:
            y = LunarYear(lunar_year)
            LunarYear.__CACHE_YEAR = y
        else:
            y = LunarYear.__CACHE_YEAR
        LunarYear.__lock.release()
        return y

    def compute(self):
        from . import Lunar, LunarMonth, Solar
        # Solar terms
        jq = []
        # New moon (first day of each month)
        hs = []
        # Days per month, length 15
        day_counts = []
        # Months
        months = []

        current_year = self.__year
        jd = floor((current_year - 2000) * 365.2422 + 180)
        # 355 is the Winter Solstice of 2000.12, get an estimated Winter Solstice close to jd
        w = floor((jd - 355 + 183) / 365.2422) * 365.2422 + 355
        if ShouXingUtil.calcQi(w) > jd:
            w -= 365.2422
        # 25 solar term times (Beijing time), starting from Winter Solstice to the next Winter Solstice
        for i in range(0, 26):
            jq.append(ShouXingUtil.calcQi(w + 15.2184 * i))

        # From last year's Major Snow to next year's Start of Spring, precise solar terms
        for i in range(0, len(Lunar.JIE_QI_IN_USE)):
            if i == 0:
                jd = ShouXingUtil.qiAccurate2(jq[0] - 15.2184)
            elif i <= 26:
                jd = ShouXingUtil.qiAccurate2(jq[i - 1])
            else:
                jd = ShouXingUtil.qiAccurate2(jq[25] + 15.2184 * (i - 26))
            self.__jieQiJulianDays.append(jd + Solar.J2000)

        # First new moon before Winter Solstice, the solar-lunar longitude difference w
        w = ShouXingUtil.calcShuo(jq[0])
        if w > jq[0]:
            w -= 29.53
        # Recurse each month's first day
        for i in range(0, 16):
            hs.append(ShouXingUtil.calcShuo(w + 29.5306 * i))
        # 每月
        for i in range(0, 15):
            day_counts.append(int(hs[i + 1] - hs[i]))
            months.append(i)

        prev_year = current_year - 1
        leap_index = 16

        if current_year in LunarYear.__LEAP_11:
            leap_index = 13
        elif current_year in LunarYear.__LEAP_12:
            leap_index = 14
        elif hs[13] <= jq[24]:
            i = 1
            while hs[i + 1] > jq[2 * i] and i < 13:
                i += 1
            leap_index = i
        for j in range(leap_index, 15):
            months[j] -= 1
        ymc = [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        fm = -1
        index = -1
        y = prev_year
        for i in range(0, 15):
            dm = hs[i] + Solar.J2000
            v2 = months[i]
            mc = ymc[v2 % 12]
            if 1724360 <= dm < 1729794:
                mc = ymc[(v2 + 1) % 12]
            elif 1807724 <= dm < 1808699:
                mc = ymc[(v2 + 1) % 12]
            elif dm == 1729794 or dm == 1808699:
                mc = 12
            if fm == -1:
                fm = mc
                index = mc
            if mc < fm:
                y += 1
                index = 1
            fm = mc
            if i == leap_index:
                mc = -mc
            elif dm == 1729794 or dm == 1808699:
                mc = -11
            self.__months.append(LunarMonth(y, mc, day_counts[i], dm, index))
            index += 1

    def getYear(self):
        return self.__year

    def getGanIndex(self):
        return self.__ganIndex

    def getZhiIndex(self):
        return self.__zhiIndex

    def getGan(self):
        return LunarUtil.GAN[self.__ganIndex + 1]

    def getZhi(self):
        return LunarUtil.ZHI[self.__zhiIndex + 1]

    def getGanZhi(self):
        return "%s%s" % (self.getGan(), self.getZhi())

    def toString(self):
        return str(self.__year) + ""

    def toFullString(self):
        return "%d年" % self.__year

    def __str__(self):
        return self.toString()

    def getDayCount(self):
        n = 0
        for m in self.__months:
            if m.getYear() == self.__year:
                n += m.getDayCount()
        return n

    def getMonthsInYear(self):
        months = []
        for m in self.__months:
            if m.getYear() == self.__year:
                months.append(m)
        return months

    def getMonths(self):
        return self.__months

    def getJieQiJulianDays(self):
        return self.__jieQiJulianDays

    def getLeapMonth(self):
        """
        Get leap month
        :return: Leap month number, 1 for leap 1st month, 0 for no leap month
        """
        for m in self.__months:
            if m.getYear() == self.__year and m.isLeap():
                return abs(m.getMonth())
        return 0

    def getMonth(self, lunar_month):
        """
        Get lunar month
        :param lunar_month: Leap month number, 1 for leap 1st month, 0 for no leap month
        :return: Lunar month
        """
        for m in self.__months:
            if m.getYear() == self.__year and m.getMonth() == lunar_month:
                return m
        return None

    def __getZaoByGan(self, index, name):
        offset = index - Solar.fromJulianDay(self.getMonth(1).getFirstJulianDay()).getLunar().getDayGanIndex()
        if offset < 0:
            offset += 10
        return name.replace("几", LunarUtil.NUMBER[offset + 1], 1)

    def __getZaoByZhi(self, index, name):
        offset = index - Solar.fromJulianDay(self.getMonth(1).getFirstJulianDay()).getLunar().getDayZhiIndex()
        if offset < 0:
            offset += 12
        return name.replace("几", LunarUtil.NUMBER[offset + 1], 1)

    def getTouLiang(self):
        return self.__getZaoByZhi(0, "几鼠偷粮")

    def getCaoZi(self):
        return self.__getZaoByZhi(0, "草子几分")

    def getGengTian(self):
        """
        Get plowing (first Chou day of first month, e.g. Six Oxen Plowing)
        :return: Plowing, e.g. Six Oxen Plowing
        """
        return self.__getZaoByZhi(1, "几牛耕田")

    def getHuaShou(self):
        return self.__getZaoByZhi(3, "花收几分")

    def getZhiShui(self):
        """
        Get water management (first Chen day of first month, e.g. Two Dragons Water Management)
        :return: Water management, e.g. Two Dragons Water Management
        """
        return self.__getZaoByZhi(4, "几龙治水")

    def getTuoGu(self):
        return self.__getZaoByZhi(6, "几马驮谷")

    def getQiangMi(self):
        return self.__getZaoByZhi(9, "几鸡抢米")

    def getKanCan(self):
        return self.__getZaoByZhi(9, "几姑看蚕")

    def getGongZhu(self):
        return self.__getZaoByZhi(11, "几屠共猪")

    def getJiaTian(self):
        return self.__getZaoByGan(0, "甲田几分")

    def getFenBing(self):
        """
        Get cake division (first Bing day of first month, e.g. Six People Share Cake)
        :return: Cake division, e.g. Six People Share Cake
        """
        return self.__getZaoByGan(2, "几人分饼")

    def getDeJin(self):
        """
        Get gold acquisition (first Xin day of first month, e.g. One Day Acquires Gold)
        :return: Gold acquisition, e.g. One Day Acquires Gold
        """
        return self.__getZaoByGan(7, "几日得金")

    def getRenBing(self):
        return self.__getZaoByGan(2, self.__getZaoByZhi(2, "几人几丙"))

    def getRenChu(self):
        return self.__getZaoByGan(3, self.__getZaoByZhi(2, "几人几锄"))

    def getYuan(self):
        return LunarYear.YUAN[int((self.__year + 2696) / 60) % 3] + " Nguyên"

    def getYun(self):
        return LunarYear.YUN[int((self.__year + 2696) / 20) % 9] + " Vận"

    def getNineStar(self):
        index = LunarUtil.getJiaZiIndex(self.getGanZhi()) + 1
        yuan = int((self.__year + 2696) / 60) % 3
        offset = (62 + yuan * 3 - index) % 9
        if 0 == offset:
            offset = 9
        return NineStar.fromIndex(offset - 1)

    def getPositionXi(self):
        return LunarUtil.POSITION_XI[self.__ganIndex + 1]

    def getPositionXiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionXi()]

    def getPositionYangGui(self):
        return LunarUtil.POSITION_YANG_GUI[self.__ganIndex + 1]

    def getPositionYangGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYangGui()]

    def getPositionYinGui(self):
        return LunarUtil.POSITION_YIN_GUI[self.__ganIndex + 1]

    def getPositionYinGuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionYinGui()]

    def getPositionFu(self, sect=2):
        return (LunarUtil.POSITION_FU if 1 == sect else LunarUtil.POSITION_FU_2)[self.__ganIndex + 1]

    def getPositionFuDesc(self, sect=2):
        return LunarUtil.POSITION_DESC[self.getPositionFu(sect)]

    def getPositionCai(self):
        return LunarUtil.POSITION_CAI[self.__ganIndex + 1]

    def getPositionCaiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionCai()]

    def getPositionTaiSui(self):
        return LunarUtil.POSITION_TAI_SUI_YEAR[self.__zhiIndex]

    def getPositionTaiSuiDesc(self):
        return LunarUtil.POSITION_DESC[self.getPositionTaiSui()]

    def next(self, n):
        """
        Get lunar year pushed forward by n years, use negative for backward
        :param n: Years
        :return: Lunar year
        """
        return LunarYear.fromYear(self.__year + n)
