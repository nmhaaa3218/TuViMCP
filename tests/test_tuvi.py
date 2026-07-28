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

    # 4. Verify static geometry relationships (quan_he_hinh_hoc)
    ty_cung = [c for c in chart["dia_ban"] if c["cung_so"] == 1][0]
    qh = ty_cung["quan_he_hinh_hoc"]
    assert qh["xung_chieu"] == "Ngọ"
    assert set(qh["tam_hop"]) == {"Thìn", "Thân"}
    assert qh["nhi_hop"] == "Sửu"
    assert qh["giap_cung"] == ["Hợi", "Sửu"]

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
        generate_image=True,
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
        generate_image=False,
    )
    assert isinstance(res_no_img, dict)
    assert "thien_ban" in res_no_img
    assert res_no_img["thien_ban"]["ten"] == "Manh Ha Nguyen"


def test_calendar_conversion():
    # 1. Test Solar to Lunar conversion
    # Solar: June 28, 2026 -> Lunar: May 14, 2026, not a leap month
    lunar_res = tuvi_calculator.convert_solar_to_lunar(28, 6, 2026)
    assert lunar_res["lunar_day"] == 14
    assert lunar_res["lunar_month"] == 5
    assert lunar_res["lunar_year"] == 2026
    assert lunar_res["lunar_leap"] is False
    assert lunar_res["formatted"] == "14/5/2026"

    # 2. Test Lunar to Solar conversion
    solar_res = tuvi_calculator.convert_lunar_to_solar(14, 5, 2026, is_leap=False)
    assert solar_res["solar_day"] == 28
    assert solar_res["solar_month"] == 6
    assert solar_res["solar_year"] == 2026
    assert solar_res["formatted"] == "28/6/2026"

    # 3. Test MCP Tool exposure
    from tuvi_mcp.mcp_server import convert_calendar

    # Tool call Solar -> Lunar
    tool_lunar = convert_calendar(day=28, month=6, year=2026, from_solar=True)
    assert tool_lunar["lunar_day"] == 14
    assert tool_lunar["lunar_month"] == 5

    # Tool call Lunar -> Solar
    tool_solar = convert_calendar(day=14, month=5, year=2026, from_solar=False)
    assert tool_solar["solar_day"] == 28

    # 4. Error case
    invalid_lunar = convert_calendar(
        day=14, month=5, year=2026, from_solar=False, lunar_leap=True
    )  # May 2026 has no leap month
    assert "error" in invalid_lunar


def test_late_ty_hour_shift():
    # 1. Test Solar birth in late Tý hour (15/5/2024 at 23:15 Solar)
    # This should shift Lunar day to 9/4/2024 but keep displayed Solar date as 15/5/2024
    chart_solar = tuvi_calculator.get_horoscope_chart(
        name="Test Solar", day=15, month=5, year=2024, hour_val="23:15", gender_val="Nam", is_solar=True
    )
    assert chart_solar["thien_ban"]["ngay_duong"] == "15/5/2024"
    assert chart_solar["thien_ban"]["ngay_am"] == "9/4/2024"
    assert chart_solar["thien_ban"]["gio_sinh"] == "Bính Tý"
    assert chart_solar["thien_ban"]["can_ngay"] == "Canh"
    assert chart_solar["thien_ban"]["chi_ngay"] == "Thìn"

    # 2. Test Lunar birth in late Tý hour (8/4/2024 at 23:15 Lunar)
    # This should shift Lunar day to 9/4/2024 and correctly calculate Bính Tý hour
    chart_lunar = tuvi_calculator.get_horoscope_chart(
        name="Test Lunar", day=8, month=4, year=2024, hour_val="23:15", gender_val="Nam", is_solar=False
    )
    assert chart_lunar["thien_ban"]["ngay_duong"] == "15/5/2024"
    assert chart_lunar["thien_ban"]["ngay_am"] == "9/4/2024"
    assert chart_lunar["thien_ban"]["gio_sinh"] == "Bính Tý"
    assert chart_lunar["thien_ban"]["can_ngay"] == "Canh"
    assert chart_lunar["thien_ban"]["chi_ngay"] == "Thìn"

    # 3. Test branch-based inputs (should NOT shift day even if it has labels containing hours)
    for branch_input in ("Tý", "giờ Tý", "Tý (23h - 1h)", 1):
        chart_branch = tuvi_calculator.get_horoscope_chart(
            name="Test Branch", day=15, month=5, year=2024, hour_val=branch_input, gender_val="Nam", is_solar=True
        )
        # Should stay on Solar 15/5/2024 -> Lunar 8/4/2024
        assert chart_branch["thien_ban"]["ngay_duong"] == "15/5/2024"
        assert chart_branch["thien_ban"]["ngay_am"] == "8/4/2024"
        assert chart_branch["thien_ban"]["gio_sinh"] == "Giáp Tý"
        assert chart_branch["thien_ban"]["can_ngay"] == "Kỷ"
        assert chart_branch["thien_ban"]["chi_ngay"] == "Mão"


def test_input_validation():
    # 1. Test invalid date (Feb 31)
    res_date = tuvi_calculator.get_horoscope_chart(
        name="Test Bad Date", day=31, month=2, year=2024, hour_val="12:00", gender_val="Nam", is_solar=True
    )
    assert "error" in res_date
    assert res_date["error_code"] == "INVALID_INPUT_PARAMETER"
    assert "suggestions" in res_date
    assert "day" in res_date["suggestions"]

    # 2. Test invalid gender
    res_gender = tuvi_calculator.get_horoscope_chart(
        name="Test Bad Gender", day=15, month=5, year=2024, hour_val="12:00", gender_val="unknown_gender", is_solar=True
    )
    assert "error" in res_gender
    assert res_gender["error_code"] == "INVALID_INPUT_PARAMETER"
    assert "gender_val" in res_gender["suggestions"]

    # 3. Test invalid hour string
    res_hour = tuvi_calculator.get_horoscope_chart(
        name="Test Bad Hour", day=15, month=5, year=2024, hour_val="xyz_abc", gender_val="Nam", is_solar=True
    )
    assert "error" in res_hour
    assert res_hour["error_code"] == "INVALID_INPUT_PARAMETER"
    assert "hour_val" in res_hour["suggestions"]

    # 4. Test invalid transit period
    res_transit = tuvi_calculator.get_van_han_analysis(
        name="Test Transit",
        day=15,
        month=5,
        year=2024,
        hour_val="12:00",
        gender_val="Nam",
        is_solar=True,
        current_year=2500,
        current_month=15,
    )
    assert "error" in res_transit
    assert res_transit["error_code"] == "INVALID_INPUT_PARAMETER"

    # 5. Test MCP tool validations
    from tuvi_mcp.mcp_server import convert_calendar

    # convert_calendar with bad year/month
    conv_err = convert_calendar(day=35, month=13, year=1700)
    assert "error" in conv_err
    assert conv_err["error_code"] == "INVALID_INPUT_PARAMETER"


def test_cach_cuc_evaluation():
    # 1. Schema validation on a generic chart — content can be empty, but
    # `cach_cuc` key must exist and yield a list with required keys when
    # populated. The 10/10/2000 chart is known to trigger several rules.
    chart = tuvi_calculator.get_horoscope_chart("Test Cach Cuc", 10, 10, 2000, "12:00", "Nam", True)
    assert "cach_cuc" in chart
    assert isinstance(chart["cach_cuc"], list)
    if chart["cach_cuc"]:
        first_match = chart["cach_cuc"][0]
        required_keys = ["id", "name", "category", "description", "reason", "co_ca", "binh_chu", "uu_khuyet_diem"]
        for key in required_keys:
            assert key in first_match

    # 2. Pinned chart-rule match: Thạch Trung Ẩn Ngọc Cách (ID 24)
    #    for a 21/8/2003 Nam, giờ Thân chart.
    chart_thach_trung = tuvi_calculator.get_horoscope_chart("Test Thach Trung", 21, 8, 2003, "Thân", "Nam", True)
    matched_ids = [c["id"] for c in chart_thach_trung.get("cach_cuc", [])]
    assert 24 in matched_ids

    # 3. Empty chart input safety
    from tuvi_mcp.cach_cuc_evaluator import evaluate_cach_cuc
    assert evaluate_cach_cuc({}) == []
    assert evaluate_cach_cuc({"dia_ban": []}) == []

    # 4. Real-chart regression tests for the evaluator fixes:
    #    Rule 18 (Minh Châu Xuất Hải Cách) requires `cung_quan`/`cung_tai`
    #    lookups that broke under case-sensitive `==`. 13/5/1989 Tuất Nữ is
    #    a known chart that triggers rule 18, giving an end-to-end smoke.
    chart_rule18 = tuvi_calculator.get_horoscope_chart(
        "Test Rule 18", 13, 5, 1989, "Tuất", "Nữ", True
    )
    ids_rule18 = [r["id"] for r in chart_rule18.get("cach_cuc", [])]
    assert 18 in ids_rule18, "Rule 18 must surface for known chart 13/5/1989 Tuất Nữ"

    # 5. Pinned synthetic chart for rule 51 (Khoa Minh Lộc Ám Cách).
    #    Verifies the canonical Lục Hợp map and `cung_menh` matching.
    #    Mệnh at Hợi (12) → Lục Hợp cung = Dần (3). Placing Hóa Khoa at
    #    Mệnh and Lộc Tồn at Dần must satisfy both rule conditions.
    rule_51_chart = {
        "thien_ban": {"can_nam": "Giáp"},
        "dia_ban": [
            {
                "cung_so": 12, "cung_ten": "Mậu Hợi", "cung_chu": "Mệnh",
                "sao": [{"id": 7, "name": "Hóa khoa", "attribute": "Đắc địa"}],
            },
            {
                "cung_so": 3, "cung_ten": "Quý Dần", "cung_chu": "",
                "sao": [{"id": 8, "name": "Lộc tồn", "attribute": None}],
            },
        ],
    }
    rule_51_matches = [r["id"] for r in evaluate_cach_cuc(rule_51_chart)]
    assert 51 in rule_51_matches, (
        "Rule 51 (Khoa Minh Lộc Ám) must fire when Mệnh has Hóa Khoa "
        "and Lục Hợp cung has Lộc Tồn"
    )


def test_cach_cuc_lookup_helpers():
    from tuvi_mcp.cach_cuc_evaluator import get_cung_by_chu, has_star

    dia_ban = [
        {"cung_so": 1, "cung_ten": "Kỷ Sửu", "cung_chu": "Mệnh", "sao": []},
        {"cung_so": 2, "cung_ten": "Canh Tý", "cung_chu": "Quan lộc", "sao": []},
        {"cung_so": 3, "cung_ten": "Tân Hợi", "cung_chu": "Tài bạch", "sao": []},
        {"cung_so": 4, "cung_ten": "Nhâm Tuất", "cung_chu": "Điền trạch", "sao": []},
    ]

    # Case-insensitive lookup must resolve canonical capitalizations.
    assert get_cung_by_chu(dia_ban, "Mệnh")["cung_so"] == 1
    assert get_cung_by_chu(dia_ban, "Quan Lộc")["cung_so"] == 2
    assert get_cung_by_chu(dia_ban, "Tài Bạch")["cung_so"] == 3
    assert get_cung_by_chu(dia_ban, "Điền Trạch")["cung_so"] == 4
    assert get_cung_by_chu(dia_ban, "Không tồn tại") is None

    # has_star attribute filter: name-only True; mismatch False; match True.
    cung = {"sao": [{"name": "Thái Dương", "attribute": "Miếu địa"}]}
    assert has_star(cung, "Thái Dương") is True
    assert has_star(cung, "Thái Dương", "Hãm địa") is False
    assert has_star(cung, "Thái Dương", "Miếu địa") is True


def test_saved_horoscope_includes_cach_cuc():
    # Save a fresh record; fetch by ID; assert cach_cuc attached.
    from tuvi_mcp import database as db
    db.init_db()
    rid = db.save_horoscope(
        name="Cach Cuc Saved",
        day=21,
        month=8,
        year=2003,
        hour=9,  # Thân
        gender="Nam",
        is_solar=True,
        notes="cach_cuc enrichment test",
    )
    try:
        saved = db.get_saved_horoscope_by_id(rid)
        assert saved is not None
        assert "cach_cuc" in saved
        assert isinstance(saved["cach_cuc"], list)
        matched_ids = [c["id"] for c in saved["cach_cuc"]]
        assert 24 in matched_ids, "Thạch Trung Ẩn Ngọc (24) must surface through saved path"

        saved_by_name = db.get_saved_horoscope_by_name("Cach Cuc Saved")
        assert saved_by_name is not None
        assert "cach_cuc" in saved_by_name
        assert [c["id"] for c in saved_by_name["cach_cuc"]] == matched_ids
    finally:
        db.delete_saved_horoscope_by_id(rid)


def test_auspicious_info():
    from tuvi_mcp.auspicious_calculator import get_auspicious_details
    from tuvi_mcp.mcp_server import get_auspicious_info

    # 1. Test calculation for 27/07/2026
    res = get_auspicious_details(27, 7, 2026, is_solar=True)
    assert "error" not in res
    assert res["duong_lich"] == "27/07/2026"
    assert "Bính Ngọ" in res["am_lich"]
    assert "Nhâm Dần" in res["can_chi_ngay"]
    assert res["ngay_hoang_dao"]["is_hoang_dao"] is True
    assert res["ngay_hoang_dao"]["ten_sao"] == "Kim Quỹ"
    assert res["truc_ngay"]["ten"] == "Trực Nguy"
    assert res["nhi_thap_bat_tu"]["ten"] == "Sao Tâm"
    assert "luc_dieu" not in res
    assert "Đại Thử" in res["tiet_khi_hien_tai"] or "Lập Thu" in res["tiet_khi_hien_tai"]
    assert "Lập Thu" in res["tiet_khi_tiep_theo"] or "Xử Thử" in res["tiet_khi_tiep_theo"]
    assert res["huong_xuat_hanh"]["hy_than"] == "Chính Nam"
    assert len(res["gio_hoang_dao"]) == 12

    # 2. Test MCP tool wrapper with explicit date
    mcp_res = get_auspicious_info(day=27, month=7, year=2026, is_solar=True)
    assert mcp_res == res

    # 3. Test MCP tool wrapper with default values (current date)
    from datetime import datetime
    now = datetime.now()
    default_res = get_auspicious_info()
    assert "error" not in default_res
    assert default_res["duong_lich"] == f"{now.day:02d}/{now.month:02d}/{now.year}"
    # 4. Test edge cases: invalid date validation
    err_res = get_auspicious_info(day=35, month=13, year=2026)
    assert "error" in err_res
    assert err_res["error_code"] == "INVALID_INPUT_PARAMETER"

    # 5. Test 28 Tú Sao Mão key lookup (canonical VN key)
    from tuvi_mcp.auspicious_calculator import XIU_MAP
    assert "Mão" in XIU_MAP
    assert XIU_MAP["Mão"]["ten"] == "Sao Mão"


# Cleanup hook to remove temp file after test session
def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove(db_path)
    except Exception:
        pass

