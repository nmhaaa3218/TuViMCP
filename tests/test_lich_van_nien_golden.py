# -*- coding: utf-8 -*-
"""Golden tests cross-checked against public Vietnamese lịch vạn niên references.

References (Aug 2026 and others):
- thienmenh.net, lichvannien365.com, phongthuyvuong.net, ngaydep.com
- saptet.com/thang-8/lich-van-nien (full month August 2026 Hoàng/Hắc pattern)
"""

from __future__ import annotations

import calendar
import pytest

from tuvi_mcp._auspicious import get_auspicious_details

# (day, month, year, ten_sao, loai, truc, xiu, hoang_hours)
GOLDEN_DAYS = [
    pytest.param(
        10, 8, 2026,
        "Bạch Hổ", "Hắc Đạo", "Thành", "Tất",
        ["Dần", "Thìn", "Tỵ", "Thân", "Dậu", "Hợi"],
        id="aug10_bach_ho_hac_dao",
    ),
    pytest.param(
        21, 8, 2026,
        "Chu Tước", "Hắc Đạo", "Nguy", "Cang",
        ["Tý", "Dần", "Mão", "Ngọ", "Mùi", "Dậu"],
        id="aug21_chu_tuoc_hac_dao",
    ),
    pytest.param(
        22, 8, 2026,
        "Kim Quỹ", "Hoàng Đạo", "Thành", "Đê",
        ["Dần", "Thìn", "Tỵ", "Thân", "Dậu", "Hợi"],
        id="aug22_kim_quy_hoang_dao",
    ),
    pytest.param(
        1, 1, 2026,
        "Chu Tước", "Hắc Đạo", "Bế", "Tỉnh",
        ["Sửu", "Thìn", "Ngọ", "Mùi", "Tuất", "Hợi"],
        id="jan01_chu_tuoc_hac_dao",
    ),
    pytest.param(
        4, 8, 2026,
        "Thanh Long", "Hoàng Đạo", "Bình", "Thất", None,
        id="aug04_thanh_long",
    ),
    pytest.param(
        5, 8, 2026,
        "Minh Đường", "Hoàng Đạo", "Định", "Bích", None,
        id="aug05_minh_duong",
    ),
    pytest.param(
        6, 8, 2026,
        "Thiên Hình", "Hắc Đạo", "Chấp", "Khuê", None,
        id="aug06_thien_hinh",
    ),
    pytest.param(
        23, 8, 2026,
        "Thiên Đức", "Hoàng Đạo", "Thâu", "Phòng", None,
        id="aug23_thien_duc",
    ),
    pytest.param(
        24, 8, 2026,
        "Bạch Hổ", "Hắc Đạo", "Khai", "Tâm", None,
        id="aug24_bach_ho",
    ),
    pytest.param(
        26, 9, 2026,
        "Minh Đường", "Hoàng Đạo", "Phá", "Nữ",
        ["Tý", "Dần", "Mão", "Ngọ", "Mùi", "Dậu"],
        id="sep26_minh_duong_hoang_dao",
    ),
    pytest.param(
        5, 2, 2026,
        "Thanh Long", "Hoàng Đạo", "Thành", "Giác",
        ["Dần", "Thìn", "Tỵ", "Thân", "Dậu", "Hợi"],
        id="feb05_thanh_long_hoang_dao_lap_xuan",
    ),
    pytest.param(
        17, 2, 2026,
        "Tư Mệnh", "Hoàng Đạo", "Thành", "Thất",
        ["Dần", "Thìn", "Tỵ", "Thân", "Dậu", "Hợi"],
        id="feb17_tu_menh_mung_1_tet_binh_ngo",
    ),
]

# saptet.com August 2026 — Hoàng/Hắc per day
SAPTET_AUG_2026_HOANG = {2, 4, 5, 8, 9, 11, 13, 16, 18, 19, 22, 23, 25, 28, 30, 31}
SAPTET_AUG_2026_HAC = {1, 3, 6, 7, 10, 12, 14, 15, 17, 20, 21, 24, 26, 27, 29}


def _norm_truc(ten: str) -> str:
    return ten.removeprefix("Trực ")


def _norm_xiu(ten: str) -> str:
    return ten.removeprefix("Sao ")


@pytest.mark.parametrize(
    "day,month,year,ten_sao,loai,truc,xiu,hoang_hours",
    GOLDEN_DAYS,
)
def test_golden_day_matches_lich_van_nien(
    day, month, year, ten_sao, loai, truc, xiu, hoang_hours
):
    raw = get_auspicious_details(day, month, year, is_solar=True)
    assert "error" not in raw

    ngay = raw["ngay_hoang_dao"]
    assert ngay["ten_sao"] == ten_sao
    assert ngay["loai"] == loai
    assert ngay["is_hoang_dao"] == (loai == "Hoàng Đạo")
    assert _norm_truc(raw["truc_ngay"]["ten"]) == truc
    assert _norm_xiu(raw["nhi_thap_bat_tu"]["ten"]) == xiu

    if hoang_hours is not None:
        got = [g["chi"] for g in raw["gio_hoang_dao"] if g["is_hoang_dao"]]
        assert got == hoang_hours


@pytest.mark.parametrize("day", range(1, 32))
def test_aug_2026_hoang_hac_matches_saptet(day: int):
    raw = get_auspicious_details(day, 8, 2026, is_solar=True)
    is_hoang = raw["ngay_hoang_dao"]["is_hoang_dao"]
    if day in SAPTET_AUG_2026_HOANG:
        assert is_hoang is True, f"Day {day}/8/2026 should be Hoàng Đạo"
    elif day in SAPTET_AUG_2026_HAC:
        assert is_hoang is False, f"Day {day}/8/2026 should be Hắc Đạo"


@pytest.mark.parametrize("month", range(1, 13))
def test_all_2026_days_have_valid_hoang_hac_type(month: int):
    ndays = calendar.monthrange(2026, month)[1]
    for day in range(1, ndays + 1):
        raw = get_auspicious_details(day, month, 2026, is_solar=True)
        loai = raw["ngay_hoang_dao"]["loai"]
        assert loai in ("Hoàng Đạo", "Hắc Đạo"), f"{day}/{month}/2026 -> {loai}"
