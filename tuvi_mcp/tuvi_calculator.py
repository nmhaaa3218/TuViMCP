# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. The 736-line implementation was split into:

    - ``tuvi_mcp._input``       — parsing, validation, string maps
    - ``tuvi_mcp._calendar``    — Solar <-> Lunar conversion
    - ``tuvi_mcp._chart``       — chart building pipeline
    - ``tuvi_mcp._transit``     — Vận Hạn / transit analysis

This module re-exports the public surface so existing imports keep working.
"""

from ._calendar import convert_lunar_to_solar, convert_solar_to_lunar
from ._chart import (
    SAO_ATTRIBUTE_MAP,
    adjust_date_for_late_ty,
    build_raw_chart,
    get_horoscope_chart,
    get_quan_he_hinh_hoc,
    serialize_sao,
)
from ._input import (
    BRANCH_NAMES,
    CAN_NAMES,
    HOUR_BRANCH_MAP,
    LUC_HOP_MAP,
    MONTH_NAMES,
    get_max_days_in_solar_month,
    map_hour_of_day_to_branch,
    parse_gender,
    parse_hour,
    parse_solar_hour,
    validate_birth_parameters,
    validate_calendar_convert,
    validate_transit_period,
)
from ._transit import calculate_transit_stars, get_van_han_analysis

__all__ = [
    "BRANCH_NAMES",
    "CAN_NAMES",
    "HOUR_BRANCH_MAP",
    "LUC_HOP_MAP",
    "MONTH_NAMES",
    "SAO_ATTRIBUTE_MAP",
    "adjust_date_for_late_ty",
    "build_raw_chart",
    "calculate_transit_stars",
    "convert_lunar_to_solar",
    "convert_solar_to_lunar",
    "get_horoscope_chart",
    "get_max_days_in_solar_month",
    "get_quan_he_hinh_hoc",
    "get_van_han_analysis",
    "map_hour_of_day_to_branch",
    "parse_gender",
    "parse_hour",
    "parse_solar_hour",
    "serialize_sao",
    "validate_birth_parameters",
    "validate_calendar_convert",
    "validate_transit_period",
]
