# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
"""
import os
import tempfile

# Create a temporary file path for the database before importing database
db_fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(db_fd)  # Close file descriptor so sqlite can open it
os.environ["TUVI_DB_PATH"] = db_path

# Now import the target modules
from tuvi_mcp import database, tuvi_calculator  # noqa: E402


def test_hour_parsing():
    assert tuvi_calculator.parse_hour("14:30") == 8  # Mùi
    assert tuvi_calculator.parse_hour("Ngọ") == 7  # Ngọ
    assert tuvi_calculator.parse_hour("tý") == 1  # Tý
    assert tuvi_calculator.parse_hour(13.5) == 8  # Mùi (13.5 -> hour 13 of day -> Mùi)
    assert tuvi_calculator.parse_hour(3) == 3  # Direct branch index 3 -> Dần


def test_chart_generation():
    chart = tuvi_calculator.get_horoscope_chart(
        name="Nguyễn Văn A", day=10, month=6, year=1995, hour_val="14:30", gender_val="Nam", is_solar=True
    )
    # 1. Verify basic demographics
    assert chart["thien_ban"]["ten"] == "Nguyễn Văn A"
    assert chart["thien_ban"]["gioi_tinh"] == "Nam"
    assert len(chart["dia_ban"]) == 12

    # 2. Verify deterministic Solar to Lunar calendar conversion
    # Solar 10/06/1995 -> Lunar 13/05/1995 (Year of Ất Hợi)
    assert chart["thien_ban"]["ngay_am"] == "13/5/1995"
    assert chart["thien_ban"]["can_nam"] == "Ất"
    assert chart["thien_ban"]["chi_nam"] == "Hợi"

    # 3. Verify Tuần/Triệt double-cung behavior
    # For Can Ất, Triệt-Lộ is at Ngọ (7) and Mùi (8) cungs
    # For Giáp/Ất years (like Ất Hợi), Tuần-Trung is at Thân (9) and Dậu (10) cungs
    triet_cungs = [c for c in chart["dia_ban"] if c["cung_so"] in (7, 8)]
    non_triet_cung = [c for c in chart["dia_ban"] if c["cung_so"] == 9][0]
    tuan_cungs = [c for c in chart["dia_ban"] if c["cung_so"] in (9, 10)]

    for cung in triet_cungs:
        assert cung["triet_lo"] is True, f"Cung {cung['cung_so']} should have Triệt-Lộ"
    assert non_triet_cung["triet_lo"] is False

    for cung in tuan_cungs:
        assert cung["tuan_trung"] is True, f"Cung {cung['cung_so']} should have Tuần-Trung"

    # Ensure stars are populated
    has_stars = False
    for cung in chart["dia_ban"]:
        if len(cung["sao"]) > 0:
            has_stars = True
            break
    assert has_stars, "Cungs should have stars populated"


def test_van_han_transit_analysis():
    van_han = tuvi_calculator.get_van_han_analysis(
        name="Nguyễn Văn A",
        day=10,
        month=6,
        year=1995,
        hour_val="14:30",
        gender_val="Nam",
        is_solar=True,
        current_year=2026,
        current_month=5,
    )
    # 1. Target period details (Bính Ngọ 2026)
    assert van_han["target_period"]["current_year"] == 2026
    assert van_han["target_period"]["current_year_can_chi"] == "Bính Ngọ"
    assert van_han["target_period"]["current_month_lunar"] == 5
    assert len(van_han["transit_stars"]) == 7

    # 2. Verify deterministic transit star branch mappings for 2026:
    # - Lưu Thái Tuế is at branch Ngọ (index 7)
    # - Lưu Lộc Tồn (Can Bính) is at branch Tỵ (index 6)
    transit_map = {t["name"]: t["cung_so"] for t in van_han["transit_stars"]}

    assert transit_map["Lưu Thái Tuế"] == 7
    assert transit_map["Lưu Lộc Tồn"] == 6
    assert transit_map["Lưu Kình Dương"] == 7  # 1 cung forward from Lộc Tồn (Tỵ -> Ngọ)
    assert transit_map["Lưu Đà La"] == 5  # 1 cung backward from Lộc Tồn (Tỵ -> Thìn)

    # Verify transit stars calculation
    transit_names = [t["name"] for t in van_han["transit_stars"]]
    assert "Lưu Thái Tuế" in transit_names
    assert "Lưu Lộc Tồn" in transit_names
    assert "Lưu Kình Dương" in transit_names
    assert "Lưu Đà La" in transit_names
    assert "Lưu Thiên Mã" in transit_names
    assert "Lưu Thiên Khốc" in transit_names
    assert "Lưu Thiên Hư" in transit_names

    # Verify Đại Hạn, Tiểu Hạn, Nguyệt Hạn structures are present
    assert van_han["dai_han"] is not None
    assert van_han["tieu_han"] is not None
    assert van_han["nguyet_han"] is not None


def test_database_operations():
    # Database is initialized on import because TUVI_DB_PATH is set
    database.init_db()  # Ensure table exists

    # Save a record
    record_id = database.save_horoscope(
        name="Test Person",
        day=20,
        month=12,
        year=1980,
        hour=5,  # Mão
        gender="Nữ",
        is_solar=False,
        notes="Test notes",
    )
    assert record_id > 0

    # List and find
    records = database.list_saved_horoscopes()
    assert len(records) > 0

    saved_record = database.get_saved_horoscope_by_id(record_id)
    assert saved_record is not None
    assert saved_record["name"] == "Test Person"
    assert saved_record["day"] == 20
    assert saved_record["month"] == 12
    assert saved_record["year"] == 1980
    assert saved_record["hour"] == 5
    assert saved_record["gender"] == "Nữ"
    assert saved_record["is_solar"] == 0
    assert saved_record["notes"] == "Test notes"

    # Test name retrieval
    saved_by_name = database.get_saved_horoscope_by_name("Test Person")
    assert saved_by_name is not None
    assert saved_by_name["id"] == record_id

    # Delete record
    deleted = database.delete_saved_horoscope_by_id(record_id)
    assert deleted is True

    # Verify deletion
    deleted_record = database.get_saved_horoscope_by_id(record_id)
    assert deleted_record is None


def test_image_generation():
    from tuvi_mcp.mcp_server import generate_horoscope
    
    # 1. Test when generate_image is True (should return list with Image and dict)
    res = generate_horoscope(
        name="Manh Ha Nguyen",
        day=21,
        month=8,
        year=2003,
        hour_val="15:30",
        gender_val="Nam",
        is_solar=True,
        current_year=2026,
        generate_image=True
    )
    
    assert isinstance(res, list)
    assert len(res) == 2
    
    img_obj = res[0]
    chart_data = res[1]
    
    assert hasattr(img_obj, "path")
    assert img_obj.path is not None
    assert os.path.exists(img_obj.path)
    assert isinstance(chart_data, dict)
    assert chart_data["thien_ban"]["ten"] == "Manh Ha Nguyen"
    
    # Clean up the generated file
    try:
        os.remove(img_obj.path)
    except Exception:
        pass

    # 2. Test when generate_image is False (should return dict directly)
    res_no_img = generate_horoscope(
        name="Manh Ha Nguyen",
        day=21,
        month=8,
        year=2003,
        hour_val="15:30",
        gender_val="Nam",
        is_solar=True,
        current_year=2026,
        generate_image=False
    )
    assert isinstance(res_no_img, dict)
    assert "thien_ban" in res_no_img
    assert res_no_img["thien_ban"]["ten"] == "Manh Ha Nguyen"


# Cleanup hook to remove temp file after test session
def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove(db_path)
    except Exception:
        pass
