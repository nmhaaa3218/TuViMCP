# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. The localized calendar engine lives at
``tuvi_mcp._lunar_calendar``. This module re-exports the public surface
and aliases each submodule so legacy imports
``from tuvi_mcp.lunar_calendar.X import ...`` keep working.
"""

import sys as _sys

from .. import _lunar_calendar as _lc
from .._compat._aliases import install_module_aliases

# Eagerly import the public symbols; submodule paths (incl. nested
# packages like ``util`` and ``sino_vn_huyen_hoc``) get re-exported as
# ``sys.modules`` aliases by ``install_module_aliases`` below, so that
# legacy ``from tuvi_mcp.lunar_calendar.X.Y import Z`` still works
# without us ever re-exporting EightChar into this package's ``__dict__``.
from .._lunar_calendar import (  # noqa: F401
    Holiday,
    HolidayEntry,
    HolidayScope,
    JieQi,
    LichAm,
    LichDuong,
    Lunar,
    LunarMonth,
    LunarTime,
    LunarYear,
    NineStar,
    Solar,
    SolarHalfYear,
    SolarMonth,
    SolarSeason,
    SolarWeek,
    SolarYear,
    VietnameseHoliday,
    VnCalendarUtil,
    VnHolidayRegistry,
    lunar_types,  # noqa: F401
    vn_holidays,  # noqa: F401
)
from .._lunar_calendar import sino_vn_huyen_hoc as _lc_sino  # noqa: F401
from .._lunar_calendar import util as _lc_util  # noqa: F401

__version__ = "1.4.9"

__all__ = [
    "Holiday",
    "JieQi",
    "NineStar",
    "Solar",
    "SolarWeek",
    "SolarMonth",
    "SolarSeason",
    "SolarHalfYear",
    "SolarYear",
    "LunarTime",
    "Lunar",
    "LunarYear",
    "LunarMonth",
    "VnCalendarUtil",
    "VietnameseHoliday",
    "HolidayEntry",
    "HolidayScope",
    "VnHolidayRegistry",
    "LichAm",
    "LichDuong",
]

# Re-export submodule aliases so ``from tuvi_mcp.lunar_calendar.Lunar import ...``
# still resolves after we moved implementations to ``tuvi_mcp._lunar_calendar.*``.
install_module_aliases(__name__, _lc.__name__, _sys.modules)
