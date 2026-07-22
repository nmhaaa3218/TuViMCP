# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
"""

import calendar
import re
from datetime import datetime, timedelta

from .ansaotuvi.AmDuong import dichCung, thienCan, timThienMa
from .ansaotuvi.App import lapDiaBan
from .ansaotuvi.DiaBan import diaBan as DiaBanClass
from .ansaotuvi.ThienBan import lapThienBan
from .cach_cuc_evaluator import evaluate_cach_cuc

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


def parse_solar_hour(hour_val) -> int:
    """
    Extract the solar hour (0-23) if the input represents a time of day,
    or None if it is a direct branch index or branch name.
    """
    if isinstance(hour_val, (int, float)):
        # If it is direct branch index (1-12)
        if 1 <= hour_val <= 12 and int(hour_val) == hour_val:
            return None
        return int(hour_val) % 24

    if isinstance(hour_val, str):
        val = hour_val.strip().lower()
        # If it contains an earthly branch name, it is a branch-based input rather than a solar hour
        for k in HOUR_BRANCH_MAP.keys():
            if k in val:
                return None

        # Check if PM/AM is present
        is_pm = False
        if "pm" in val:
            is_pm = True
            val = val.replace("pm", "").strip()
        elif "am" in val:
            val = val.replace("am", "").strip()

        # Match HH:MM or HHhMM or HH
        match = re.search(r"(\d+)(?::|h| |$)", val)
        if match:
            h = int(match.group(1))
            if is_pm and h < 12:
                h += 12
            elif not is_pm and h == 12:
                h = 0
            return h % 24

    return None


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
    """Map gender input to 1 (Male) or -1 (Female)."""
    if isinstance(gender_val, (int, float)):
        return 1 if int(gender_val) >= 1 else -1
    if isinstance(gender_val, bool):
        return 1 if gender_val else -1
    if isinstance(gender_val, str):
        val = gender_val.strip().lower()
        if val in ("nam", "male", "m", "1", "true"):
            return 1
        if val in ("nữ", "nu", "female", "f", "-1", "false"):
            return -1
    return -1


# Month names for error formatting
MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def get_max_days_in_solar_month(month: int, year: int) -> int:
    """Return maximum days in a given solar month and year (e.g. 29 for Feb 2024, 28 for Feb 2025)."""
    try:
        return calendar.monthrange(year, month)[1]
    except Exception:
        return 31


def validate_birth_parameters(
    day: int, month: int, year: int, hour_val, gender_val, is_solar: bool = True
) -> dict:
    """
    Validate birth parameters passed by AI agents or API callers.
    Returns None if all parameters are valid, or a structured dict with
    error details and actionable suggestions if invalid.
    """
    errors = []
    suggestions = {}

    # 1. Validate year
    if not isinstance(year, int) or isinstance(year, bool) or year < 1800 or year > 2100:
        errors.append(f"Invalid year '{year}'. Year must be an integer between 1800 and 2100.")
        suggestions["year"] = "Provide a 4-digit integer year between 1800 and 2100 (e.g., 1995, 2004)."

    # 2. Validate month
    if not isinstance(month, int) or isinstance(month, bool) or month < 1 or month > 12:
        errors.append(f"Invalid month '{month}'. Month must be an integer from 1 to 12.")
        suggestions["month"] = "Provide an integer month between 1 and 12."

    # 3. Validate day and calendar existence
    if not isinstance(day, int) or isinstance(day, bool) or day < 1 or day > 31:
        errors.append(f"Invalid day '{day}'. Day must be an integer from 1 to 31.")
        suggestions["day"] = "Provide a valid day of the month (1-31)."
    elif isinstance(month, int) and 1 <= month <= 12 and isinstance(year, int) and 1800 <= year <= 2100:
        if is_solar:
            try:
                datetime(year, month, day)
            except ValueError:
                max_d = get_max_days_in_solar_month(month, year)
                m_name = MONTH_NAMES[month]
                errors.append(f"Unreal date '{day}/{month}/{year}' ({m_name} {day}, {year} does not exist).")
                suggestions["day"] = f"Provide a real calendar date. {m_name} {year} has a maximum of {max_d} days (1-{max_d})."
        else:
            solar_res = convert_lunar_to_solar(day, month, year, False)
            if "error" in solar_res:
                errors.append(f"Unreal Lunar date '{day}/{month}/{year}' ({solar_res['error']}).")
                suggestions["day"] = f"Verify the specified Lunar day exists in Lunar month {month}/{year}."

    # 4. Validate gender_val
    if isinstance(gender_val, str):
        val = gender_val.strip().lower()
        valid_genders = {"nam", "nữ", "nu", "male", "female", "m", "f", "1", "-1", "true", "false"}
        if val not in valid_genders:
            errors.append(f"Invalid gender_val '{gender_val}'.")
            suggestions["gender_val"] = "Must be one of: 'Nam', 'Nữ', 'male', 'female'."
    elif not isinstance(gender_val, (int, float, bool)):
        errors.append(f"Invalid gender_val type '{type(gender_val).__name__}'.")
        suggestions["gender_val"] = "Must be a string ('Nam' or 'Nữ'), integer (1 or -1), or boolean."

    # 5. Validate hour_val
    if isinstance(hour_val, (int, float)) and not isinstance(hour_val, bool):
        if not (1 <= hour_val <= 12 and int(hour_val) == hour_val) and not (0 <= hour_val <= 23):
            errors.append(f"Invalid numeric hour_val '{hour_val}'.")
            suggestions["hour_val"] = "Must be an integer branch index (1-12) or hour of day (0-23)."
    elif isinstance(hour_val, str):
        val = hour_val.strip().lower()
        matched_branch = any(k in val for k in HOUR_BRANCH_MAP.keys())
        matched_time = re.search(r"(\d+)(?::|h| |$)", val) is not None
        if not matched_branch and not matched_time:
            try:
                v_int = int(val)
                if not (1 <= v_int <= 12 or 0 <= v_int <= 23):
                    errors.append(f"Invalid hour_val '{hour_val}'.")
                    suggestions["hour_val"] = "Must be a time string ('14:30'), Earthly Branch name ('Ngọ'), or branch index (1-12)."
            except ValueError:
                errors.append(f"Invalid hour_val '{hour_val}'.")
                suggestions["hour_val"] = "Must be a time string ('14:30'), Earthly Branch name ('Ngọ'), or branch index (1-12)."
    elif hour_val is not None:
        errors.append(f"Invalid hour_val type '{type(hour_val).__name__}'.")
        suggestions["hour_val"] = "Must be a time string ('14:30'), Earthly Branch name ('Ngọ'), or branch index (1-12)."

    if errors:
        return {
            "error": "Input validation failed",
            "error_code": "INVALID_INPUT_PARAMETER",
            "details": errors,
            "suggestions": suggestions,
        }
    return None


def validate_transit_period(current_year: int = None, current_month: int = 1) -> dict:
    """Validate target transit period parameters."""
    errors = []
    suggestions = {}

    if current_year is not None:
        if not isinstance(current_year, int) or isinstance(current_year, bool) or current_year < 1800 or current_year > 2100:
            errors.append(f"Invalid current_year '{current_year}'. Year must be an integer between 1800 and 2100.")
            suggestions["current_year"] = "Provide a 4-digit integer year between 1800 and 2100 (e.g., 2026)."

    if current_month is not None:
        if not isinstance(current_month, int) or isinstance(current_month, bool) or current_month < 1 or current_month > 12:
            errors.append(f"Invalid current_month '{current_month}'. Month must be an integer from 1 to 12.")
            suggestions["current_month"] = "Provide an integer Lunar month between 1 and 12."

    if errors:
        return {
            "error": "Input validation failed",
            "error_code": "INVALID_INPUT_PARAMETER",
            "details": errors,
            "suggestions": suggestions,
        }
    return None


def validate_calendar_convert(day: int, month: int, year: int, from_solar: bool = True, lunar_leap: bool = False, timezone: int = 7) -> dict:
    """Validate calendar conversion input parameters."""
    errors = []
    suggestions = {}

    if not isinstance(year, int) or isinstance(year, bool) or year < 1800 or year > 2100:
        errors.append(f"Invalid year '{year}'. Year must be an integer between 1800 and 2100.")
        suggestions["year"] = "Provide a 4-digit integer year between 1800 and 2100."

    if not isinstance(month, int) or isinstance(month, bool) or month < 1 or month > 12:
        errors.append(f"Invalid month '{month}'. Month must be an integer from 1 to 12.")
        suggestions["month"] = "Provide an integer month between 1 and 12."

    if not isinstance(day, int) or isinstance(day, bool) or day < 1 or day > 31:
        errors.append(f"Invalid day '{day}'. Day must be an integer from 1 to 31.")
        suggestions["day"] = "Provide an integer day between 1 and 31."
    elif isinstance(month, int) and 1 <= month <= 12 and isinstance(year, int) and 1800 <= year <= 2100:
        if from_solar:
            try:
                datetime(year, month, day)
            except ValueError:
                max_d = get_max_days_in_solar_month(month, year)
                m_name = MONTH_NAMES[month]
                errors.append(f"Unreal date '{day}/{month}/{year}' ({m_name} {day}, {year} does not exist).")
                suggestions["day"] = f"Provide a real calendar date. {m_name} {year} has a maximum of {max_d} days (1-{max_d})."
        else:
            solar_res = convert_lunar_to_solar(day, month, year, lunar_leap, timezone)
            if "error" in solar_res:
                errors.append(f"Unreal Lunar date '{day}/{month}/{year}' ({solar_res['error']}).")
                suggestions["day"] = "Verify the maximum days for the specified Lunar month and year."

    if not isinstance(timezone, (int, float)) or timezone < -12 or timezone > 14:
        errors.append(f"Invalid timezone '{timezone}'. Timezone offset must be between -12 and 14.")
        suggestions["timezone"] = "Provide a numeric UTC offset (default 7 for ICT)."

    if errors:
        return {
            "error": "Input validation failed",
            "error_code": "INVALID_INPUT_PARAMETER",
            "details": errors,
            "suggestions": suggestions,
        }
    return None


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


def adjust_date_for_late_ty(day: int, month: int, year: int, hour_val, is_solar: bool):
    """
    If birth hour is 23 (late Tý hour), roll calculation date forward by +1 day.
    Returns: (calc_day, calc_month, calc_year, orig_solar_str, is_late_ty)
    """
    is_late_ty = (parse_solar_hour(hour_val) == 23)
    calc_day, calc_month, calc_year = day, month, year

    # Pre-calculate original solar date string
    if is_solar:
        orig_solar_str = f"{day}/{month}/{year}"
    else:
        # Convert lunar to solar to find the original solar date
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
                solar_res = convert_lunar_to_solar(day, month, year, False, 7)
                if "error" not in solar_res:
                    dt = datetime(solar_res["solar_year"], solar_res["solar_month"], solar_res["solar_day"]) + timedelta(days=1)
                    lunar_res = convert_solar_to_lunar(dt.day, dt.month, dt.year, 7)
                    if "error" not in lunar_res:
                        calc_day, calc_month, calc_year = lunar_res["lunar_day"], lunar_res["lunar_month"], lunar_res["lunar_year"]
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
        "ngay_duong": orig_solar_str if (is_late_ty and orig_solar_str) else f"{tb.ngayDuong}/{tb.thangDuong}/{tb.namDuong}",
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
    validation_err = validate_birth_parameters(day, month, year, hour_val, gender_val, is_solar)
    if validation_err:
        return validation_err
    transit_err = validate_transit_period(current_year, current_month)
    if transit_err:
        return transit_err
    hour = parse_hour(hour_val)
    gender = parse_gender(gender_val)

    calc_day, calc_month, calc_year, _, _ = adjust_date_for_late_ty(
        day, month, year, hour_val, is_solar
    )

    # Calculate birth details first
    db, tb = build_raw_chart(calc_day, calc_month, calc_year, hour, gender, is_solar, name)
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


def convert_solar_to_lunar(day: int, month: int, year: int, timezone: int = 7) -> dict:
    """
    Convert a Solar date (Dương lịch) to the corresponding Lunar date (Âm lịch).
    Returns a dictionary containing lunar day, month, year, leap status, and a formatted string.
    """
    from .ansaotuvi.Lich_HND import S2L

    try:
        res = S2L(day, month, year, timeZone=timezone)
        return {
            "lunar_day": res[0],
            "lunar_month": res[1],
            "lunar_year": res[2],
            "lunar_leap": bool(res[3]),
            "formatted": f"{res[0]}/{res[1]}/{res[2]}" + (" (nhận)" if res[3] else ""),
        }
    except Exception as e:
        return {"error": f"Failed to convert Solar to Lunar: {str(e)}"}


def convert_lunar_to_solar(day: int, month: int, year: int, is_leap: bool = False, timezone: int = 7) -> dict:
    """
    Convert a Lunar date (Âm lịch) to the corresponding Solar date (Dương lịch).
    Returns a dictionary containing solar day, month, year, and a formatted string.
    """
    from .ansaotuvi.Lich_HND import L2S, getLeapMonthOffset, getLunarMonth11

    try:
        # Validate leap month parameters
        if is_leap:
            if month < 11:
                a11 = getLunarMonth11(year - 1, timezone)
                b11 = getLunarMonth11(year, timezone)
            else:
                a11 = getLunarMonth11(year, timezone)
                b11 = getLunarMonth11(year + 1, timezone)

            if b11 - a11 <= 365:
                return {"error": f"Lunar year {year} is not a leap year. No leap month exists."}

            leapOff = getLeapMonthOffset(a11, timezone)
            leapM = leapOff - 2
            if leapM < 0:
                leapM += 12
            if month != leapM:
                return {
                    "error": (
                        f"Lunar month {month} is not the leap month of year {year}. "
                        f"The leap month is month {leapM}."
                    )
                }

        leap_val = 1 if is_leap else 0
        res = L2S(day, month, year, leap_val, tZ=timezone)
        if res == [0, 0, 0]:
            return {"error": "Invalid lunar date or invalid leap month configuration."}
        return {
            "solar_day": res[0],
            "solar_month": res[1],
            "solar_year": res[2],
            "formatted": f"{res[0]}/{res[1]}/{res[2]}",
        }
    except Exception as e:
        return {"error": f"Failed to convert Lunar to Solar: {str(e)}"}
