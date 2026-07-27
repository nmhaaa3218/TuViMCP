# -*- coding: utf-8 -*-
"""
Tests for Phase 3: Vietnamese Holiday & Cultural Ritual Engine
"""

import pytest
from tuvi_mcp.lunar_calendar import Solar, Lunar
from tuvi_mcp.lunar_calendar.VietnameseHoliday import VietnameseHoliday


def test_vietnamese_lunar_holidays():
    """Verify traditional Vietnamese lunar holidays."""
    # 01/01 Lunar: Tết Nguyên Đán
    assert "Tết Nguyên Đán" in VietnameseHoliday.get_lunar_holiday(1, 1)
    
    # 01/07 Lunar: Lễ Khai Hạ
    assert "Khai Hạ" in VietnameseHoliday.get_lunar_holiday(1, 7)

    # 01/10 Lunar: Vía Thần Tài
    assert "Thần Tài" in VietnameseHoliday.get_lunar_holiday(1, 10)

    # 10/03 Lunar: Giỗ Tổ Hùng Vương
    assert VietnameseHoliday.get_lunar_holiday(3, 10) == "Giỗ Tổ Hùng Vương"
    
    # 05/05 Lunar: Tết Đoan Ngọ
    assert "Tết Đoan Ngọ" in VietnameseHoliday.get_lunar_holiday(5, 5)

    # 07/07 Lunar: Thất Tịch
    assert "Thất Tịch" in VietnameseHoliday.get_lunar_holiday(7, 7)
    
    # 15/07 Lunar: Vu Lan báo hiếu
    assert "Vu Lan" in VietnameseHoliday.get_lunar_holiday(7, 15)
    
    # 15/08 Lunar: Tết Trung Thu
    assert "Tết Trung Thu" in VietnameseHoliday.get_lunar_holiday(8, 15)

    # 10/10 Lunar: Tết Trùng Thập
    assert "Trùng Thập" in VietnameseHoliday.get_lunar_holiday(10, 10)
    
    # 23/12 Lunar: Ngày Ông Táo
    assert "Ông Táo" in VietnameseHoliday.get_lunar_holiday(12, 23)
    
    # Leap month should not trigger main holiday
    assert VietnameseHoliday.get_lunar_holiday(1, 1, is_leap=True) is None


def test_lunar_object_festivals():
    """Test getVietnameseFestivals on Lunar object."""
    lunar_tet = Lunar.fromYmd(2026, 1, 1)
    festivals = lunar_tet.getVietnameseFestivals()
    assert any("Tết Nguyên Đán" in f for f in festivals)



def test_vietnamese_solar_holidays():
    """Verify national Vietnamese solar holidays."""
    assert VietnameseHoliday.get_solar_holiday(4, 30) == "Ngày Giải phóng miền Nam"
    assert VietnameseHoliday.get_solar_holiday(5, 1) == "Quốc tế Lao động"
    assert VietnameseHoliday.get_solar_holiday(9, 2) == "Quốc khánh Việt Nam"
