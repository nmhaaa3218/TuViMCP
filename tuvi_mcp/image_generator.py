# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. Implementation moved to ``tuvi_mcp._rendering``.
"""

from ._rendering import (
    ATTR_SUFFIX_MAP,
    CHINH_TINH_IDS,
    CUNG_COORDS,
    ELEMENT_COLORS,
    TRANSIT_STAR_DETAILS,
    draw_badge,
    draw_lines_behind_center,
    draw_tuan_triet,
    generate_laso_image,
    get_font,
)

__all__ = [
    "ATTR_SUFFIX_MAP",
    "CHINH_TINH_IDS",
    "CUNG_COORDS",
    "ELEMENT_COLORS",
    "TRANSIT_STAR_DETAILS",
    "draw_badge",
    "draw_lines_behind_center",
    "draw_tuan_triet",
    "generate_laso_image",
    "get_font",
]
