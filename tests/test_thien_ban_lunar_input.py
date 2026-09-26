# -*- coding: utf-8 -*-
"""Unit tests verifying solar date conversion when birth dates are provided in Lunar calendar."""

import pytest
from tuvi_mcp import Horoscope


def test_thien_ban_lunar_input_trung_thu_1995():
    """Verify 15/08/1995 Lunar converts to 09/09/1995 Solar on Thien Ban."""
    h = Horoscope.from_birth(
        name="Nguyễn Văn A",
        day=15,
        month=8,
        year=1995,
        hour=6,  # Giờ Mão
        gender=1,  # Nam
        calendar="lunar",
    )
    chart = h.chart()
    thien_ban = chart.thien_ban

    assert thien_ban["ngay_am"] == "15/8/1995"
    assert thien_ban["ngay_duong"] == "9/9/1995"
    assert thien_ban["can_nam"] == "Ất"
    assert thien_ban["chi_nam"] == "Hợi"
    # 09/09/1995 has day Can Chi Quý Mão
    assert thien_ban["can_ngay"] == "Quý"
    assert thien_ban["chi_ngay"] == "Mão"


def test_thien_ban_lunar_input_tet_canh_thin_2000():
    """Verify 01/01/2000 Lunar (Mùng 1 Tết Canh Thìn) converts to 05/02/2000 Solar."""
    h = Horoscope.from_birth(
        name="Trần Thị B",
        day=1,
        month=1,
        year=2000,
        hour=1,  # Giờ Tý
        gender=0,  # Nữ
        calendar="lunar",
    )
    chart = h.chart()
    thien_ban = chart.thien_ban

    assert thien_ban["ngay_am"] == "1/1/2000"
    assert thien_ban["ngay_duong"] == "5/2/2000"
    assert thien_ban["can_nam"] == "Canh"
    assert thien_ban["chi_nam"] == "Thìn"
    # 05/02/2000 has day Can Chi Quý Tỵ
    assert thien_ban["can_ngay"] == "Quý"
    assert thien_ban["chi_ngay"] == "Tỵ"


def test_thien_ban_lunar_and_solar_input_consistency():
    """Verify that entering the equivalent Solar date produces identical chart data."""
    # 15/08/1995 Lunar == 09/09/1995 Solar
    h_lunar = Horoscope.from_birth(
        name="Test",
        day=15,
        month=8,
        year=1995,
        hour=8,
        gender=1,
        calendar="lunar",
    )
    h_solar = Horoscope.from_birth(
        name="Test",
        day=9,
        month=9,
        year=1995,
        hour=8,
        gender=1,
        calendar="solar",
    )

    chart_lunar = h_lunar.chart().to_dict()
    chart_solar = h_solar.chart().to_dict()

    assert chart_lunar["thien_ban"]["ngay_am"] == chart_solar["thien_ban"]["ngay_am"]
    assert chart_lunar["thien_ban"]["ngay_duong"] == chart_solar["thien_ban"]["ngay_duong"]
    assert chart_lunar["thien_ban"]["can_ngay"] == chart_solar["thien_ban"]["can_ngay"]
    assert chart_lunar["thien_ban"]["chi_ngay"] == chart_solar["thien_ban"]["chi_ngay"]
    assert chart_lunar["thien_ban"]["ten_cuc"] == chart_solar["thien_ban"]["ten_cuc"]
    assert chart_lunar["thien_ban"]["menh"] == chart_solar["thien_ban"]["menh"]
