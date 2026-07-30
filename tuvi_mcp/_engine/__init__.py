#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
"""
from .AmDuong import (
    L2S,
    S2L,
    canChiGio,
    canChiNgay,
    dichCung,
    khoangCachCung,
    ngayThangNam,
    ngayThangNamCanChi,
    nguHanh,
    nguHanhNapAm,
    sinhKhac,
    thienCan,
    timCoThan,
    timCuc,
    timHoaLinh,
    timPhaToai,
    timThienKhoi,
    timThienMa,
    timThienQuanThienPhuc,
    timTrangSinh,
    timTuVi,
)
from .App import lapDiaBan
from .DiaBan import cungDiaBan, dacTinhSao, diaBan
from .Lich_HND import (
    NewMoon,
    SunLongitude,
    getLeapMonthOffset,
    getLunarMonth11,
    getNewMoonDay,
    getSunLongitude,
    jdFromDate,
    jdToDate,
)
from .Sao import Sao
from .ThienBan import lapThienBan

# ``Lich_EPHEM`` requires the optional ``ephem`` dependency. Importing it
# lazily keeps the public package importable in environments where the
# dependency is not installed (e.g. CI testing the chart-only path).
try:
    from .Lich_EPHEM import (
        find_new_moon_between,
        find_solar_terms_between,
        l2s,
        s2l,
        when_is_sun_at_degrees_longitude,
    )

    _HAS_EPHEM = True
    _ephem_err: Exception | None = None
except Exception as _err:  # pragma: no cover - import guarded
    _HAS_EPHEM = False
    _ephem_err = _err

__title__ = "ansaotuvi"
__version__ = "0.4.0"
__author__ = "Manh Ha Nguyen"
__author_email__ = "manh.ha.3218@gmail.com"
__license__ = "MIT License"

__all__ = [
    "S2L",
    "L2S",
    "lapDiaBan",
    "lapThienBan",
    "diaBan",
    "cungDiaBan",
    "dacTinhSao",
    "thienCan",
    "dichCung",
    "khoangCachCung",
    "timCuc",
    "timTuVi",
    "timTrangSinh",
    "timHoaLinh",
    "timThienKhoi",
    "timThienQuanThienPhuc",
    "timCoThan",
    "timThienMa",
    "timPhaToai",
    "Sao",
    "ngayThangNam",
    "canChiNgay",
    "canChiGio",
    "ngayThangNamCanChi",
    "nguHanh",
    "sinhKhac",
    "nguHanhNapAm",
    "jdFromDate",
    "jdToDate",
    "NewMoon",
    "SunLongitude",
    "getSunLongitude",
    "getNewMoonDay",
    "getLunarMonth11",
    "getLeapMonthOffset",
]
