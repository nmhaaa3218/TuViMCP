import re

from .ansaotuvi.AmDuong import dichCung, thienCan, timThienMa
from .ansaotuvi.App import lapDiaBan
from .ansaotuvi.DiaBan import diaBan as DiaBanClass
from .ansaotuvi.ThienBan import lapThienBan

# Branch maps
BRANCH_NAMES = ["", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

CAN_NAMES = ["", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

HOUR_BRANCH_MAP = {
    "tý": 1,
    "sửu": 2,
    "dần": 3,
    "mão": 4,
    "thìn": 5,
    "tỵ": 6,
    "ngọ": 7,
    "mùi": 8,
    "thân": 9,
    "dậu": 10,
    "tuất": 11,
    "hợi": 12,
}


def parse_hour(hour_val) -> int:
    """
    Parse the hour input into the 1-indexed Earthly Branch index (1-12).
    Allows:
    - Integer/float 1-12 directly representing branch index.
    - Integer/float representing hour of day (0-23).
    - String name of branch (e.g. "Tý", "ngo").
    - String representing time of day (e.g. "14:30", "11h15").
    """
    if isinstance(hour_val, (int, float)):
        # If it is direct branch index
        if 1 <= hour_val <= 12 and int(hour_val) == hour_val:
            return int(hour_val)
        # Otherwise, treat as hour of day
        h = int(hour_val) % 24
        return map_hour_of_day_to_branch(h)

    if isinstance(hour_val, str):
        val = hour_val.strip().lower()
        # Check if matches direct branch name
        for k, v in HOUR_BRANCH_MAP.items():
            if k in val:
                return v

        # Try to parse as HH:MM or HHhMM
        match = re.search(r"(\d+)(?::|h| |$)", val)
        if match:
            h = int(match.group(1)) % 24
            return map_hour_of_day_to_branch(h)

        # Try to convert string integer
        try:
            val_int = int(val)
            if 1 <= val_int <= 12:
                return val_int
            return map_hour_of_day_to_branch(val_int % 24)
        except ValueError:
            pass

    # Default to Tý (1)
    return 1


def map_hour_of_day_to_branch(h: int) -> int:
    """Map solar hour (0-23) to 1-indexed Earthly Branch (1-12)."""
    if h == 23 or h == 0:
        return 1  # Tý (23:00 - 00:59)
    elif h == 1 or h == 2:
        return 2  # Sửu (01:00 - 02:59)
    elif h == 3 or h == 4:
        return 3  # Dần (03:00 - 04:59)
    elif h == 5 or h == 6:
        return 4  # Mão (05:00 - 06:59)
    elif h == 7 or h == 8:
        return 5  # Thìn (07:00 - 08:59)
    elif h == 9 or h == 10:
        return 6  # Tỵ (09:00 - 10:59)
    elif h == 11 or h == 12:
        return 7  # Ngọ (11:00 - 12:59)
    elif h == 13 or h == 14:
        return 8  # Mùi (13:00 - 14:59)
    elif h == 15 or h == 16:
        return 9  # Thân (15:00 - 16:59)
    elif h == 17 or h == 18:
        return 10  # Dậu (17:00 - 18:59)
    elif h == 19 or h == 20:
        return 11  # Tuất (19:00 - 20:59)
    elif h == 21 or h == 22:
        return 12  # Hợi (21:00 - 22:59)
    return 1


def parse_gender(gender_val) -> int:
    """Map gender input to 1 (Male) or 0 (Female)."""
    if isinstance(gender_val, (int, float)):
        return 1 if int(gender_val) == 1 else 0
    if isinstance(gender_val, bool):
        return 1 if gender_val else 0
    if isinstance(gender_val, str):
        val = gender_val.strip().lower()
        if val in ("nam", "male", "m", "1", "true"):
            return 1
    return 0


SAO_ATTRIBUTE_MAP = {"M": "Miếu địa", "V": "Vượng địa", "Đ": "Đắc địa", "B": "Bình hòa", "H": "Hãm địa"}


def serialize_sao(sao_dict):
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


def get_horoscope_chart(
    name: str, day: int, month: int, year: int, hour_val, gender_val, is_solar: bool = True
) -> dict:
    """Standardized entry point to calculate and return full horoscope JSON."""
    hour = parse_hour(hour_val)
    gender = parse_gender(gender_val)

    db, tb = build_raw_chart(day, month, year, hour, gender, is_solar, name)

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
        "ngay_duong": f"{tb.ngayDuong}/{tb.thangDuong}/{tb.namDuong}",
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

    return {"thien_ban": thien_ban_data, "dia_ban": cungs}


def calculate_transit_stars(current_year: int) -> list:
    """Calculate the positions of the transit stars (sao lưu) for a target year."""
    # current_year can and chi
    can_nam = (current_year + 6) % 10 + 1
    chi_nam = (current_year + 8) % 12 + 1

    # Lưu Thái Tuế: at branch of target year
    luu_thai_tue = chi_nam

    # Lưu Lộc Tồn: based on Can of target year
    # vitriDiaBan matches thienCan table
    luu_loc_ton = thienCan[can_nam]["vitriDiaBan"]

    # Lưu Kình Dương and Lưu Đà La relative to Lộc Tồn
    luu_kinh_duong = dichCung(luu_loc_ton, 1)
    luu_da_la = dichCung(luu_loc_ton, -1)

    # Lưu Thiên Mã: based on Chi of target year
    luu_thien_ma = timThienMa(chi_nam)

    # Lưu Thiên Khốc and Lưu Thiên Hư: start from Ngọ (7)
    luu_thien_khoc = dichCung(7, -chi_nam + 1)
    luu_thien_hu = dichCung(7, chi_nam - 1)

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
) -> dict:
    """Analyze yearly transit stars and active cungs (Đại Hạn, Tiểu Hạn, Nguyệt Hạn) for current year/month."""
    hour = parse_hour(hour_val)
    gender = parse_gender(gender_val)

    # Calculate birth details first
    db, tb = build_raw_chart(day, month, year, hour, gender, is_solar, name)
    chart = get_horoscope_chart(name, day, month, year, hour_val, gender_val, is_solar)

    # Current lunar year and branch
    curr_can = (current_year + 6) % 10 + 1
    curr_chi = (current_year + 8) % 12 + 1
    curr_year_can_chi = f"{CAN_NAMES[curr_can]} {BRANCH_NAMES[curr_chi]}"

    # Calculate current age (tuổi mụ)
    # lunar birth year
    birth_lunar_year = tb.namAm
    age = current_year - birth_lunar_year + 1

    # 1. Identify active Đại Hạn cung
    active_dai_han_cung = None
    for cung in chart["dia_ban"]:
        cung["cung_so"]
        dai_han_start = cung["dai_han"]
        if dai_han_start is not None:
            if dai_han_start <= age < dai_han_start + 10:
                active_dai_han_cung = cung
                break

    # 2. Identify active Tiểu Hạn cung
    active_tieu_han_cung = None
    for cung in chart["dia_ban"]:
        # cung_tieu_han is name of Earthly Branch (e.g. "Ngọ")
        if cung["tieu_han"] == BRANCH_NAMES[curr_chi]:
            active_tieu_han_cung = cung
            break

    # 3. Identify active Nguyệt Hạn cung
    active_nguyet_han_cung = None
    if active_tieu_han_cung:
        # 0-indexed positions
        p_tieu_han = active_tieu_han_cung["cung_so"] - 1
        m_birth = tb.thangAm
        h_birth = hour
        m_target = current_month

        p_month = (p_tieu_han - m_birth + h_birth + m_target - 1) % 12
        s_month = p_month + 1  # 1-indexed cungSo

        for cung in chart["dia_ban"]:
            if cung["cung_so"] == s_month:
                active_nguyet_han_cung = cung
                break

    # Calculate transit stars
    transits = calculate_transit_stars(current_year)

    # Append transit stars to their corresponding cungs in the return data
    # to let the AI see them easily
    cung_transits = {i: [] for i in range(1, 13)}
    for t in transits:
        cung_transits[t["cung_so"]].append(t["name"])

    # Build enriched results
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
    }
