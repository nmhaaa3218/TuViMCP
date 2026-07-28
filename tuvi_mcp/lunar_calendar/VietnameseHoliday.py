# -*- coding: utf-8 -*-
"""
Vietnamese Traditional & National Holiday Evaluator (compat shim).

DEPRECATED: prefer `VnHolidayRegistry` (in `vn_holidays.py`). This module is
preserved for backwards compatibility and routes through the new registry.
"""
from __future__ import annotations

from .vn_holidays import VnHolidayRegistry


class VietnameseHoliday:
    """Backwards-compatible facade over `VnHolidayRegistry`."""

    @staticmethod
    def get_lunar_holiday(month: int, day: int, is_leap: bool = False) -> str | None:
        return VnHolidayRegistry.get_lunar(month, day, is_leap=is_leap)

    @staticmethod
    def get_solar_holiday(month: int, day: int) -> str | None:
        return VnHolidayRegistry.get_solar(month, day)


__all__ = ["VietnameseHoliday"]