#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. The vendored star-placement engine lives at
``tuvi_mcp._engine``. Re-exports the same surface so legacy imports
``from tuvi_mcp.ansaotuvi import ...`` keep working.
"""

import sys as _sys

from .. import _engine as _priv_engine
from .._compat._aliases import install_module_aliases

# Import submodules + names so the alias helper at the bottom registers
# ``tuvi_mcp.ansaotuvi.<name>`` entries in ``sys.modules``.
from .._engine import (
    L2S,
    S2L,
    AmDuong,
    App,
    DiaBan,
    Lich_HND,
    Sao,
    ThienBan,
    canChiGio,
    canChiNgay,
    cungDiaBan,
    dacTinhSao,
    diaBan,
    dichCung,
    jdFromDate,
    jdToDate,
    khoangCachCung,
    lapDiaBan,
    lapThienBan,
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
from .._engine import (
    Sao as _Sao_mod,
)

# ``Lich_EPHEM`` is optional (requires the ``ephem`` dependency). Reference
# it lazily so legacy imports ``from tuvi_mcp.ansaotuvi import Lich_EPHEM``
# still resolve without forcing ``ephem`` to be installed.
try:
    from .._engine import Lich_EPHEM as _Lich_EPHEM
    Lich_EPHEM = _Lich_EPHEM
except Exception:
    Lich_EPHEM = None

__title__ = "ansaotuvi"
__version__ = "0.4.0"
__author__ = "Manh Ha Nguyen"
__author_email__ = "manh.ha.3218@gmail.com"
__license__ = "MIT License"

__all__ = [
    "AmDuong",
    "App",
    "DiaBan",
    "Lich_EPHEM",
    "Lich_HND",
    "Sao",
    "ThienBan",
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
    "ngayThangNam",
    "canChiNgay",
    "canChiGio",
    "ngayThangNamCanChi",
    "nguHanh",
    "sinhKhac",
    "nguHanhNapAm",
]

install_module_aliases(__name__, _priv_engine.__name__, _sys.modules)
