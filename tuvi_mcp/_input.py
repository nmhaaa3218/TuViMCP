# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Internal input parsing and validation utilities.

Implements:
    - Branch / Can name maps (BRANCH_NAMES, CAN_NAMES, HOUR_BRANCH_MAP)
    - LUC_HOP_MAP (6-Harmony pairs)
    - parse_hour / parse_solar_hour / parse_gender / map_hour_of_day_to_branch
    - validate_birth_parameters / validate_transit_period / validate_calendar_convert
    - get_max_days_in_solar_month / MONTH_NAMES
"""

from __future__ import annotations

import calendar
import re
from datetime import datetime

BRANCH_NAMES = ["", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

CAN_NAMES = ["", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

LUC_HOP_MAP = {
    1: 2,
    2: 1,  # Tý - Sửu
    3: 12,
    12: 3,  # Dần - Hợi
    4: 11,
    11: 4,  # Mão - Tuất
    5: 10,
    10: 5,  # Thìn - Dậu
    6: 9,
    9: 6,  # Tỵ - Thân
    7: 8,
    8: 7,  # Ngọ - Mùi
}

HOUR_BRANCH_MAP = {
    "tý": 1,
    "sửu": 2,
    "dần": 3,
    "mão": 4,
    "thìn": 5,
    "tỵ": 6,
    "ngọ": 7,
    "mùi": 8,
    "thân": 9,
    "dậu": 10,
    "tuất": 11,
    "hợi": 12,
}

MONTH_NAMES = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_max_days_in_solar_month(month: int, year: int) -> int:
    """Return maximum days in a given solar month and year (e.g. 29 for Feb 2024, 28 for Feb 2025)."""
    try:
        return calendar.monthrange(year, month)[1]
    except Exception:
        return 31


def parse_solar_hour(hour_val) -> int | None:
    """Extract the solar hour (0-23) if the input represents a time of day,
    or None if it is a direct branch index or branch name.
    """
    if isinstance(hour_val, (int, float)):
        # If it is direct branch index (1-12)
        if 1 <= hour_val <= 12 and int(hour_val) == hour_val:
            return None
        return int(hour_val) % 24

    if isinstance(hour_val, str):
        val = hour_val.strip().lower()
        # If it contains an earthly branch name, it is a branch-based input rather than a solar hour
        for k in HOUR_BRANCH_MAP.keys():
            if k in val:
                return None

        # Check if PM/AM is present
        is_pm = False
        if "pm" in val:
            is_pm = True
            val = val.replace("pm", "").strip()
        elif "am" in val:
            val = val.replace("am", "").strip()

        # Match HH:MM or HHhMM or HH
        match = re.search(r"(\d+)(?::|h| |$)", val)
        if match:
            h = int(match.group(1))
            if is_pm and h < 12:
                h += 12
            elif not is_pm and h == 12:
                h = 0
            return h % 24

    return None


def parse_hour(hour_val) -> int:
    """Parse the hour input into the 1-indexed Earthly Branch index (1-12).

    Allows:
        - Integer/float 1-12 directly representing branch index.
        - Integer/float representing hour of day (0-23).
        - String name of branch (e.g. "Tý", "ngo").
        - String representing time of day (e.g. "14:30", "11h15").
    """
    if isinstance(hour_val, (int, float)):
        if 1 <= hour_val <= 12 and int(hour_val) == hour_val:
            return int(hour_val)
        h = int(hour_val) % 24
        return map_hour_of_day_to_branch(h)

    if isinstance(hour_val, str):
        val = hour_val.strip().lower()
        for k, v in HOUR_BRANCH_MAP.items():
            if k in val:
                return v

        match = re.search(r"(\d+)(?::|h| |$)", val)
        if match:
            h = int(match.group(1)) % 24
            return map_hour_of_day_to_branch(h)

        try:
            val_int = int(val)
            if 1 <= val_int <= 12:
                return val_int
            return map_hour_of_day_to_branch(val_int % 24)
        except ValueError:
            pass

    return 1


def map_hour_of_day_to_branch(h: int) -> int:
    """Map solar hour (0-23) to 1-indexed Earthly Branch (1-12)."""
    if h == 23 or h == 0:
        return 1  # Tý (23:00 - 00:59)
    elif h == 1 or h == 2:
        return 2  # Sửu (01:00 - 02:59)
    elif h == 3 or h == 4:
        return 3  # Dần (03:00 - 04:59)
    elif h == 5 or h == 6:
        return 4  # Mão (05:00 - 06:59)
    elif h == 7 or h == 8:
        return 5  # Thìn (07:00 - 08:59)
    elif h == 9 or h == 10:
        return 6  # Tỵ (09:00 - 10:59)
    elif h == 11 or h == 12:
        return 7  # Ngọ (11:00 - 12:59)
    elif h == 13 or h == 14:
        return 8  # Mùi (13:00 - 14:59)
    elif h == 15 or h == 16:
        return 9  # Thân (15:00 - 16:59)
    elif h == 17 or h == 18:
        return 10  # Dậu (17:00 - 18:59)
    elif h == 19 or h == 20:
        return 11  # Tuất (19:00 - 20:59)
    elif h == 21 or h == 22:
        return 12  # Hợi (21:00 - 22:59)
    return 1


def parse_gender(gender_val) -> int:
    """Map gender input to 1 (Male) or -1 (Female)."""
    if isinstance(gender_val, (int, float)):
        return 1 if int(gender_val) >= 1 else -1
    if isinstance(gender_val, bool):
        return 1 if gender_val else -1
    if isinstance(gender_val, str):
        val = gender_val.strip().lower()
        if val in ("nam", "male", "m", "1", "true"):
            return 1
        if val in ("nữ", "nu", "female", "f", "-1", "false"):
            return -1
    return -1


def validate_birth_parameters(
    day: int, month: int, year: int, hour_val, gender_val, is_solar: bool = True
) -> dict | None:
    """Validate birth parameters. Returns None if valid, else a structured error dict."""
    errors = []
    suggestions = {}

    # 1. Validate year
    if not isinstance(year, int) or isinstance(year, bool) or year < 1800 or year > 2100:
        errors.append(f"Invalid year '{year}'. Year must be an integer between 1800 and 2100.")
        suggestions["year"] = "Provide a 4-digit integer year between 1800 and 2100 (e.g., 1995, 2004)."

    # 2. Validate month
    if not isinstance(month, int) or isinstance(month, bool) or month < 1 or month > 12:
        errors.append(f"Invalid month '{month}'. Month must be an integer from 1 to 12.")
        suggestions["month"] = "Provide an integer month between 1 and 12."

    # 3. Validate day and calendar existence
    if not isinstance(day, int) or isinstance(day, bool) or day < 1 or day > 31:
        errors.append(f"Invalid day '{day}'. Day must be an integer from 1 to 31.")
        suggestions["day"] = "Provide a valid day of the month (1-31)."
    elif isinstance(month, int) and 1 <= month <= 12 and isinstance(year, int) and 1800 <= year <= 2100:
        if is_solar:
            try:
                datetime(year, month, day)
            except ValueError:
                max_d = get_max_days_in_solar_month(month, year)
                m_name = MONTH_NAMES[month]
                errors.append(f"Unreal date '{day}/{month}/{year}' ({m_name} {day}, {year} does not exist).")
                suggestions["day"] = (
                    f"Provide a real calendar date. {m_name} {year} has a maximum of {max_d} days (1-{max_d})."
                )
        else:
            from ._calendar import convert_lunar_to_solar  # local import to avoid cycle

            solar_res = convert_lunar_to_solar(day, month, year, False)
            if "error" in solar_res:
                errors.append(f"Unreal Lunar date '{day}/{month}/{year}' ({solar_res['error']}).")
                suggestions["day"] = f"Verify the specified Lunar day exists in Lunar month {month}/{year}."

    # 4. Validate gender_val
    if isinstance(gender_val, str):
        val = gender_val.strip().lower()
        valid_genders = {"nam", "nữ", "nu", "male", "female", "m", "f", "1", "-1", "true", "false"}
        if val not in valid_genders:
            errors.append(f"Invalid gender_val '{gender_val}'.")
            suggestions["gender_val"] = "Must be one of: 'Nam', 'Nữ', 'male', 'female'."
    elif not isinstance(gender_val, (int, float, bool)):
        errors.append(f"Invalid gender_val type '{type(gender_val).__name__}'.")
        suggestions["gender_val"] = "Must be a string ('Nam' or 'Nữ'), integer (1 or -1), or boolean."

    # 5. Validate hour_val
    if isinstance(hour_val, (int, float)) and not isinstance(hour_val, bool):
        if not (1 <= hour_val <= 12 and int(hour_val) == hour_val) and not (0 <= hour_val <= 23):
            errors.append(f"Invalid numeric hour_val '{hour_val}'.")
            suggestions["hour_val"] = "Must be an integer branch index (1-12) or hour of day (0-23)."
    elif isinstance(hour_val, str):
        val = hour_val.strip().lower()
        matched_branch = any(k in val for k in HOUR_BRANCH_MAP.keys())
        matched_time = re.search(r"(\d+)(?::|h| |$)", val) is not None
        if not matched_branch and not matched_time:
            try:
                v_int = int(val)
                if not (1 <= v_int <= 12 or 0 <= v_int <= 23):
                    errors.append(f"Invalid hour_val '{hour_val}'.")
                    suggestions["hour_val"] = (
                        "Must be a time string ('14:30'), Earthly Branch name ('Ngọ'), or branch index (1-12)."
                    )
            except ValueError:
                errors.append(f"Invalid hour_val '{hour_val}'.")
                suggestions["hour_val"] = (
                    "Must be a time string ('14:30'), Earthly Branch name ('Ngọ'), or branch index (1-12)."
                )
    elif hour_val is not None:
        errors.append(f"Invalid hour_val type '{type(hour_val).__name__}'.")
        suggestions["hour_val"] = (
            "Must be a time string ('14:30'), Earthly Branch name ('Ngọ'), or branch index (1-12)."
        )

    if errors:
        return {
            "error": "Input validation failed",
            "error_code": "INVALID_INPUT_PARAMETER",
            "details": errors,
            "suggestions": suggestions,
        }
    return None


def validate_transit_period(
    current_year: int | None = None, current_month: int = 1, current_day: int | None = None
) -> dict | None:
    """Validate target transit period parameters."""
    errors = []
    suggestions = {}

    if current_year is not None:
        if (
            not isinstance(current_year, int)
            or isinstance(current_year, bool)
            or current_year < 1800
            or current_year > 2100
        ):
            errors.append(f"Invalid current_year '{current_year}'. Year must be an integer between 1800 and 2100.")
            suggestions["current_year"] = "Provide a 4-digit integer year between 1800 and 2100 (e.g., 2026)."

    if current_month is not None:
        if (
            not isinstance(current_month, int)
            or isinstance(current_month, bool)
            or current_month < 1
            or current_month > 12
        ):
            errors.append(f"Invalid current_month '{current_month}'. Month must be an integer between 1 and 12.")
            suggestions["current_month"] = "Provide an integer Lunar month between 1 and 12."

    if current_day is not None:
        if not isinstance(current_day, int) or isinstance(current_day, bool) or current_day < 1 or current_day > 30:
            errors.append(f"Invalid current_day '{current_day}'. Day must be an integer between 1 and 30.")
            suggestions["current_day"] = "Provide an integer Lunar day between 1 and 30."

    if errors:
        return {
            "error": "Input validation failed",
            "error_code": "INVALID_INPUT_PARAMETER",
            "details": errors,
            "suggestions": suggestions,
        }
    return None


_TZ_STR_RE = re.compile(r"^([+-])?(\d{1,2})(?::30)?$")


def coerce_timezone(value, default: float = 7.0) -> tuple[float | None, dict | None]:
    """Normalize a timezone argument to a float offset in hours.

    Accepts:
        - ``int``          → ``float(N)``
        - ``float``        → only if integer-valued (e.g. ``7.0``); fractions rejected
        - ``str`` matching ``^([+-])?(\\d{1,2})(?::30)?$`` → ``±N.0`` or ``±N.5``
        - ``None``         → returns ``default``

    Any other input is rejected with a structured error dict. Range guard:
    ``-12 <= offset <= 14``.

    Returns:
        ``(offset, None)`` on success; ``(None, error_dict)`` on validation failure.
    """
    if value is None:
        return default, None
    if isinstance(value, bool):
        return None, _tz_error("Timezone must be int or 'h:30' string.", value)
    if isinstance(value, int):
        offset = float(value)
    elif isinstance(value, float):
        if not value.is_integer():
            return None, _tz_error("Fractional float not allowed. Use 'h:30' form.", value)
        offset = value
    elif isinstance(value, str):
        m = _TZ_STR_RE.match(value.strip())
        if not m:
            return None, _tz_error("Timezone string must be integer hour or 'h:30'.", value)
        sign = -1.0 if m.group(1) == "-" else 1.0
        hours = int(m.group(2))
        stripped = value.strip()
        minutes = 0.5 if stripped.endswith(":30") else 0.0
        offset = sign * (hours + minutes)
    else:
        return None, _tz_error("Timezone must be int or 'h:30' string.", value)

    if offset < -12 or offset > 14:
        return None, _tz_error("Timezone offset must be between -12 and 14.", offset)
    return offset, None


def _tz_error(msg: str, value) -> dict:
    return {
        "error": "Input validation failed",
        "error_code": "INVALID_INPUT_PARAMETER",
        "details": [f"Invalid timezone '{value}'. {msg}"],
        "suggestions": {
            "timezone": "Provide an integer hour (e.g. 7 for ICT) or 'h:30' string (e.g. '7:30')."
        },
    }


def validate_calendar_convert(
    day: int, month: int, year: int, from_solar: bool = True, lunar_leap: bool = False, timezone: int = 7
) -> dict | None:
    """Validate calendar conversion input parameters."""
    errors = []
    suggestions = {}

    if not isinstance(year, int) or isinstance(year, bool) or year < 1800 or year > 2100:
        errors.append(f"Invalid year '{year}'. Year must be an integer between 1800 and 2100.")
        suggestions["year"] = "Provide a 4-digit integer year between 1800 and 2100."

    if not isinstance(month, int) or isinstance(month, bool) or month < 1 or month > 12:
        errors.append(f"Invalid month '{month}'. Month must be an integer between 1 and 12.")
        suggestions["month"] = "Provide an integer month between 1 and 12."

    if not isinstance(day, int) or isinstance(day, bool) or day < 1 or day > 31:
        errors.append(f"Invalid day '{day}'. Day must be an integer between 1 and 31.")
        suggestions["day"] = "Provide an integer day between 1 and 31."
    elif isinstance(month, int) and 1 <= month <= 12 and isinstance(year, int) and 1800 <= year <= 2100:
        if from_solar:
            try:
                datetime(year, month, day)
            except ValueError:
                max_d = get_max_days_in_solar_month(month, year)
                m_name = MONTH_NAMES[month]
                errors.append(f"Unreal date '{day}/{month}/{year}' ({m_name} {day}, {year} does not exist).")
                suggestions["day"] = (
                    f"Provide a real calendar date. {m_name} {year} has a maximum of {max_d} days (1-{max_d})."
                )
        else:
            from ._calendar import convert_lunar_to_solar  # local import to avoid cycle

            solar_res = convert_lunar_to_solar(day, month, year, lunar_leap, timezone)
            if "error" in solar_res:
                errors.append(f"Unreal Lunar date '{day}/{month}/{year}' ({solar_res['error']}).")
                suggestions["day"] = "Verify the maximum days for the specified Lunar month and year."

    if not isinstance(timezone, (int, float)) or timezone < -12 or timezone > 14:
        errors.append(f"Invalid timezone '{timezone}'. Timezone offset must be between -12 and 14.")
        suggestions["timezone"] = "Provide a numeric UTC offset (default 7 for ICT)."

    if errors:
        return {
            "error": "Input validation failed",
            "error_code": "INVALID_INPUT_PARAMETER",
            "details": errors,
            "suggestions": suggestions,
        }
    return None


__all__ = [
    "BRANCH_NAMES",
    "CAN_NAMES",
    "HOUR_BRANCH_MAP",
    "LUC_HOP_MAP",
    "MONTH_NAMES",
    "get_max_days_in_solar_month",
    "map_hour_of_day_to_branch",
    "parse_gender",
    "parse_hour",
    "parse_solar_hour",
    "coerce_timezone",
    "validate_birth_parameters",
    "validate_calendar_convert",
    "validate_transit_period",
]
