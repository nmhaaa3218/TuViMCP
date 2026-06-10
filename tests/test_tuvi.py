import os
import tempfile
import pytest

# Create a temporary file path for the database before importing database
db_fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(db_fd)  # Close file descriptor so sqlite can open it
os.environ["TUVI_DB_PATH"] = db_path

# Now import the target modules
from tuvi_mcp import database, tuvi_calculator

def test_hour_parsing():
    assert tuvi_calculator.parse_hour("14:30") == 8   # Mùi
    assert tuvi_calculator.parse_hour("Ngọ") == 7     # Ngọ
    assert tuvi_calculator.parse_hour("tý") == 1      # Tý
    assert tuvi_calculator.parse_hour(13.5) == 8      # Mùi (13.5 -> hour 13 of day -> Mùi)
    assert tuvi_calculator.parse_hour(3) == 3         # Direct branch index 3 -> Dần

def test_chart_generation():
    chart = tuvi_calculator.get_horoscope_chart(
        name="Nguyễn Văn A",
        day=10,
        month=6,
        year=1995,
        hour_val="14:30",
        gender_val="Nam",
        is_solar=True
    )
    assert chart["thien_ban"]["ten"] == "Nguyễn Văn A"
    assert chart["thien_ban"]["gioi_tinh"] == "Nam"
    assert len(chart["dia_ban"]) == 12
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
        current_month=5
    )
    assert van_han["target_period"]["current_year"] == 2026
    assert van_han["target_period"]["current_month_lunar"] == 5
    assert len(van_han["transit_stars"]) == 7
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
        hour=5, # Mão
        gender="Nữ",
        is_solar=False,
        notes="Test notes"
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

# Cleanup hook to remove temp file after test session
def pytest_sessionfinish(session, exitstatus):
    try:
        os.remove(db_path)
    except Exception:
        pass
