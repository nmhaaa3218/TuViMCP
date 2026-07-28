# -*- coding: utf-8 -*-
from ..FotoFestival import FotoFestival


class FotoUtil:
    """
    Phật lịch - Buddhist Calendar
    """

    DAY_ZHAI_GUAN_YIN = ("1-8", "2-7", "2-9", "2-19", "3-3", "3-6", "3-13", "4-22", "5-3", "5-17", "6-16", "6-18", "6-19", "6-23", "7-13", "8-16", "9-19", "9-23", "10-2", "11-19", "11-24", "12-25")

    XIU_27 = ("Giác", "Cang", "Đê", "Phòng", "Tâm", "Vĩ", "Cơ", "Đẩu", "Nữ", "Hư", "Nguy", "Thất", "Bích", "Khuê", "Lâu", "Vị", "Mão", "Tất", "Chủy", "Sâm", "Tỉnh", "Quỷ", "Liễu", "Tinh", "Trương", "Dực", "Chẩn")

    XIU_OFFSET = (11, 13, 15, 17, 19, 21, 24, 0, 2, 4, 7, 9)

    @staticmethod
    def getXiu(month, day):
        return FotoUtil.XIU_27[(FotoUtil.XIU_OFFSET[abs(month)-1] + day - 1) % len(FotoUtil.XIU_27)]

    __DJ = "Phạm giả đoạt kỷ"
    __JS = "Phạm giả giảm thọ"
    __SS = "Phạm giả tổn thọ"
    __XL = "Phạm giả tước lộc đoạt kỷ"
    __JW = "Phạm giả tam niên nội phu phụ câu vong"

    __Y = FotoFestival("Dương Công Kỵ")
    __T = FotoFestival("Tứ Thiên Vương Tuần Hành", "", True)
    __D = FotoFestival("Đẩu Giáng", __DJ, True)
    __S = FotoFestival("Nguyệt Sóc", __DJ, True)
    __W = FotoFestival("Nguyệt Vọng", __DJ, True)
    __H = FotoFestival("Nguyệt Hối", __JS, True)
    __L = FotoFestival("Lôi Trai Nhật", __JS, True)
    __J = FotoFestival("Cửu Độc Nhật", "Phạm giả yểu vong, kỳ họa bất trắc")
    __R = FotoFestival("Nhân Thần Tại Âm", "Phạm giả đắc bệnh", True, "Nên giới trước một ngày")
    __M = FotoFestival("Tư Mệnh Tấu Sự", __JS, True, "Nếu tháng thiếu, giới ngày 29")
    __HH = FotoFestival("Nguyệt Hối", __JS, True, "Nếu tháng thiếu, giới ngày 29")

    FESTIVAL = {}

    OTHER_FESTIVAL = {
        "1-1": ["Lễ Di Lặc Bồ Tát"],
        "1-6": ["Lễ Định Quang Phật"],
        "2-8": ["Phật Xuất Gia"],
        "2-15": ["Phật Niết Bàn"],
        "2-19": ["Lễ Quán Thế Âm Bồ Tát"],
        "2-21": ["Lễ Phổ Hiền Bồ Tát"],
        "3-16": ["Lễ Chuẩn Đề Bồ Tát"],
        "4-4": ["Lễ Văn Thù Bồ Tát"],
        "4-8": ["Lễ Phật Đản"],
        "4-15": ["Phật Cát Tường Nhật"],
        "4-28": ["Lễ Dược Vương Bồ Tát"],
        "5-13": ["Lễ Già Lam Bồ Tát"],
        "6-3": ["Lễ Vi Đà Bồ Tát"],
        "6-19": ["Quán Thế Âm Thành Đạo"],
        "7-13": ["Lễ Đại Thế Chí Bồ Tát"],
        "7-15": ["Phật Hoan Hỉ Nhật"],
        "7-24": ["Lễ Long Thọ Bồ Tát"],
        "7-30": ["Lễ Địa Tạng Bồ Tát"],
        "8-15": ["Lễ Nguyệt Quang Bồ Tát"],
        "8-22": ["Lễ Nhiên Đăng Cổ Phật"],
        "9-9": ["Lễ Ma Lợi Chi Thiên Bồ Tát"],
        "9-19": ["Quán Thế Âm Xuất Gia"],
        "9-30": ["Lễ Dược Sư Lưu Ly Quang Phật"],
        "10-5": ["Lễ Bồ Đề Đạt Ma"],
        "10-20": ["Văn Thù Xuất Gia"],
        "11-17": ["Lễ A Di Đà Phật"],
        "11-19": ["Lễ Nhật Quang Bồ Tát"],
        "12-8": ["Phật Thành Đạo"],
        "12-23": ["Lễ Giám Trai Bồ Tát"],
        "12-29": ["Lễ Hoa Nghiêm Bồ Tát"]
    }

    def __init__(self):
        pass
