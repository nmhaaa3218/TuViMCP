# -*- coding: utf-8 -*-


class JieQi:
    """
    Solar term
    """

    def __init__(self, name, solar):
        self.__name = name
        self.__jie = False
        self.__qi = False
        self.__solar = solar
        self.setName(name)

    def getName(self):
        """
        Get name
        :return: Name
        """
        return self.__name

    def setName(self, name):
        """
        Set name
        :param name: Name
        """
        from . import Lunar
        self.__name = name
        # Reset state before determining new values
        self.__jie = False
        self.__qi = False
        for i in range(0, len(Lunar.JIE_QI)):
            if name == Lunar.JIE_QI[i]:
                if i % 2 == 0:
                    self.__qi = True
                else:
                    self.__jie = True
                return

    def getSolar(self):
        """
        Get solar date
        :return: Solar date
        """
        return self.__solar

    def setSolar(self, solar):
        """
        Set solar date
        :param solar: Solar date
        """
        self.__solar = solar

    def isJie(self):
        """
        Whether Jie (solar term start)
        :return: true/false
        """
        return self.__jie

    def isQi(self):
        """
        Whether Qi (solar term midpoint)
        :return: true/false
        """
        return self.__qi

    def toString(self):
        return self.__name

    def __str__(self):
        return self.toString()
