# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Internal Solar <-> Lunar calendar conversion routines.

Routed through ``tuvi_mcp._lunar_calendar.util.VnCalendarUtil`` — the
unified astronomical engine (Ho Ngọc Đức / Meeus, UTC+7).
"""

from __future__ import annotations


def convert_solar_to_lunar(day: int, month: int, year: int, timezone: int = 7) -> dict:
    """Convert a Solar date (Dương lịch) to the corresponding Lunar date (Âm lịch)."""
    from ._lunar_calendar.util.VnCalendarUtil import solar_to_lunar_vn

    try:
        res = solar_to_lunar_vn(day, month, year, time_zone=float(timezone))
        return {
            "lunar_day": res[0],
            "lunar_month": res[1],
            "lunar_year": res[2],
            "lunar_leap": bool(res[3]),
            "formatted": f"{res[0]}/{res[1]}/{res[2]}" + (" (nhận)" if res[3] else ""),
        }
    except Exception as e:
        return {"error": f"Failed to convert Solar to Lunar: {str(e)}"}


def convert_lunar_to_solar(day: int, month: int, year: int, is_leap: bool = False, timezone: int = 7) -> dict:
    """Convert a Lunar date (Âm lịch) to the corresponding Solar date (Dương lịch).

    Leap-month validation uses the engine's own helpers before delegating
    the conversion.
    """
    from ._lunar_calendar.util.VnCalendarUtil import (
        getLeapMonthOffset,
        getLunarMonth11,
        lunar_to_solar_vn,
    )

    try:
        if is_leap:
            if month < 11:
                a11 = getLunarMonth11(year - 1, timezone)
                b11 = getLunarMonth11(year, timezone)
            else:
                a11 = getLunarMonth11(year, timezone)
                b11 = getLunarMonth11(year + 1, timezone)

            if b11 - a11 <= 365:
                return {"error": f"Lunar year {year} is not a leap year. No leap month exists."}

            leapOff = getLeapMonthOffset(a11, timezone)
            leapM = leapOff - 2
            if leapM < 0:
                leapM += 12
            if month != leapM:
                return {
                    "error": (
                        f"Lunar month {month} is not the leap month of year {year}. The leap month is month {leapM}."
                    )
                }

        leap_val = 1 if is_leap else 0
        res = lunar_to_solar_vn(day, month, year, leap_val, time_zone=float(timezone))
        if res == [0, 0, 0]:
            return {"error": "Invalid lunar date or invalid leap month configuration."}
        return {
            "solar_day": res[0],
            "solar_month": res[1],
            "solar_year": res[2],
            "formatted": f"{res[0]}/{res[1]}/{res[2]}",
        }
    except Exception as e:
        return {"error": f"Failed to convert Lunar to Solar: {str(e)}"}


__all__ = ["convert_lunar_to_solar", "convert_solar_to_lunar"]
