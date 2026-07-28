# -*- coding: utf-8 -*-
"""
Native-only surface guard.

Asserts that the default Vietnamese calendar surface does not leak Chinese /
foreign religious/almanac content. Items under `sino_vn_huyen_hoc/` (EightChar)
are intentionally permitted because they are documented as Sino-Vietnamese
huyền học, not native folk religion.
"""
import os
import re

import pytest

LUNAR_CALENDAR_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "tuvi_mcp",
    "lunar_calendar",
)
LUNAR_CALENDAR_DIR = os.path.abspath(LUNAR_CALENDAR_DIR)


BANNED_TERMS = [
    r"元始天尊",
    r"灵宝天尊",
    r"佛灭",
    r"先胜",
    r"先负",
    r"留连",
    r"友引",
    r"速喜",
    r"赤口",
    r"小吉",
    r"空亡",
    r"三元",
    r"五腊",
    r"三会",
    r"上元",
    r"中元",
    r"下元",
    r"玉皇大帝",
    r"太上老君",
    r"灶王爺",
    r"Bành Tổ",
    r"PengZu",
    r"thanksgiving",
    r"Thanksgiving",
    r"Thanksgiving",
    r"ShuJiu",
    r"getShuJiu",
    r"getSanFu",
    r"TaoUtil",
    r"FotoUtil",
    r"TaoFestival",
    r"FotoFestival",
    r"HolidayUtil",
    r"Lục Diệu",
    r"六曜",
]


def _iter_default_surface_files():
    for root, dirs, files in os.walk(LUNAR_CALENDAR_DIR):
        # Skip the Sino-VN huyen hoc subpackage on purpose.
        dirs[:] = [d for d in dirs if d != "sino_vn_huyen_hoc"]
        for f in files:
            if f.endswith(".py"):
                yield os.path.join(root, f)


def _strip_strings_and_comments(source: str) -> str:
    """Strip Python string literals and comments, leaving only executable code."""
    out = []
    i = 0
    n = len(source)
    while i < n:
        c = source[i]
        # Strip line comments
        if c == "#":
            while i < n and source[i] != "\n":
                i += 1
            continue
        # Strip triple-quoted strings (docstrings etc.)
        if c in ('"', "'") and i + 2 < n and source[i + 1] == c and source[i + 2] == c:
            quote = c * 3
            i += 3
            while i < n:
                if source[i] == "\\" and i + 1 < n:
                    i += 2
                    continue
                if source[i:i + 3] == quote:
                    i += 3
                    break
                i += 1
            continue
        # Strip single-quoted strings
        if c in ('"', "'"):
            quote = c
            i += 1
            while i < n and source[i] != "\n":
                if source[i] == "\\" and i + 1 < n:
                    i += 2
                    continue
                if source[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


@pytest.mark.parametrize("banned", BANNED_TERMS)
def test_default_surface_excludes_banned_term(banned):
    """No banned Chinese / foreign term appears in executable code of default surface.

    Strings and comments (including deprecation docstrings) are stripped before
    matching so legitimate migration notes are tolerated.
    """
    pattern = re.compile(banned)
    leaks = []
    for path in _iter_default_surface_files():
        with open(path, "r", encoding="utf-8") as fh:
            source = fh.read()
        code = _strip_strings_and_comments(source)
        for lineno, line in enumerate(code.splitlines(), start=1):
            if pattern.search(line):
                leaks.append(f"{path}:{lineno}: {line.rstrip()}")
    assert not leaks, "Banned Chinese/foreign content leaked into executable code:\n" + "\n".join(leaks)


def test_solar_util_has_no_western_zodiac():
    """SolarUtil.XING_ZUO removed in v1.4.9."""
    from tuvi_mcp.lunar_calendar.util.SolarUtil import SolarUtil

    assert not hasattr(SolarUtil, "XING_ZUO")


def test_solar_util_has_no_thanksgiving():
    """Lễ Tạ Ơn (US Thanksgiving) removed from WEEK_FESTIVAL in v1.4.9."""
    from tuvi_mcp.lunar_calendar.util.SolarUtil import SolarUtil

    assert "11-4-4" not in SolarUtil.WEEK_FESTIVAL


def test_lunar_util_has_no_peng_zu():
    """Peng Zu (Bành Tổ) constants emptied in v1.4.9."""
    from tuvi_mcp.lunar_calendar.util.LunarUtil import LunarUtil

    assert LunarUtil.PENG_ZU_GAN == ()
    assert LunarUtil.PENG_ZU_ZHI == ()


def test_lunar_util_has_no_liu_yao():
    """Lục Diệu (六曜) constant removed in v1.4.9."""
    from tuvi_mcp.lunar_calendar.util.LunarUtil import LunarUtil

    assert not hasattr(LunarUtil, "LIU_YAO")


def test_lunar_get_liu_yao_returns_none():
    """Lunar.getLiuYao() deprecated, returns None."""
    from tuvi_mcp.lunar_calendar import Solar

    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    assert lunar.getLiuYao() is None


def test_lunar_get_peng_zu_methods_removed():
    """Lunar.getPengZu* methods removed in v1.4.9."""
    from tuvi_mcp.lunar_calendar import Solar

    lunar = Solar.fromYmd(2026, 6, 14).getLunar()
    assert not hasattr(lunar, "getPengZuGan")
    assert not hasattr(lunar, "getPengZuZhi")


def test_deleted_modules_absent():
    """Tao / Foto / ShuJiu / Fu / FotoUtil / TaoUtil / HolidayUtil gone."""
    import importlib

    for mod in [
        "tuvi_mcp.lunar_calendar.Tao",
        "tuvi_mcp.lunar_calendar.TaoFestival",
        "tuvi_mcp.lunar_calendar.Foto",
        "tuvi_mcp.lunar_calendar.FotoFestival",
        "tuvi_mcp.lunar_calendar.ShuJiu",
        "tuvi_mcp.lunar_calendar.Fu",
        "tuvi_mcp.lunar_calendar.util.TaoUtil",
        "tuvi_mcp.lunar_calendar.util.FotoUtil",
        "tuvi_mcp.lunar_calendar.util.HolidayUtil",
    ]:
        with pytest.raises(ImportError):
            importlib.import_module(mod)


def test_eightchar_lives_under_sino_vn_huyen_hoc():
    """EightChar is now in the explicitly-labeled subpackage."""
    from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar

    assert EightChar.__module__ == "tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc.EightChar"


def test_default_lunar_calendar_exports_no_eightchar():
    """EightChar removed from default lunar_calendar exports; opt-in only."""
    import tuvi_mcp.lunar_calendar as pkg

    assert "EightChar" not in pkg.__dict__
