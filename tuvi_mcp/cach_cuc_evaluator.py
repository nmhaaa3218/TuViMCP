# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. Implementation moved to ``tuvi_mcp._rules``.
"""

from ._rules import (
    CACH_CUC_RULES,
    count_stars_in_houses,
    evaluate_cach_cuc,
    evaluate_single_condition,
    get_cung_by_chi,
    get_cung_by_chu,
    get_cung_by_so,
    get_cung_chi,
    get_giap_cung,
    get_luc_hop_cung,
    get_tam_phuong_tu_chinh,
    has_star,
    load_cach_cuc_rules,
    match_house_condition,
)

__all__ = [
    "CACH_CUC_RULES",
    "count_stars_in_houses",
    "evaluate_cach_cuc",
    "evaluate_single_condition",
    "get_cung_by_chi",
    "get_cung_by_chu",
    "get_cung_by_so",
    "get_cung_chi",
    "get_giap_cung",
    "get_luc_hop_cung",
    "get_tam_phuong_tu_chinh",
    "has_star",
    "load_cach_cuc_rules",
    "match_house_condition",
]
