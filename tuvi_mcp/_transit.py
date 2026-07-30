# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Internal transit (Vận Hạn) analysis.

Public entry: ``get_van_han_analysis``.
"""

from __future__ import annotations

from ._chart import adjust_date_for_late_ty, build_raw_chart, get_horoscope_chart
from ._engine.AmDuong import dichCung, thienCan, timThienMa
from ._input import (
    CAN_NAMES,
    parse_gender,
    parse_hour,
    validate_birth_parameters,
    validate_transit_period,
)


def calculate_transit_stars(current_year: int) -> list:
    """Calculate the positions of the transit stars (sao lưu) for a target year."""
    # current_year can and chi
    can_nam = (current_year + 6) % 10 + 1
    chi_nam = (current_year + 8) % 12 + 1

    # Lưu Thái Tuế: at branch of target year
    luu_thai_tue = chi_nam

    # Lưu Lộc Tồn: based on Can of target year
    luu_loc_ton = thienCan[can_nam]["vitriDiaBan"]

    # Lưu Kình Dương and Lưu Đà La relative to Lộc Tồn
    luu_kinh_duong = dichCung(luu_loc_ton, 1)
    luu_da_la = dichCung(luu_loc_ton, -1)

    # Lưu Thiên Mã: based on Chi of target year
    luu_thien_ma = timThienMa(chi_nam)

    # Lưu Thiên Khốc and Lưu Thiên Hư: start from Ngọ (7)
    luu_thien_khoc = dichCung(7, -chi_nam + 1)
    luu_thien_hu = dichCung(7, chi_nam - 1)

    from ._input import BRANCH_NAMES

    return [
        {"name": "Lưu Thái Tuế", "cung_so": luu_thai_tue, "chi": BRANCH_NAMES[luu_thai_tue]},
        {"name": "Lưu Lộc Tồn", "cung_so": luu_loc_ton, "chi": BRANCH_NAMES[luu_loc_ton]},
        {"name": "Lưu Kình Dương", "cung_so": luu_kinh_duong, "chi": BRANCH_NAMES[luu_kinh_duong]},
        {"name": "Lưu Đà La", "cung_so": luu_da_la, "chi": BRANCH_NAMES[luu_da_la]},
        {"name": "Lưu Thiên Mã", "cung_so": luu_thien_ma, "chi": BRANCH_NAMES[luu_thien_ma]},
        {"name": "Lưu Thiên Khốc", "cung_so": luu_thien_khoc, "chi": BRANCH_NAMES[luu_thien_khoc]},
        {"name": "Lưu Thiên Hư", "cung_so": luu_thien_hu, "chi": BRANCH_NAMES[luu_thien_hu]},
    ]


def get_van_han_analysis(
    name: str,
    day: int,
    month: int,
    year: int,
    hour_val,
    gender_val,
    is_solar: bool,
    current_year: int,
    current_month: int = 1,
    current_day: int | None = None,
    timezone: float = 7.0,
) -> dict:
    """Analyze transit stars & active cungs (Đại Hạn, Tiểu Hạn, Nguyệt Hạn, Nhật Hạn) for a target Lunar period."""
    validation_err = validate_birth_parameters(day, month, year, hour_val, gender_val, is_solar, timezone)
    if validation_err:
        return validation_err
    transit_err = validate_transit_period(current_year, current_month, current_day)
    if transit_err:
        return transit_err
    hour = parse_hour(hour_val)
    gender = parse_gender(gender_val)

    calc_day, calc_month, calc_year, _, _ = adjust_date_for_late_ty(day, month, year, hour_val, is_solar, timezone)

    # Calculate birth details first
    _, tb = build_raw_chart(calc_day, calc_month, calc_year, hour, gender, is_solar, name, timezone)
    chart = get_horoscope_chart(name, day, month, year, hour_val, gender_val, is_solar, timezone)

    from ._input import BRANCH_NAMES

    # Current lunar year and branch
    curr_can = (current_year + 6) % 10 + 1
    curr_chi = (current_year + 8) % 12 + 1
    curr_year_can_chi = f"{CAN_NAMES[curr_can]} {BRANCH_NAMES[curr_chi]}"

    # Calculate current age (tuổi mụ)
    birth_lunar_year = tb.namAm
    age = current_year - birth_lunar_year + 1

    # 1. Identify active Đại Hạn cung
    active_dai_han_cung = None
    for cung in chart["dia_ban"]:
        dai_han_start = cung["dai_han"]
        if dai_han_start is not None:
            if dai_han_start <= age < dai_han_start + 10:
                active_dai_han_cung = cung
                break

    # 2. Identify active Tiểu Hạn cung
    active_tieu_han_cung = None
    for cung in chart["dia_ban"]:
        if cung["tieu_han"] == BRANCH_NAMES[curr_chi]:
            active_tieu_han_cung = cung
            break

    # 3. Identify active Nguyệt Hạn cung
    active_nguyet_han_cung = None
    if active_tieu_han_cung:
        p_tieu_han = active_tieu_han_cung["cung_so"] - 1
        m_birth = tb.thangAm
        h_birth = hour
        m_target = current_month

        p_month = (p_tieu_han - m_birth + h_birth + m_target - 1) % 12
        s_month = p_month + 1

        for cung in chart["dia_ban"]:
            if cung["cung_so"] == s_month:
                active_nguyet_han_cung = cung
                break

    # 4. Identify active Nhật Hạn cung (optional)
    active_nhat_han_cung = None
    if active_nguyet_han_cung and current_day is not None:
        nhat_so = ((active_nguyet_han_cung["cung_so"] - 1 + current_day - 1) % 12) + 1
        for cung in chart["dia_ban"]:
            if cung["cung_so"] == nhat_so:
                active_nhat_han_cung = cung
                break

    transits = calculate_transit_stars(current_year)

    # Build per-cung transit star map
    cung_transits = {i: [] for i in range(1, 13)}
    for t in transits:
        cung_transits[t["cung_so"]].append(t["name"])

    def enrich_cung(cung):
        if not cung:
            return None
        cung_id = cung["cung_so"]
        return {**cung, "transit_stars": cung_transits[cung_id]}

    return {
        "person_details": {
            "name": name,
            "gender": tb.namNu,
            "birth_solar": chart["thien_ban"]["ngay_duong"],
            "birth_lunar": chart["thien_ban"]["ngay_am"],
            "birth_lunar_year_can_chi": f"{chart['thien_ban']['can_nam']} {chart['thien_ban']['chi_nam']}",
            "birth_lunar_month_can_chi": f"{chart['thien_ban']['can_thang']} {chart['thien_ban']['chi_thang']}",
            "birth_lunar_day_can_chi": f"{chart['thien_ban']['can_ngay']} {chart['thien_ban']['chi_ngay']}",
            "birth_hour": chart["thien_ban"]["gio_sinh"],
            "element": chart["thien_ban"]["menh"],
            "destiny_cuc": chart["thien_ban"]["ten_cuc"],
            "lai_nhan_cung": chart["thien_ban"].get("lai_nhan_cung", ""),
        },
        "target_period": {
            "current_year": current_year,
            "current_year_can_chi": curr_year_can_chi,
            "current_month_lunar": current_month,
            "current_age": age,
        },
        "transit_stars": transits,
        "dai_han": enrich_cung(active_dai_han_cung),
        "tieu_han": enrich_cung(active_tieu_han_cung),
        "nguyet_han": enrich_cung(active_nguyet_han_cung),
        "nhat_han": enrich_cung(active_nhat_han_cung) if current_day is not None else None,
    }


__all__ = ["calculate_transit_stars", "get_van_han_analysis"]
