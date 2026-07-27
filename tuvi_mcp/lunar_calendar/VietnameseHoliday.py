# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
Vietnamese Traditional & National Holiday Evaluator.
"""


class VietnameseHoliday:
    """
    Evaluates Vietnamese Lunar & Solar Traditional Holidays.
    """

    LUNAR_HOLIDAYS = {
        "1-1": "Tết Nguyên Đán (Mùng 1 Tết)",
        "1-2": "Mùng 2 Tết Nguyên Đán",
        "1-3": "Mùng 3 Tết Nguyên Đán",
        "1-7": "Lễ Khai Hạ (Hạ Cây Nêu)",
        "1-9": "Ngày Vía Ngọc Hoàng",
        "1-10": "Ngày Vía Thần Tài",
        "1-15": "Tết Nguyên Tiêu (Rằm tháng Giêng / Lễ Thượng Nguyên)",
        "3-3": "Tết Hàn Thực",
        "3-10": "Giỗ Tổ Hùng Vương",
        "4-15": "Lễ Phật Đản (Rằm tháng Tư)",
        "5-5": "Tết Đoan Ngọ (Tết Diệt sâu bọ)",
        "7-7": "Lễ Thất Tịch",
        "7-15": "Vu Lan báo hiếu / Tết Trung Nguyên (Rằm tháng Bảy)",
        "8-15": "Tết Trung Thu (Rằm tháng Tám)",
        "9-9": "Tết Trùng Cửu (Tết Trùng Dương)",
        "10-10": "Tết Trùng Thập (Tết Mới / Tết Thầy Thuốc)",
        "10-15": "Tết Hạ Nguyên (Rằm tháng Mười)",
        "12-23": "Ngày Ông Táo chầu trời (Tết Ông Công Ông Táo)",
    }


    SOLAR_HOLIDAYS = {
        "1-1": "Tết Dương Lịch",
        "2-14": "Lễ Tình Nhân (Valentine)",
        "3-8": "Quốc tế Phụ nữ",
        "4-30": "Ngày Giải phóng miền Nam",
        "5-1": "Quốc tế Lao động",
        "6-1": "Quốc tế Thiếu nhi",
        "9-2": "Quốc khánh Việt Nam",
        "10-20": "Ngày Phụ nữ Việt Nam",
        "11-20": "Ngày Nhà giáo Việt Nam",
        "12-22": "Ngày Thành lập QĐND Việt Nam",
        "12-25": "Lễ Giáng sinh",
    }

    @staticmethod
    def get_lunar_holiday(month: int, day: int, is_leap: bool = False) -> str | None:
        """
        Returns the Vietnamese traditional holiday name for a given lunar month and day.
        Returns None if not a traditional holiday or if it is a leap month.
        """
        if is_leap or month < 0:
            return None
        key = f"{month}-{day}"
        return VietnameseHoliday.LUNAR_HOLIDAYS.get(key)

    @staticmethod
    def get_solar_holiday(month: int, day: int) -> str | None:
        """
        Returns the Vietnamese national holiday name for a given solar month and day.
        """
        key = f"{month}-{day}"
        return VietnameseHoliday.SOLAR_HOLIDAYS.get(key)
