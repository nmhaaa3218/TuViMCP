# -*- coding: utf-8 -*-
"""
Tests for Phase 1: Engine Foundation & Timezone Calibration (UTC+7 Vietnamese Standard)
"""

import pytest
from tuvi_mcp.lunar_calendar import Solar, Lunar


def test_tet_1985_benchmark():
    """
    Historical Benchmark: Tết Ất Sửu 1985
    Vietnam celebrated Tết on Jan 21, 1985 (Lunar 1985/01/01),
    whereas Beijing UTC+8 counted Jan 21 as Lunar 1984/12/30.
    """
    solar = Solar.fromYmd(1985, 1, 21)
    lunar = solar.getLunar()
    assert lunar.getYear() == 1985
    assert lunar.getMonth() == 1
    assert lunar.getDay() == 1


def test_tet_2007_benchmark():
    """
    Historical Benchmark: Tết Đinh Hợi 2007
    Vietnam Mùng 1 Tết was Feb 17, 2007.
    China Mùng 1 Tết was Feb 18, 2007.
    """
    solar = Solar.fromYmd(2007, 2, 17)
    lunar = solar.getLunar()
    assert lunar.getYear() == 2007
    assert lunar.getMonth() == 1
    assert lunar.getDay() == 1


def test_tet_2026_benchmark():
    """
    Tết Bính Ngọ 2026: Feb 17, 2026 is Lunar 2026/01/01
    """
    solar = Solar.fromYmd(2026, 2, 17)
    lunar = solar.getLunar()
    assert lunar.getYear() == 2026
    assert lunar.getMonth() == 1
    assert lunar.getDay() == 1


def test_lunar_to_solar_roundtrip():
    """
    Verify Solar -> Lunar -> Solar roundtrip consistency for multiple dates
    """
    test_dates = [
        (1975, 4, 30),
        (1985, 1, 21),
        (2007, 2, 17),
        (2026, 7, 27),
        (2030, 9, 2),
    ]
    for year, month, day in test_dates:
        solar_orig = Solar.fromYmd(year, month, day)
        lunar = solar_orig.getLunar()
        solar_converted = lunar.getSolar()
        assert solar_converted.getYear() == year
        assert solar_converted.getMonth() == month
        assert solar_converted.getDay() == day
