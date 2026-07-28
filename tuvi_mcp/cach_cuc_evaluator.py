# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Data-driven Cách Cục Evaluator for Tử Vi Đẩu Số.
Evaluates rules declaratively defined in tuvi_mcp/data/cach_cuc.json.
"""

import json
import os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
_CACH_CUC_PATH = os.path.join(_DATA_DIR, "cach_cuc.json")

with open(_CACH_CUC_PATH, "r", encoding="utf-8") as _f:
    CACH_CUC_RULES: list = json.load(_f)
del _f


def load_cach_cuc_rules() -> list:
    """Return the eagerly-loaded declarative cách cục rules.

    Kept as a thin accessor for backward compatibility. The dataset is loaded
    once at module import time so any malformed/missing data fails loudly on
    server startup (or test collection) rather than on the first chart call.
    """
    return CACH_CUC_RULES


def get_cung_chi(cung: dict) -> str:
    """Extract Earthly Branch name from cung_ten (e.g. 'Mậu Tý' -> 'Tý')."""
    if not cung or "cung_ten" not in cung:
        return ""
    parts = cung["cung_ten"].strip().split()
    return parts[1] if len(parts) > 1 else parts[0]


def get_cung_by_chu(dia_ban: list, cung_chu: str) -> dict:
    """Find a house by its domain name (e.g., 'Mệnh', 'Quan Lộc', 'Tài Bạch', 'Thiên Di', 'Điền Trạch').

    Lookup is case-insensitive to tolerate serializer casing variance
    (chart emits e.g. 'Quan lộc' / 'Tài bạch' / 'Điền trạch' lowercased b/t).
    """
    target = cung_chu.strip().lower()
    for c in dia_ban:
        if c.get("cung_chu", "").strip().lower() == target:
            return c
    return None


def get_cung_by_so(dia_ban: list, cung_so: int) -> dict:
    """Find a house by its 1-indexed number (1 to 12)."""
    cung_so_norm = ((cung_so - 1) % 12) + 1
    for c in dia_ban:
        if c.get("cung_so") == cung_so_norm:
            return c
    return None


def get_cung_by_chi(dia_ban: list, chi_name: str) -> dict:
    """Find a house by its Earthly Branch name (e.g., 'Ngọ', 'Tý', 'Thìn')."""
    chi_lower = chi_name.strip().lower()
    for c in dia_ban:
        if get_cung_chi(c).lower() == chi_lower:
            return c
    return None


def get_tam_phuong_tu_chinh(dia_ban: list, cung_so: int) -> list:
    """Returns list of houses in Tam Phương Tứ Chính."""
    c_base = (cung_so - 1) % 12
    opp = (c_base + 6) % 12 + 1
    tri1 = (c_base + 4) % 12 + 1
    tri2 = (c_base + 8) % 12 + 1
    res = [
        get_cung_by_so(dia_ban, cung_so),
        get_cung_by_so(dia_ban, opp),
        get_cung_by_so(dia_ban, tri1),
        get_cung_by_so(dia_ban, tri2),
    ]
    return [c for c in res if c is not None]


def get_giap_cung(dia_ban: list, cung_so: int) -> tuple:
    """Returns tuple of left and right adjacent houses (Giáp cung)."""
    c_left = (cung_so - 2) % 12 + 1
    c_right = cung_so % 12 + 1
    return get_cung_by_so(dia_ban, c_left), get_cung_by_so(dia_ban, c_right)


def get_luc_hop_cung(dia_ban: list, cung_so: int) -> dict:
    """Returns the 6-Harmony (Lục Hợp) house for a given house index."""
    luc_hop_map = {
        1: 2, 2: 1,      # Tý - Sửu
        3: 12, 12: 3,    # Dần - Hợi
        4: 11, 11: 4,    # Mão - Tuất
        5: 10, 10: 5,    # Thìn - Dậu
        6: 9, 9: 6,      # Tỵ - Thân
        7: 8, 8: 7       # Ngọ - Mùi
    }
    lh_so = luc_hop_map.get(cung_so)
    return get_cung_by_so(dia_ban, lh_so) if lh_so else None


def has_star(cung: dict, star_name: str, star_attr: str = None) -> bool:
    """Check if a house contains a specific star (exact normalized name matching)."""
    if not cung:
        return False
    star_name_lower = star_name.strip().lower()
    for s in cung.get("sao", []):
        s_name = s.get("name", "").strip().lower()
        if s_name == star_name_lower:
            if star_attr is None:
                return True
            s_attr = s.get("attribute", "") or ""
            if star_attr.lower() in s_attr.lower():
                return True
            return False
    return False


def count_stars_in_houses(houses: list, star_names: list) -> int:
    """Count how many of the listed stars are present across the given houses."""
    count = 0
    for st in star_names:
        for h in houses:
            if has_star(h, st):
                count += 1
                break
    return count


def match_house_condition(cung: dict, rule: dict) -> bool:
    """Evaluate star and branch conditions against a single house."""
    if not cung:
        return False
    if "branches_in" in rule and get_cung_chi(cung) not in rule["branches_in"]:
        return False
    if "stars_all" in rule:
        for st in rule["stars_all"]:
            if not has_star(cung, st):
                return False
    if "stars_any" in rule:
        found = any(has_star(cung, st) for st in rule["stars_any"])
        if not found:
            return False
    if "stars_none" in rule:
        for st in rule["stars_none"]:
            if has_star(cung, st):
                return False
    if "not_both" in rule:
        if all(has_star(cung, st) for st in rule["not_both"]):
            return False
    return True


def evaluate_single_condition(cond: dict, dia_ban: list, thien_ban: dict) -> bool:
    """Evaluate a single rule block against the chart data."""
    cung_menh = get_cung_by_chu(dia_ban, "Mệnh")
    menh_so = cung_menh.get("cung_so") if cung_menh else 1
    tam_phuong = get_tam_phuong_tu_chinh(dia_ban, menh_so)
    giap_left, giap_right = get_giap_cung(dia_ban, menh_so)

    if "cung_menh" in cond:
        if not match_house_condition(cung_menh, cond["cung_menh"]):
            return False

    # Tam Phương star-count predicates share identical semantics with different
    # condition keys. Dispatch over the canonical set instead of repeating the
    # same min-count check seven times.
    for tp_key in (
        "tam_phuong_tu_chinh",
        "tam_phuong_tu_chinh_aux",
        "tam_phuong_tu_chinh_loc",
        "tam_phuong_sat",
        "tam_phuong_loc",
        "tam_phuong_ma",
        "tam_phuong_tuong",
    ):
        if tp_key not in cond:
            continue
        tp_rule = cond[tp_key]
        st_req = tp_rule.get("stars_required", [])
        min_cnt = tp_rule.get("min_count", len(st_req))
        if count_stars_in_houses(tam_phuong, st_req) < min_cnt:
            return False

    if "giap_cung" in cond:
        g_rule = cond["giap_cung"]
        cnt = count_stars_in_houses([giap_left, giap_right], g_rule.get("stars_required", []))
        if cnt < g_rule.get("min_count", 2):
            return False

    if "giap_cung_pairs" in cond:
        matched_pair = False
        for p1, p2 in cond["giap_cung_pairs"]:
            if (has_star(giap_left, p1) and has_star(giap_right, p2)) or \
               (has_star(giap_left, p2) and has_star(giap_right, p1)):
                matched_pair = True
                break
        if not matched_pair:
            return False

    if "luc_hop" in cond:
        lh_cung = get_luc_hop_cung(dia_ban, menh_so)
        if not match_house_condition(lh_cung, cond["luc_hop"]):
            return False

    if "cung_quan" in cond:
        c_quan = get_cung_by_chu(dia_ban, "Quan Lộc")
        if not match_house_condition(c_quan, cond["cung_quan"]):
            return False

    if "cung_tai" in cond:
        c_tai = get_cung_by_chu(dia_ban, "Tài Bạch")
        if not match_house_condition(c_tai, cond["cung_tai"]):
            return False

    if "cung_dien" in cond:
        c_dien = get_cung_by_chu(dia_ban, "Điền Trạch")
        if not match_house_condition(c_dien, cond["cung_dien"]):
            return False

    if "cung_ty" in cond:
        c_ty = get_cung_by_chi(dia_ban, "Tỵ")
        if not match_house_condition(c_ty, cond["cung_ty"]):
            return False

    if "cung_dau" in cond:
        c_dau = get_cung_by_chi(dia_ban, "Dậu")
        if not match_house_condition(c_dau, cond["cung_dau"]):
            return False

    if "stem_contains" in cond:
        nam_can = thien_ban.get("can_nam", "")
        if cond["stem_contains"] not in nam_can:
            return False

    return True


def evaluate_cach_cuc(chart_data: dict) -> list:
    """
    Evaluate all declarative Cách Cục rules against the given chart_data.
    Returns a list of matched cách cục dictionaries.
    """
    dia_ban = chart_data.get("dia_ban", [])
    thien_ban = chart_data.get("thien_ban", {})
    if not dia_ban:
        return []

    rules = CACH_CUC_RULES
    matched_results = []

    for rule_item in rules:
        conds = rule_item.get("conditions", {})
        is_match = False

        if "any_of" in conds:
            for sub_cond in conds["any_of"]:
                if evaluate_single_condition(sub_cond, dia_ban, thien_ban):
                    is_match = True
                    break
        else:
            is_match = evaluate_single_condition(conds, dia_ban, thien_ban)

        if is_match:
            matched_results.append({
                "id": rule_item["id"],
                "name": rule_item["name"],
                "category": rule_item["category"],
                "description": rule_item["description"],
                "reason": rule_item["reason"],
                "co_ca": rule_item.get("co_ca", ""),
                "binh_chu": rule_item.get("binh_chu", ""),
                "uu_khuyet_diem": rule_item.get("uu_khuyet_diem", "")
            })

    return matched_results
