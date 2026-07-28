# -*- coding: utf-8 -*-
"""
Conversion round-trip + ref-pattern adoption tests (Phase 6 surface).

Covers:
  - solar → lunar → solar identity for fixed sample dates
  - `Lunar.get_full_info()` returns a typed `LunarInfo`
  - `Lunar.check_age_conflict`, `get_travel_direction`, `check_travel_hour`,
    `find_good_days` exist and behave sanely
"""

import pytest

from tuvi_mcp.lunar_calendar import Lunar, Solar
from tuvi_mcp.lunar_calendar.lunar_types import LunarInfo

SAMPLES = [
    (14, 2, 2024),
    (28, 6, 2026),
    (10, 3, 2025),
    (15, 8, 2024),
    (23, 12, 2024),
    (1, 1, 2025),
    (30, 4, 1975),
    (2, 9, 2025),
]


@pytest.mark.parametrize("day,month,year", SAMPLES)
def test_solar_lunar_solar_roundtrip(day, month, year):
    """Round-tripping a Solar date through Lunar must return the same Solar date."""
    solar = Solar.fromYmd(year, month, day)
    lunar = solar.getLunar()
    solar_back = lunar.getSolar()
    assert (solar_back.getYear(), solar_back.getMonth(), solar_back.getDay()) == (
        year,
        month,
        day,
    ), f"Roundtrip drift on {day}/{month}/{year}"


@pytest.mark.parametrize("day,month,year", SAMPLES)
def test_lunar_solar_lunar_roundtrip(day, month, year):
    """Round-tripping a Lunar date through Solar must return the same Lunar date."""
    solar = Solar.fromYmd(year, month, day)
    lunar = solar.getLunar()
    ld, lm, ly = (
        lunar.getDay(),
        abs(lunar.getMonth()),
        lunar.getYear(),
    )
    solar_back = Solar.fromYmd(year, month, day)
    lunar_back = solar_back.getLunar()
    assert lunar_back.getDay() == ld
    assert abs(lunar_back.getMonth()) == lm
    assert lunar_back.getYear() == ly


def test_get_full_info_returns_lunar_info():
    """Lunar.get_full_info returns a typed LunarInfo dataclass."""
    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    info = lunar.get_full_info()
    assert isinstance(info, LunarInfo)
    assert info.solar.day == 14
    assert info.solar.month == 6
    assert info.solar.year == 2026
    assert info.lunar.day >= 1
    assert info.can_chi.year != ""
    assert info.can_chi.day != ""
    assert info.twenty_eight_mansions != ""
    assert info.god_directions != {}


def test_check_age_conflict_returns_list():
    """check_age_conflict returns a list of conflicting ages."""
    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    conflicts = lunar.check_age_conflict(birth_year=1990, target_year=2026)
    assert isinstance(conflicts, list)
    for age in conflicts:
        assert isinstance(age, int)


def test_get_travel_direction_returns_string():
    """get_travel_direction returns a non-empty string."""
    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    direction = lunar.get_travel_direction()
    assert isinstance(direction, str)
    assert direction != ""


def test_check_travel_hour_returns_string():
    """check_travel_hour returns Hoàng Đạo or Hắc Đạo."""
    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    for hour in [0, 6, 12, 18, 23]:
        verdict = lunar.check_travel_hour(hour)
        assert verdict in ("Hoàng Đạo", "Hắc Đạo", "N/A")


def test_find_good_days_filters_hoang_dao():
    """find_good_days only returns Hoàng Đạo days in the requested range."""
    start = Solar.fromYmd(2026, 6, 1)
    end = Solar.fromYmd(2026, 6, 30)
    good = Lunar.find_good_days(start, end)
    assert all(isinstance(d, Solar) for d in good)
    for d in good:
        assert d.getLunar().getDayTianShenType() == "Hoàng Đạo"
        assert start.isBefore(d) or d == start
        assert end.isAfter(d) or d == end


def test_find_good_days_accepts_tuple_dates():
    """find_good_days accepts (day, month, year) tuples."""
    good = Lunar.find_good_days((1, 6, 2026), (30, 6, 2026))
    assert isinstance(good, list)
    assert len(good) > 0
    for d in good:
        assert isinstance(d, Solar)
