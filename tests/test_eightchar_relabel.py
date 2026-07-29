# -*- coding: utf-8 -*-
"""
EightChar subpackage relabel + relocation tests.

Asserts that the Tứ Trụ / Bát Tự system is reachable only via the explicitly
labeled `sino_vn_huyen_hoc` subpackage, and that the module docstring
discloses its Sino-VN huyền học (non-native-folk) origin.
"""


def test_eightchar_module_docstring_discloses_origin():
    """EightChar module docstring must call out Sino-VN huyền học origin."""
    from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar

    doc = (EightChar.__doc__ or "")
    assert "Sino-Vietnamese" in doc or "Sino-VN" in doc
    assert "Chinese" in doc or "Trung Hoa" in doc or "Trung Quốc" in doc
    assert "tín ngưỡng dân gian" in doc or "folk religion" in doc


def test_eightchar_class_docstring_discloses_origin():
    """EightChar class docstring must call out origin."""
    from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar

    doc = (EightChar.__doc__ or "")
    assert "Đông Á" in doc or "Trung Hoa" in doc or "Chinese" in doc
    assert "tín ngưỡng dân gian" in doc or "folk religion" in doc


def test_subpackage_docstring_explains_sino_vn_categorization():
    """The `sino_vn_huyen_hoc` package docstring explains why it's separated."""
    import tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc as pkg

    doc = (pkg.__doc__ or "")
    assert "Sino-Vietnamese" in doc or "Sino-VN" in doc
    assert "tín ngưỡng dân gian" in doc or "folk religion" in doc
    assert "Tứ Bất Tử" in doc  # explicitly disambiguates from "Tứ Trụ"


def test_eightchar_subclasses_resolve():
    """DaYun / XiaoYun / LiuNian / LiuYue / Yun still resolve."""
    from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc.eightchar import (
        DaYun,
        LiuNian,
        LiuYue,
        XiaoYun,
        Yun,
    )

    assert all([DaYun, LiuNian, LiuYue, XiaoYun, Yun])


def test_lunar_get_eight_char_works_through_new_path():
    """Lunar.getEightChar still returns a usable EightChar instance."""
    from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar

    from tuvi_mcp.lunar_calendar import Solar

    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    ec = lunar.getEightChar()
    assert isinstance(ec, EightChar)
    # Year / month / day / time pillars must all be non-empty strings
    assert ec.getYear() != ""
    assert ec.getMonth() != ""
    assert ec.getDay() != ""
    assert ec.getTime() != ""
