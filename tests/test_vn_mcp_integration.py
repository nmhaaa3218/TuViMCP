# -*- coding: utf-8 -*-
"""
Phase 4 Integration Test: Native Vietnamese Lunar Calendar End-to-End Verification
"""

import pytest
from tuvi_mcp.lunar_calendar import LichAm, LichDuong, VietnameseHoliday, VnCalendarUtil


def test_lich_am_alias_and_native_conversions():
    """Verify LichAm and LichDuong native aliases and UTC+7 calculations."""
    ld = LichDuong.fromYmd(2026, 2, 17) # Tết 2026
    la = ld.getLunar()
    
    assert la.getYear() == 2026
    assert la.getMonth() == 1
    assert la.getDay() == 1
    assert la.getYearInGanZhiVn() == "Bính Ngọ"
    assert la.getYearShengXiaoVn() == "Ngựa"
    
    # Test reverse conversion using LichAm alias
    la_tet = LichAm.fromYmd(2026, 1, 1)
    sol = la_tet.getSolar()
    assert sol.getYear() == 2026
    assert sol.getMonth() == 2
    assert sol.getDay() == 17


def test_vn_calendar_util_direct_astronomy():
    """Test direct astronomical engine functions calibrated to UTC+7."""
    l_day, l_month, l_year, is_leap = VnCalendarUtil.solar_to_lunar_vn(17, 2, 2026)
    assert (l_day, l_month, l_year, is_leap) == (1, 1, 2026, False)

    s_day, s_month, s_year = VnCalendarUtil.lunar_to_solar_vn(1, 1, 2026, False)
    assert (s_day, s_month, s_year) == (17, 2, 2026)


def test_native_holiday_integration():
    """Test holiday integration via LichAm."""
    la = LichAm.fromYmd(2026, 1, 1)
    vn_festivals = la.getVietnameseFestivals()
    assert any("Tết Nguyên Đán" in f for f in vn_festivals)


def test_lunar_time_and_nine_star():
    """Verify NineStar and LunarTime lookups work cleanly without KeyError."""
    la = LichAm.fromYmd(2026, 7, 27)
    nine_star = la.getDayNineStar()
    assert nine_star is not None
    
    time_list = la.getTimes()
    assert len(time_list) >= 12

    for t in time_list:
        assert t.getTianShen() != ""



