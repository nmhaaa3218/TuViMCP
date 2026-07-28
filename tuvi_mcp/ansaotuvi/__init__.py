#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. The vendored star-placement engine moved to
``tuvi_mcp._engine``.
"""

from ._engine import *  # noqa: F401,F403
from ._engine import AmDuong, App, DiaBan, Lich_EPHEM, Lich_HND, Sao, ThienBan

__title__ = 'ansaotuvi'
__version__ = '0.3.0'
__author__ = 'Manh Ha Nguyen'
__author_email__ = 'manh.ha.3218@gmail.com'
__license__ = 'MIT License'