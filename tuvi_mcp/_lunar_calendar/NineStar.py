# -*- coding: utf-8 -*-
from .util import LunarUtil


class NineStar:
    """
    Nine Star
    """

    NUMBER = ("Nhất", "Nhị", "Tam", "Tứ", "Ngũ", "Lục", "Thất", "Bát", "Cửu")
    NUMBER_VI = ("Nhất", "Nhị", "Tam", "Tứ", "Ngũ", "Lục", "Thất", "Bát", "Cửu")
    COLOR = ("Bạch", "Hắc", "Bích", "Lục", "Hoàng", "Bạch", "Xích", "Bạch", "Tử")
    COLOR_VI = ("Bạch", "Hắc", "Bích", "Lục", "Hoàng", "Bạch", "Xích", "Bạch", "Tử")
    WU_XING = ("Thủy", "Thổ", "Mộc", "Mộc", "Thổ", "Kim", "Kim", "Thổ", "Hỏa")
    WU_XING_VI = ("Thủy", "Thổ", "Mộc", "Mộc", "Thổ", "Kim", "Kim", "Thổ", "Hỏa")
    POSITION = ("Khảm", "Khôn", "Chấn", "Tốn", "Trung", "Càn", "Đoài", "Cấn", "Ly")
    POSITION_VI = ("Khảm", "Khôn", "Chấn", "Tốn", "Trung", "Càn", "Đoài", "Cấn", "Ly")
    NAME_BEI_DOU = ("Tham Lang", "Cự Môn", "Lộc Tồn", "Văn Khúc", "Liêm Trinh", "Vũ Khúc", "Phá Quân", "Tả Phụ", "Hữu Bật")
    NAME_BEI_DOU_VI = ("Tham Lang", "Cự Môn", "Lộc Tồn", "Văn Khúc", "Liêm Trinh", "Vũ Khúc", "Phá Quân", "Tả Phụ", "Hữu Bật")
    NAME_XUAN_KONG = ("Tham Lang", "Cự Môn", "Lộc Tồn", "Văn Khúc", "Liêm Trinh", "Vũ Khúc", "Phá Quân", "Tả Phụ", "Hữu Bật")
    NAME_XUAN_KONG_VI = ("Tham Lang", "Cự Môn", "Lộc Tồn", "Văn Khúc", "Liêm Trinh", "Vũ Khúc", "Phá Quân", "Tả Phụ", "Hữu Bật")
    NAME_QI_MEN = ("Thiên Bồng", "Thiên Nhuế", "Thiên Xung", "Thiên Phụ", "Thiên Cầm", "Thiên Tâm", "Thiên Trụ", "Thiên Nhậm", "Thiên Anh")
    BA_MEN_QI_MEN = ("Hưu", "Tử", "Thương", "Đỗ", "", "Khai", "Kinh", "Sinh", "Cảnh")
    NAME_TAI_YI = ("Thái Ất", "Nhiếp Đề", "Hiên Viên", "Chiêu Dao", "Thiên Phù", "Thanh Long", "Hàm Trì", "Thái Âm", "Thiên Ất")
    TYPE_TAI_YI = ("Cát Thần", "Hung Thần", "An Thần", "An Thần", "Hung Thần", "Cát Thần", "Hung Thần", "Cát Thần", "Cát Thần")
    SONG_TAI_YI = (
        "Cửa gặp Thái Ất sáng, sao hiệu Tham Lang, cầu xin tài lộc hưng vong, hôn nhân đại cát hanh thông, ra vào không trở ngại, gặp gỡ bậc hiền lương, đi năm ba dặm, mặc áo đen phân âm dương.",
        "Trước cửa thấy Nhiếp Đề, trăm việc phải nghiền ngẫm, tương sinh còn tạm được, tương khắc họa tất tới, Tử Môn cùng hội họi, bà lão khóc thảm thương, cầu mưu sự cát, chẳng nên chăng hợp, chỉ nên ẩn núp trốn tránh, động tới thương tích thân.",
        "Ra vào gặp Hiên Viên, mọi việc tất ràng buộc, tương sinh chẳng tốt đẹp, tương khắc càng lo buồn, đi xa nhiều bất lợi, đánh bạc thua sạch tiền, Cửu Thiên Huyền Nữ pháp, câu câu chẳng vọng ngôn.",
        "Chiêu Dao hiệu Mộc Tinh, đương sự chớ nên hành, tương khắc kẻ qua đường trở ngại, người âm mồm miệng nghinh đón, chiêm bao nhiều kinh sợ, nhà vang tiếng búa tự kêu, âm dương tiêu tin lý, vạn pháp chẳng trái tình.",
        "Ngũ Quỷ là Thiên Phù, cửa gặp đàn bà âm mưu, tương khắc chẳng việc tốt, đường đi trở ngại nửa đường, đi lạc khó tìm kiếm, đường gặp có ni cô, sao này đương cửa trị, vạn sự có tai trừ.",
        "Thần quang nhảy Thanh Long, khí tài vui mừng nặng, đầu tư có rượu thịt, đánh bạc hưng thịnh nhất, lại gặp tương sinh vượng, thôi nói khắc phá hung, thấy quý lập doanh trại, vạn sự tổng cát đồng.",
        "Ta sẽ vì Hàm Trì, đương nó hết chẳng nên, ra vào nhiều bất lợi, tương khắc có tai tình, đánh bạc thua sạch hết, cầu tài tay không về, tiên nhân quả diệu ngữ, người ngu chớ nên biết, động dụng hư kinh thoái, lặp lặp nghịch phong thổi.",
        "Ngồi đến Thái Âm tinh, trăm họa chẳng xâm phạm, cầu mưu mọi sự thành, tri giao có tìm kiếm, hồi phong quy lại lộ, sợ có ương phục khởi, mật ngữ trung ký thụ, thận hề chớ khinh hành.",
        "Nghênh đón Thiên Ất tinh, tương phùng trăm sự hưng, vận dụng hòa hợp mừng, trà rượu vui nghênh đón, cầu mưu và xin cưới, hảo hợp có thiên thành, họa phúc như thần nghiệm, cát hung thật phân minh."
    )
    LUCK_XUAN_KONG = ("Cát", "Hung", "Hung", "Cát", "Hung", "Cát", "Hung", "Cát", "Cát")
    LUCK_QI_MEN = ("Đại Hung", "Đại Hung", "Tiểu Cát", "Đại Cát", "Đại Cát", "Đại Cát", "Tiểu Hung", "Tiểu Cát", "Tiểu Hung")
    YIN_YANG_QI_MEN = ("Dương", "Âm", "Dương", "Dương", "Dương", "Âm", "Âm", "Dương", "Âm")



    def __init__(self, index):
        self.__index = index

    @staticmethod
    def fromIndex(index):
        return NineStar(index)

    def getNumber(self):
        return NineStar.NUMBER[self.__index]

    def getColor(self):
        return NineStar.COLOR[self.__index]

    def getWuXing(self):
        return NineStar.WU_XING[self.__index]

    def getPosition(self):
        return NineStar.POSITION[self.__index]

    def getPositionDesc(self):
        return LunarUtil.POSITION_DESC[self.getPosition()]

    def getNameInXuanKong(self):
        return NineStar.NAME_XUAN_KONG[self.__index]

    def getNameInBeiDou(self):
        return NineStar.NAME_BEI_DOU[self.__index]

    def getNameInQiMen(self):
        return NineStar.NAME_QI_MEN[self.__index]

    def getNameInTaiYi(self):
        return NineStar.NAME_TAI_YI[self.__index]

    def getLuckInQiMen(self):
        return NineStar.LUCK_QI_MEN[self.__index]

    def getLuckInXuanKong(self):
        return NineStar.LUCK_XUAN_KONG[self.__index]

    def getYinYangInQiMen(self):
        return NineStar.YIN_YANG_QI_MEN[self.__index]

    def getTypeInTaiYi(self):
        return NineStar.TYPE_TAI_YI[self.__index]

    def getBaMenInQiMen(self):
        return NineStar.BA_MEN_QI_MEN[self.__index]

    def getSongInTaiYi(self):
        return NineStar.SONG_TAI_YI[self.__index]

    def getIndex(self):
        return self.__index

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.getNumber() + self.getColor() + self.getWuXing() + self.getNameInBeiDou()

    def toFullString(self):
        s = self.getNumber()
        s += self.getColor()
        s += self.getWuXing()
        s += " "
        s += self.getPosition()
        s += "("
        s += self.getPositionDesc()
        s += ") "
        s += self.getNameInBeiDou()
        s += " Huyền Không["
        s += self.getNameInXuanKong()
        s += " "
        s += self.getLuckInXuanKong()
        s += "] Kỳ Môn["
        s += self.getNameInQiMen()
        s += " "
        s += self.getLuckInQiMen()
        if len(self.getBaMenInQiMen()) > 0:
            s += " "
            s += self.getBaMenInQiMen()
            s += " Môn"
        s += " "
        s += self.getYinYangInQiMen()
        s += "] Thái Ất["
        s += self.getNameInTaiYi()
        s += " "
        s += self.getTypeInTaiYi()
        s += "]"
        return s
