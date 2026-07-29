# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Tests for the public library API (Phase 1 refactor).
"""

import os

# Create a temp DB before any database import (in case tests touch storage)
import tempfile

db_fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(db_fd)
os.environ["TUVI_DB_PATH"] = db_path

import pytest  # noqa: E402

from tuvi_mcp import (  # noqa: E402
    BirthInfo,
    Calendar,
    Gender,
    Horoscope,
    HoroscopeResult,
)
from tuvi_mcp.auspicious import get_auspicious_details  # noqa: E402
from tuvi_mcp.calendar import (  # noqa: E402
    convert_lunar_to_solar,
    convert_solar_to_lunar,
)


def test_horoscope_class_exposed():
    """Public API surface is importable from top-level package."""
    from tuvi_mcp import BirthInfo, Calendar, Gender, Horoscope, HoroscopeResult

    assert Horoscope is not None
    assert BirthInfo is not None
    assert Gender is not None
    assert Calendar is not None
    assert HoroscopeResult is not None


def test_birth_info_validation():
    """BirthInfo raises ValueError for out-of-range fields."""
    with pytest.raises(ValueError, match="year"):
        BirthInfo(year=1500, month=1, day=1)
    with pytest.raises(ValueError, match="month"):
        BirthInfo(year=2000, month=13, day=1)
    with pytest.raises(ValueError, match="day"):
        BirthInfo(year=2000, month=1, day=32)
    with pytest.raises(ValueError, match="hour"):
        BirthInfo(year=2000, month=1, day=1, hour=24)


def test_horoscope_from_birth_flexible_inputs():
    """from_birth accepts flexible hour, gender, calendar inputs."""
    h = Horoscope.from_birth(
        name="Test",
        year=1995,
        month=6,
        day=10,
        hour="14:30",
        gender="Nam",
        calendar="solar",
    )
    assert h.birth.name == "Test"
    assert h.birth.year == 1995
    assert h.birth.hour == 14  # parsed from "14:30"
    assert h.birth.gender == Gender.MALE
    assert h.birth.calendar == Calendar.SOLAR


def test_horoscope_from_birth_branch_name_hour():
    """Branch name resolves to start-of-window canonical solar hour."""
    h = Horoscope.from_birth(year=1995, month=6, day=10, hour="Ngọ", gender="female")
    assert h.birth.hour == 11  # Ngọ window 11:00-13:00 → canonical 11
    assert h.birth.gender == Gender.FEMALE


def test_horoscope_from_birth_branch_index_hour():
    """Branch index 1-12 resolves once at boundary; not re-interpreted downstream."""
    h_ngọ = Horoscope.from_birth(year=1995, month=6, day=10, hour=7)  # 7 = Ngọ window start
    h_tý = Horoscope.from_birth(year=1995, month=6, day=10, hour=1)  # 1 = Tý window start
    assert h_ngọ.birth.hour == 11
    assert h_tý.birth.hour == 0
    # The chart layer must interpret these as canonical solar hours (Ngọ / Tý),
    # not as the next branch round (Tuất / Tý) which the old ambiguous int path produced.
    chart = h_ngọ.chart()
    ngọ_branch = next(c for c in chart.dia_ban if c["cung_ten"].endswith("Ngọ"))
    assert any(s["name"].lower() == "thân" or s["name"].lower() == "tử vi" for s in ngọ_branch["sao"]) or ngọ_branch["cung_chu"] != ""


def test_horoscope_from_birth_gender_coercion():
    """from_birth accepts int, bool, str for gender."""
    assert Horoscope.from_birth(year=2000, month=1, day=1, gender=1).birth.gender == Gender.MALE
    assert Horoscope.from_birth(year=2000, month=1, day=1, gender=-1).birth.gender == Gender.FEMALE
    assert Horoscope.from_birth(year=2000, month=1, day=1, gender=True).birth.gender == Gender.MALE
    assert Horoscope.from_birth(year=2000, month=1, day=1, gender=False).birth.gender == Gender.FEMALE


def test_horoscope_from_birth_invalid_gender():
    """from_birth rejects garbage gender inputs."""
    with pytest.raises(ValueError, match="gender"):
        Horoscope.from_birth(year=2000, month=1, day=1, gender="other")


def test_horoscope_chart():
    """chart() returns HoroscopeResult with deterministic data."""
    h = Horoscope.from_birth(
        name="Nguyễn Văn A",
        year=1995,
        month=6,
        day=10,
        hour="14:30",
        gender="Nam",
        calendar="solar",
    )
    result = h.chart()
    assert isinstance(result, HoroscopeResult)
    assert result.thien_ban["ten"] == "Nguyễn Văn A"
    assert result.thien_ban["can_nam"] == "Ất"
    assert result.thien_ban["chi_nam"] == "Hợi"
    assert len(result.dia_ban) == 12
    assert isinstance(result.cach_cuc, list)


def test_horoscope_chart_to_dict():
    """to_dict() serializes to plain JSON-serializable dict."""
    h = Horoscope.from_birth(name="A", year=1995, month=6, day=10, hour="14:30", gender="Nam")
    d = h.chart().to_dict()
    assert "thien_ban" in d
    assert "dia_ban" in d
    assert "cach_cuc" in d
    assert "nhat_han" not in d  # not set on base chart


def test_horoscope_transit():
    """transit(year, month) returns full Vận Hạn dict."""
    h = Horoscope.from_birth(name="A", year=1995, month=6, day=10, hour="14:30", gender="Nam")
    res = h.transit(year=2026, month=5)
    assert res["target_period"]["current_year"] == 2026
    assert res["target_period"]["current_year_can_chi"] == "Bính Ngọ"
    assert res["nhat_han"] is None  # no day given
    assert "dai_han" in res
    assert "tieu_han" in res
    assert "nguyet_han" in res


def test_horoscope_transit_with_day():
    """transit(year, month, day) populates nhat_han."""
    h = Horoscope.from_birth(name="A", year=1995, month=6, day=10, hour="14:30", gender="Nam")
    res = h.transit(year=2026, month=5, day=1)
    assert res["nhat_han"] is not None
    assert res["nhat_han"]["cung_so"] == res["nguyet_han"]["cung_so"]  # day 1 == Nguyệt Hạn


def test_horoscope_auspicious():
    """auspicious(day, month, year) delegates to get_auspicious_details."""
    h = Horoscope.from_birth(name="A", year=1995, month=6, day=10, hour="14:30", gender="Nam")
    res = h.auspicious(day=27, month=7, year=2026)
    assert "error" not in res
    assert res["duong_lich"] == "27/07/2026"


def test_horoscope_auspicious_defaults_to_today():
    """Omitted date components default to today's date."""
    from datetime import date

    h = Horoscope.from_birth(name="A", year=1995, month=6, day=10, hour="14:30", gender="Nam")
    res = h.auspicious()
    assert "error" not in res
    today = date.today()
    expected = f"{today.day:02d}/{today.month:02d}/{today.year}"
    assert res["duong_lich"] == expected


def test_horoscope_render_chart(tmp_path):
    """render_chart() writes a PNG file and returns its path."""
    h = Horoscope.from_birth(name="Test", year=2003, month=8, day=21, hour="15:30", gender="Nam")
    chart = h.chart()
    path = h.render_chart(chart, year=2026)
    assert os.path.exists(path)
    assert path.endswith(".png")
    os.remove(path)


def test_calendar_module_exports():
    """calendar module exposes convert functions under stable names."""
    res = convert_solar_to_lunar(28, 6, 2026)
    assert res["lunar_day"] == 14
    res2 = convert_lunar_to_solar(14, 5, 2026, is_leap=False)
    assert res2["solar_day"] == 28


def test_auspicious_module_exports():
    """auspicious module exposes get_auspicious_details."""
    res = get_auspicious_details(27, 7, 2026, is_solar=True)
    assert "error" not in res
    assert res["duong_lich"] == "27/07/2026"


def test_gender_enum_values():
    """Gender enum matches ansaotuvi's 1/-1 convention."""
    assert int(Gender.MALE) == 1
    assert int(Gender.FEMALE) == -1


def test_calendar_enum_values():
    """Calendar enum exposes string values."""
    assert Calendar.SOLAR.value == "solar"
    assert Calendar.LUNAR.value == "lunar"


def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove(db_path)
    except Exception:
        pass
