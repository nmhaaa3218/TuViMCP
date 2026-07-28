# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Internal chart building pipeline (Thiên Bàn + Địa Bàn construction).

Public entry: ``get_horoscope_chart``.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from ._engine.App import lapDiaBan
from ._engine.DiaBan import diaBan as DiaBanClass
from ._engine.ThienBan import lapThienBan
from ._input import (
    BRANCH_NAMES,
    LUC_HOP_MAP,
    parse_gender,
    parse_hour,
    parse_solar_hour,
    validate_birth_parameters,
)
from ._rules import evaluate_cach_cuc

SAO_ATTRIBUTE_MAP = {"M": "Miếu địa", "V": "Vượng địa", "Đ": "Đắc địa", "B": "Bình hòa", "H": "Hãm địa"}


def get_quan_he_hinh_hoc(cung_so: int) -> dict:
    """Static geometric relationships (Xung Chiếu, Tam Hợp, Nhị Hợp, Giáp Cung) for a house index (1-12)."""
    opp_so = ((cung_so - 1 + 6) % 12) + 1
    tri1_so = ((cung_so - 1 + 4) % 12) + 1
    tri2_so = ((cung_so - 1 + 8) % 12) + 1
    nh_so = LUC_HOP_MAP.get(cung_so, 1)
    g_left_so = ((cung_so - 2) % 12) + 1
    g_right_so = (cung_so % 12) + 1

    return {
        "xung_chieu": BRANCH_NAMES[opp_so],
        "tam_hop": [BRANCH_NAMES[tri1_so], BRANCH_NAMES[tri2_so]],
        "nhi_hop": BRANCH_NAMES[nh_so],
        "giap_cung": [BRANCH_NAMES[g_left_so], BRANCH_NAMES[g_right_so]],
    }


def serialize_sao(sao_dict: dict) -> dict:
    """Clean and format star dictionaries."""
    attr = sao_dict.get("saoDacTinh")
    return {
        "id": sao_dict.get("saoID"),
        "name": sao_dict.get("saoTen"),
        "element": sao_dict.get("saoNguHanh"),
        "type": sao_dict.get("saoLoai"),
        "direction": sao_dict.get("saoPhuongVi"),
        "yin_yang": sao_dict.get("saoAmDuong"),
        "attribute": SAO_ATTRIBUTE_MAP.get(attr) if attr else None,
    }


def build_raw_chart(day: int, month: int, year: int, hour: int, gender: int, is_solar: bool, name: str = "Khách"):
    """Internal calculation of DiaBan and ThienBan."""
    db = lapDiaBan(DiaBanClass, day, month, year, hour, gender, is_solar, 7)
    tb = lapThienBan(day, month, year, hour, gender, name, db, is_solar, 7)
    return db, tb


def adjust_date_for_late_ty(day: int, month: int, year: int, hour_val, is_solar: bool):
    """If birth hour is 23 (late Tý hour), roll calculation date forward by +1 day.

    Returns: (calc_day, calc_month, calc_year, orig_solar_str, is_late_ty)
    """
    is_late_ty = parse_solar_hour(hour_val) == 23
    calc_day, calc_month, calc_year = day, month, year

    # Pre-calculate original solar date string
    if is_solar:
        orig_solar_str = f"{day}/{month}/{year}"
    else:
        from ._calendar import convert_lunar_to_solar  # local import to avoid cycle

        solar_res = convert_lunar_to_solar(day, month, year, False, 7)
        if "error" not in solar_res:
            orig_solar_str = f"{solar_res['solar_day']}/{solar_res['solar_month']}/{solar_res['solar_year']}"
        else:
            orig_solar_str = ""

    if is_late_ty:
        if is_solar:
            try:
                dt = datetime(year, month, day) + timedelta(days=1)
                calc_day, calc_month, calc_year = dt.day, dt.month, dt.year
            except Exception:
                pass
        else:
            try:
                from ._calendar import convert_lunar_to_solar, convert_solar_to_lunar

                solar_res = convert_lunar_to_solar(day, month, year, False, 7)
                if "error" not in solar_res:
                    dt = datetime(
                        solar_res["solar_year"], solar_res["solar_month"], solar_res["solar_day"]
                    ) + timedelta(days=1)
                    lunar_res = convert_solar_to_lunar(dt.day, dt.month, dt.year, 7)
                    if "error" not in lunar_res:
                        calc_day, calc_month, calc_year = (
                            lunar_res["lunar_day"],
                            lunar_res["lunar_month"],
                            lunar_res["lunar_year"],
                        )
            except Exception:
                pass

    return calc_day, calc_month, calc_year, orig_solar_str, is_late_ty


def get_horoscope_chart(
    name: str, day: int, month: int, year: int, hour_val, gender_val, is_solar: bool = True
) -> dict:
    """Standardized entry point to calculate and return full horoscope JSON."""
    validation_err = validate_birth_parameters(day, month, year, hour_val, gender_val, is_solar)
    if validation_err:
        return validation_err
    hour = parse_hour(hour_val)
    gender = parse_gender(gender_val)

    calc_day, calc_month, calc_year, orig_solar_str, is_late_ty = adjust_date_for_late_ty(
        day, month, year, hour_val, is_solar
    )

    db, tb = build_raw_chart(calc_day, calc_month, calc_year, hour, gender, is_solar, name)

    cungs = []
    for i in range(1, 13):
        cung = db.thapNhiCung[i]
        cungs.append(
            {
                "cung_so": cung.cungSo,
                "cung_ten": cung.cungTen,
                "hanh_cung": cung.hanhCung,
                "cung_chu": getattr(cung, "cungChu", ""),
                "dai_han": getattr(cung, "cungDaiHan", None),
                "tieu_han": getattr(cung, "cungTieuHan", ""),
                "cung_than": getattr(cung, "cungThan", False),
                "tuan_trung": getattr(cung, "tuanTrung", False),
                "triet_lo": getattr(cung, "trietLo", False),
                "quan_he_hinh_hoc": get_quan_he_hinh_hoc(cung.cungSo),
                "sao": [serialize_sao(s) for s in cung.cungSao],
            }
        )

    # Find Lai nhân cung
    lai_nhan_cung = ""
    for cung in cungs:
        if cung["cung_ten"]:
            cung_can = cung["cung_ten"].split()[0]
            if cung_can == tb.canNamTen:
                lai_nhan_cung = cung["cung_chu"]
                break

    thien_ban_data = {
        "ten": tb.ten,
        "gioi_tinh": tb.namNu,
        "ngay_duong": orig_solar_str
        if (is_late_ty and orig_solar_str)
        else f"{tb.ngayDuong}/{tb.thangDuong}/{tb.namDuong}",
        "ngay_am": f"{tb.ngayAm}/{tb.thangAm}/{tb.namAm}",
        "gio_sinh": tb.gioSinh,
        "chi_gio_sinh": tb.chiGioSinh.get("tenChi") if isinstance(tb.chiGioSinh, dict) else tb.chiGioSinh,
        "can_gio_sinh": tb.canGioSinh,
        "can_thang": tb.canThangTen,
        "chi_thang": tb.chiThangTen,
        "can_nam": tb.canNamTen,
        "chi_nam": tb.chiNamTen,
        "can_ngay": tb.canNgayTen,
        "chi_ngay": tb.chiNgayTen,
        "am_duong_nam_sinh": tb.amDuongNamSinh,
        "am_duong_menh": tb.amDuongMenh,
        "hanh_cuc": tb.hanhCuc,
        "ten_cuc": tb.tenCuc,
        "menh_chu": tb.menhChu,
        "than_chu": tb.thanChu,
        "menh": tb.menh,
        "ban_menh": tb.banMenh,
        "sinh_khac": tb.sinhKhac,
        "lai_nhan_cung": lai_nhan_cung,
    }

    chart_res = {"thien_ban": thien_ban_data, "dia_ban": cungs}
    chart_res["cach_cuc"] = evaluate_cach_cuc(chart_res)
    return chart_res


__all__ = [
    "SAO_ATTRIBUTE_MAP",
    "adjust_date_for_late_ty",
    "build_raw_chart",
    "get_horoscope_chart",
    "get_quan_he_hinh_hoc",
    "serialize_sao",
]
