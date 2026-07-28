# -*- coding: utf-8 -*-
"""
Typed result contracts for the Vietnamese lunar calendar API.

Mirrors the structure of the `pyvnlunar` reference (`lunar_types.py`) while
staying native-Vietnamese: no Lục Diệu, no Foto/Tao, no Chinese-only fields.

Library-only — these dataclasses are intended for direct Python callers, not
exposed through the MCP tool surface.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SolarInfo:
    day: int
    month: int
    year: int
    day_of_week: str = ""
    formatted: str = ""


@dataclass(frozen=True)
class LunarDateInfo:
    day: int
    month: int
    year: int
    leap: bool = False
    month_name: str = ""
    sheng_xiao: str = ""


@dataclass(frozen=True)
class CanChiInfo:
    year: str = ""
    month: str = ""
    day: str = ""
    hour: str = ""
    year_element: str = ""
    day_element_gan: str = ""
    day_element_zhi: str = ""


@dataclass(frozen=True)
class LunarInfo:
    """Unified snapshot returned by `Lunar.get_full_info()`."""

    solar: SolarInfo
    lunar: LunarDateInfo
    can_chi: CanChiInfo
    twelve_stars: str = ""
    twelve_constructions: str = ""
    twelve_gods: str = ""
    twenty_eight_mansions: str = ""
    twenty_eight_mansions_luck: str = ""
    nayin: str = ""
    day_type: str = ""
    conflicting_ages: list[int] = field(default_factory=list)
    day_position_xi: str = ""
    day_position_cai: str = ""
    day_position_fu: str = ""
    day_position_yang_gui: str = ""
    day_position_yin_gui: str = ""
    chong: str = ""
    sha: str = ""
    god_directions: dict[str, str] = field(default_factory=dict)
    auspicious_hours: list[str] = field(default_factory=list)
    festivals: list[str] = field(default_factory=list)
    vietnamese_festivals: list[str] = field(default_factory=list)
    jie_qi_current: str = ""
    jie_qi_next: str = ""


__all__ = [
    "SolarInfo",
    "LunarDateInfo",
    "CanChiInfo",
    "LunarInfo",
]
