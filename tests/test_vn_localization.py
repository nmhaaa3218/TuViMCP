# -*- coding: utf-8 -*-
"""
Tests for Phase 2: Native Vietnamese Data Layer & Terminology Engine
"""

import pytest
from tuvi_mcp.lunar_calendar import Solar, Lunar
from tuvi_mcp.lunar_calendar.util import LunarUtil


def test_vietnamese_can_chi_names():
    """Verify Can and Chi are native Vietnamese strings."""
    solar = Solar.fromYmd(2026, 7, 27)
    lunar = solar.getLunar()
    
    assert lunar.getYearGanVn() in ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    assert lunar.getYearZhiVn() in ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    assert lunar.getYearInGanZhiVn() == f"{lunar.getYearGanVn()} {lunar.getYearZhiVn()}"


def test_zodiac_mote_native_cat():
    """
    CRITICAL: In Vietnamese calendar:
    - Mão (卯) must be Mèo (Cat), NOT Rabbit (Thỏ)
    - Sửu (丑) must be Trâu (Water Buffalo)
    - Mùi (未) must be Dê (Goat)
    - Hợi (亥) must be Heo/Lợn (Pig)
    """
    assert LunarUtil.SHENGXIAO_VI[4] == "Mèo"  # Mão
    assert LunarUtil.SHENGXIAO_VI[2] == "Trâu" # Sửu
    assert LunarUtil.SHENGXIAO_VI[8] == "Dê"   # Mùi
    assert LunarUtil.SHENGXIAO_VI[12] == "Heo"  # Hợi

    # Year 2023 was Year of Mão -> Should be Mèo
    solar_2023 = Solar.fromYmd(2023, 6, 1)
    lunar_2023 = solar_2023.getLunar()
    assert lunar_2023.getYearShengXiaoVn() == "Mèo"


def test_vietnamese_tiet_khi_names():
    """Verify 24 Tiết Khí return Vietnamese Sino-Vietnamese names."""
    solar = Solar.fromYmd(2026, 2, 4) # Lập Xuân period
    lunar = solar.getLunar()
    jie_qi = lunar.getJieQi()
    assert jie_qi in ["Lập Xuân", "Vũ Thủy", "Kinh Trập", "Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng", "Hạ Chí", "Tiểu Thử", "Đại Thử", "Lập Thu", "Xử Thử", "Bạch Lộ", "Thu Phân", "Hàn Lộ", "Sương Giáng", "Lập Đông", "Tiểu Tuyết", "Đại Tuyết", "Đông Chí", "Tiểu Hàn", "Đại Hàn", ""]


def test_vietnamese_truc_names():
    """Verify 12 Trực return Vietnamese names."""
    solar = Solar.fromYmd(2026, 7, 27)
    lunar = solar.getLunar()
    assert lunar.getDayZhiXingVn() in ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Chấp", "Phá", "Nguy", "Thành", "Thu", "Khai", "Bế"]


def test_vietnamese_than_hoang_dao():
    """Verify 12 Thần Hoàng Đạo / Hắc Đạo return Vietnamese names."""
    solar = Solar.fromYmd(2026, 7, 27)
    lunar = solar.getLunar()
    assert lunar.getDayTianShenVn() in ["Thanh Long", "Minh Đường", "Thiên Hình", "Chu Tước", "Kim Quỹ", "Bảo Quang", "Bạch Hổ", "Ngọc Đường", "Thiên Lao", "Huyền Vũ", "Tư Mệnh", "Câu Trận"]

