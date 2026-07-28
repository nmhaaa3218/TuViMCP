# -*- coding: utf-8 -*-
"""
Tests for Vietnamese Holiday & Cultural Ritual Engine (v1.4.9+).

Vietnamese-only scope: official statutory + widely-recognized folk + Vietnamese
Buddhist. Chinese-derived / regional observances accessible via
`with_imported=True`.
"""

import pytest
from tuvi_mcp.lunar_calendar import Solar, Lunar
from tuvi_mcp.lunar_calendar.VietnameseHoliday import VietnameseHoliday
from tuvi_mcp.lunar_calendar.vn_holidays import VnHolidayRegistry


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


def test_thất_tịch_is_imported_scope():
    """Thất Tịch (7/7) is Chinese-origin; opt-in via with_imported=True."""
    # Default lookup: hidden
    assert VnHolidayRegistry.get_lunar(7, 7) is None
    # Opt-in: visible with imported scope flag
    assert VnHolidayRegistry.get_lunar(7, 7, with_imported=True) is not None
    assert "Thất Tịch" in VnHolidayRegistry.get_lunar(7, 7, with_imported=True)


def test_phat_dan_is_buddhist_vn_scope():
    """Phật Đản must be 4-15 (GHPGVN), not 4-8 (Chinese calendar)."""
    assert VnHolidayRegistry.get_lunar(4, 15) is not None
    assert "Phật Đản" in VnHolidayRegistry.get_lunar(4, 15)


def test_vu_lan_drops_trung_nguyen_label():
    """Vu Lan label must NOT include Đạo giáo 'Trung Nguyên' framing."""
    name = VnHolidayRegistry.get_lunar(7, 15)
    assert name is not None
    assert "Vu Lan" in name
    assert "Trung Nguyên" not in name


def test_lunar_object_festivals():
    """Test getVietnameseFestivals on Lunar object."""
    lunar_tet = Lunar.fromYmd(2026, 1, 1)
    festivals = lunar_tet.getVietnameseFestivals()
    assert any("Tết Nguyên Đán" in f for f in festivals)


def test_lunar_extended_festivals_includes_imported():
    """getVietnameseFestivalsExtended(with_imported=True) surfaces imported entries."""
    lunar = Lunar.fromYmd(2026, 7, 7)
    default = lunar.getVietnameseFestivalsExtended()
    extended = lunar.getVietnameseFestivalsExtended(with_imported=True)
    assert len(extended) >= len(default)
    scopes = {e.scope for e in extended}
    if extended:
        assert "imported" in scopes


def test_vietnamese_solar_holidays():
    """Verify national Vietnamese solar holidays."""
    assert VietnameseHoliday.get_solar_holiday(4, 30) == "Ngày Giải phóng miền Nam"
    assert VietnameseHoliday.get_solar_holiday(5, 1) == "Quốc tế Lao động"
    assert VietnameseHoliday.get_solar_holiday(9, 2) == "Quốc khánh Việt Nam"


def test_registry_metadata_exposes_scope():
    """Every registry entry exposes scope metadata for caller-side filtering."""
    all_entries = list(VnHolidayRegistry.LUNAR) + list(VnHolidayRegistry.SOLAR)
    assert len(all_entries) > 0
    scopes = {e.scope for e in all_entries}
    assert {"official", "folk", "buddhist_vn"}.issubset(scopes)
