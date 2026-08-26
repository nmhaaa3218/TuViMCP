# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Tests for Vòng Tràng Sinh (Thai & Dưỡng ordering) and Thiên Lương school astrological rules.
"""

from tuvi_mcp.tuvi_calculator import get_horoscope_chart
from tuvi_mcp.horoscope import Horoscope


def test_vong_trang_sinh_am_nam_kim_tu_cuc():
    """Verify Thai and Dưỡng positioning for Âm Nam Kim Tứ Cục (21/08/2003, giờ Thân).
    
    Kim Tứ Cục starts Tràng Sinh at Tỵ (6) and moves counter-clockwise for Âm Nam:
    - Cung 6 (Tỵ): Tràng Sinh
    - Cung 5 (Thìn): Mộc Dục
    - Cung 4 (Mão): Quan Đới
    - Cung 3 (Dần): Lâm Quan
    - Cung 2 (Sửu): Đế Vượng
    - Cung 1 (Tý): Suy
    - Cung 12 (Hợi): Bệnh
    - Cung 11 (Tuất): Tử
    - Cung 10 (Dậu): Mộ
    - Cung 9 (Thân): Tuyệt
    - Cung 8 (Mùi): Thai
    - Cung 7 (Ngọ): Dưỡng
    """
    chart = get_horoscope_chart(
        name="Guest",
        day=21,
        month=8,
        year=2003,
        hour_val="16:30",
        gender_val="Nam",
        is_solar=True,
    )
    
    cungs = {c["cung_so"]: [s["name"] for s in c["sao"]] for c in chart["dia_ban"]}
    
    assert "Tràng sinh" in cungs[6], "Cung Tỵ (6) must have Tràng sinh"
    assert "Tuyệt" in cungs[9], "Cung Thân (9) must have Tuyệt"
    assert "Thai" in cungs[8], "Cung Mùi (8) must have Thai"
    assert "Dưỡng" in cungs[7], "Cung Ngọ (7) must have Dưỡng"


def test_vong_trang_sinh_duong_nam_thuan():
    """Verify Thai and Dưỡng positioning for Dương Nam (moves clockwise).
    
    For Dương Nam, offset 10 is Thai and offset 11 is Dưỡng in clockwise direction.
    """
    # 15/08/1995 (Ất Hợi -> Âm Nữ / Dương Nam)
    chart = get_horoscope_chart(
        name="Test Dương Nam",
        day=10,
        month=6,
        year=1995,  # Ất Hợi (Âm) -> Dương Nam will move counter-clockwise, let's test a Dương Nam
        hour_val="10:00",
        gender_val="Nam",
        is_solar=True,
    )
    # Let's test a Dương Nam birth year: 1994 (Giáp Tuất - Dương Nam -> clockwise)
    chart_duong = get_horoscope_chart(
        name="Test Giáp Tuất",
        day=15,
        month=5,
        year=1994,
        hour_val="10:00",
        gender_val="Nam",
        is_solar=True,
    )
    
    cungs = {c["cung_so"]: [s["name"] for s in c["sao"]] for c in chart_duong["dia_ban"]}
    
    # Find which cung has Tràng Sinh
    ts_cung = None
    thai_cung = None
    duong_cung = None
    for c_so, star_names in cungs.items():
        if "Tràng sinh" in star_names:
            ts_cung = c_so
        if "Thai" in star_names:
            thai_cung = c_so
        if "Dưỡng" in star_names:
            duong_cung = c_so
            
    assert ts_cung is not None
    assert thai_cung is not None
    assert duong_cung is not None
    
    # In clockwise: Thai is (ts_cung - 1 + 10) % 12 + 1, Dưỡng is (ts_cung - 1 + 11) % 12 + 1
    expected_thai = ((ts_cung - 1 + 10) % 12) + 1
    expected_duong = ((ts_cung - 1 + 11) % 12) + 1
    
    assert thai_cung == expected_thai, f"Thai should be at {expected_thai} (got {thai_cung})"
    assert duong_cung == expected_duong, f"Dưỡng should be at {expected_duong} (got {duong_cung})"


def test_van_tinh_name_and_thien_giai():
    """Verify Văn Tinh does not have 'LN.' prefix and Thiên Giải follows Thiên Lương school."""
    chart = get_horoscope_chart(
        name="Guest",
        day=21,
        month=8,
        year=2003,
        hour_val="16:30",
        gender_val="Nam",
        is_solar=True,
    )
    
    all_stars = []
    for c in chart["dia_ban"]:
        for s in c["sao"]:
            all_stars.append(s["name"])
            
    assert "Văn tinh" in all_stars, "Star should be named 'Văn tinh'"
    assert "LN. Văn tinh" not in all_stars, "Star should NOT have 'LN.' prefix"
    
    # Thiên Giải in Thiên Lương school for month 7 is at Thân (9)
    than_cung = next(c for c in chart["dia_ban"] if c["cung_so"] == 9)
    than_star_names = [s["name"] for s in than_cung["sao"]]
    assert "Thiên giải" in than_star_names, "Thiên Giải for month 7 should be at Thân according to Thiên Lương school"
