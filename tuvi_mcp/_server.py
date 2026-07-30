#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

FastMCP server definition. CLI is in `__main__.py`.
"""

from datetime import datetime

from mcp.server.fastmcp import FastMCP, Image

from . import _calendar, _chart, _input, _transit
from ._auspicious import get_auspicious_details as _get_auspicious_details
from ._rendering import generate_laso_image

mcp = FastMCP("TuViMCP")


@mcp.tool(structured_output=False)
def generate_horoscope(
    name: str = "Khách",
    day: int = 1,
    month: int = 1,
    year: int = 1990,
    hour_val: str = "12:00",
    gender_val: str = "Nam",
    is_solar: bool = True,
    current_year: int = None,
    generate_image: bool = True,
):
    """
    Generate a full Tu Vi (Vietnamese horoscope) chart from raw birth details,
    with optional high-quality visual chart image rendering.

    ### Purpose and Comparison
    Use this tool when you want to compute and inspect an astrological birth chart from scratch
    for arbitrary birth details.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: If `generate_image` is `True`, it renders a high-quality PNG chart layout
      and saves it to a temporary path on the local filesystem, returning the file path. It is
      read-only and stateless.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites
    - The date parameters must form a valid date in either the Solar or Lunar calendar.

    ### Parameter Guidelines & Interactions
    - `name`: Name of the subject (default: "Khách").
    - `day`: Day of birth (1-31).
    - `month`: Month of birth (1-12).
    - `year`: Year of birth (e.g., 1995).
    - `hour_val`: Hour of birth. Accepts string formats like "14:30", "Ngọ" (Earthly Branch name),
      or numeric branch index (1-12, where 1=Tý, 12=Hợi) (default: "12:00").
    - `gender_val`: Gender of the subject. Accepts "Nam", "Nữ", "male", "female"
      (case-insensitive, default: "Nam").
    - `is_solar`: Set to `True` (default) if the birth date is Solar (Dương lịch). Set to `False`
      if it is Lunar (Âm lịch).
    - `current_year`: Year to calculate transit stars/Vận Hạn for (default: system current year,
      e.g., 2026).
    - `generate_image`: Set to `True` (default) to render and return a visual PNG chart along
      with raw data. Set to `False` to return only raw data.

    ### Output Schema and Error Conditions
    - **If `generate_image` is `True`**: Returns a list `[Image, chart_data]` where `Image` is a
      FastMCP Image object pointing to the generated PNG file on disk, and `chart_data` is a
      dictionary containing structured chart details (demographics, houses, stars).
    - **If `generate_image` is `False`**: Returns only the `chart_data` dictionary.
    - **Structure of `chart_data`**:
      - `thien_ban`: Dict containing calculated demographics, pillars/Can-Chi (year, month, day,
        hour), element (Hành Cục), destiny (Bản Mệnh), etc.
      - `dia_ban`: List of 12 dicts, each representing an astrological house (cung), including
        `cung_so` (1-12), `cung_ten` (name), `cung_chu` (domain), `sao` (list of stars),
        `quan_he_hinh_hoc` (static 100% geometric relationships: `xung_chieu`, `tam_hop`, `nhi_hop`, `giap_cung`),
        and optional transit/Hạn keys.
    - **Errors**: Returns an error dictionary `{"error": "error_message"}` if calculations fail
      (e.g. invalid date formats, out-of-range birth years).
    """
    try:
        # Calculate standard chart
        chart_data = _chart.get_horoscope_chart(
            name=name, day=day, month=month, year=year, hour_val=hour_val, gender_val=gender_val, is_solar=is_solar
        )

        if "error" in chart_data:
            return chart_data

        if not generate_image:
            return chart_data

        if current_year is None:
            current_year = datetime.now().year

        # Calculate transit details
        van_han = _transit.get_van_han_analysis(
            name=name,
            day=day,
            month=month,
            year=year,
            hour_val=hour_val,
            gender_val=gender_val,
            is_solar=is_solar,
            current_year=current_year,
        )

        # Merge transit details into chart_data
        if "error" not in van_han:
            chart_data["transit_stars"] = van_han.get("transit_stars", [])
            chart_data["target_period"] = van_han.get("target_period", {})
            chart_data["dai_han"] = van_han.get("dai_han", {})
            chart_data["tieu_han"] = van_han.get("tieu_han", {})

        image_path = generate_laso_image(chart_data, current_year=current_year)
        return [Image(path=image_path), chart_data]
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_van_han(
    name: str = "Khách",
    day: int = 1,
    month: int = 1,
    year: int = 1990,
    hour_val: str = "12:00",
    gender_val: str = "Nam",
    is_solar: bool = True,
    current_year: int = None,
    current_month: int = 1,
    current_day: int = None,
) -> dict:
    """
    Calculate transit stars (sao lưu) and active houses (Đại Hạn, Tiểu Hạn, Nguyệt Hạn, Nhật Hạn)
    for the target Lunar period.

    ### Purpose and Comparison
    Use this tool to perform transit/vận hạn luck analysis (inspecting star shifts, Đại Hạn,
    Tiểu Hạn, monthly Nguyệt Hạn transits, and daily Nhật Hạn) for a specific target Lunar
    year, month, and optionally day.
    - Contrast with `generate_horoscope`: Use `get_van_han` specifically for inspecting
      luck/predictions during a specific target timeframe. Use `generate_horoscope` to get
      the static, base birth chart.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: None. This is a read-only calculation and does not write to the database
      or render filesystem files.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites & Calendar Conversions
    - **CRITICAL**: The parameters `current_year`, `current_month`, and (if provided) `current_day`
      represent the **Lunar** year, Lunar month, and Lunar day. If the user asks to inspect a
      specific Solar period (e.g., 'October 2026' or 'May 15th, 2026'), you **MUST** first use
      the `convert_calendar` tool to find the corresponding Lunar month/year/day before calling
      this tool.

    ### Parameter Guidelines & Interactions
    - `name`: Name of the person.
    - `day`: Day of birth (1-31).
    - `month`: Month of birth (1-12).
    - `year`: Year of birth.
    - `hour_val`: Hour of birth (e.g., "14:30", "Ngọ").
    - `gender_val`: Gender ("Nam" or "Nữ").
    - `is_solar`: True if birth date is Solar (Dương lịch), False if Lunar (Âm lịch).
    - `current_year`: Target Lunar year to inspect (defaults to current system year, e.g., 2026).
    - `current_month`: Target Lunar month to inspect (1-12, default 1).
    - `current_day`: Target Lunar day to inspect (1-30, optional). When provided, also returns
      `nhat_han` — the daily transit house derived from Nguyệt Hạn.

    ### Output Schema and Error Conditions
    - **Returns**: A dictionary containing:
      - `person_details`: Summary of demographic details (name, lunar birth date, etc.).
      - `target_period`: Contains `current_year`, `current_year_can_chi`, `current_month_lunar`,
        and `current_age` representing the target period parameters.
      - `transit_stars`: List of transit stars (e.g. Lưu Thái Tuế, Lưu Lộc Tồn) and their
        current coordinates/cung indexes.
      - `dai_han`: Details of the active 10-year major cycle house.
      - `tieu_han`: Details of the active 1-year minor cycle house.
      - `nguyet_han`: Details of the active monthly cycle house.
      - `nhat_han`: (only if `current_day` is provided) Details of the active daily house,
        derived from Nguyệt Hạn.
    - **Errors**: Returns an error dictionary `{"error": "error_message"}` if birth details are
      invalid or calculation fails.
    """
    try:
        if current_year is None:
            current_year = datetime.now().year

        return _transit.get_van_han_analysis(
            name=name,
            day=day,
            month=month,
            year=year,
            hour_val=hour_val,
            gender_val=gender_val,
            is_solar=is_solar,
            current_year=current_year,
            current_month=current_month,
            current_day=current_day,
        )
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_auspicious_info(
    day: int = None,
    month: int = None,
    year: int = None,
    is_solar: bool = True,
) -> dict:
    """
    Evaluate Auspicious Days (Ngày Hoàng Đạo / Hắc Đạo), Auspicious Hours (Giờ Hoàng Đạo / Hắc Đạo),
    12 Trực, 28 Tú (Nhị Thập Bát Tú), Tiết Khí, and Auspicious Directions (Thần Hướng).

    ### Purpose and Use Cases
    Use this tool when users ask to check good/bad days, auspicious hours for specific activities
    (wedding, opening a store, starting construction, signing contracts, travel/auspicious direction),
    12 Trực, 28 Tú, or Tiết Khí for a given calendar date.

    ### Parameters
    - `day`: Day of month (1-31). Defaults to current day if omitted.
    - `month`: Month of year (1-12). Defaults to current month if omitted.
    - `year`: Year (four digits e.g. 2026). Defaults to current year if omitted.
    - `is_solar`: Set to `True` (default) for Solar date (Dương lịch), or `False` for Lunar date (Âm lịch).

    ### Returns
    A rich Vietnamese JSON structure detailing:
    - `duong_lich`, `am_lich`, `can_chi_ngay`
    - `tiet_khi_hien_tai`, `tiet_khi_tiep_theo`
    - `ngay_hoang_dao` (Sao Hoàng Đạo/Hắc Đạo, Cát/Hung)
    - `truc_ngay` (Tên Trực, Cát/Hung, Lời khuyên cổ truyền)
    - `nhi_thap_bat_tu` (Tên Sao, Động vật, Cát/Hung)
    - `huong_xuat_hanh` (Hỷ Thần, Tài Thần, Phúc Thần, Dương/Âm Quý Thần)
    - `gio_hoang_dao` (12 Giờ Canh Chi, Khung giờ, Sao Hoàng Đạo/Hắc Đạo, Cát/Hung)
    """
    now = datetime.now()
    if day is None:
        day = now.day
    if month is None:
        month = now.month
    if year is None:
        year = now.year

    return _get_auspicious_details(day, month, year, is_solar=is_solar)


@mcp.tool()
def convert_calendar(
    day: int,
    month: int,
    year: int,
    from_solar: bool = True,
    lunar_leap: bool = False,
    timezone: int = 7,
) -> dict:
    """
    Convert a date between the Solar (Dương lịch) and Lunar (Âm lịch) calendars.

    ### Purpose and Comparison
    Use this tool to translate dates back and forth between Solar and Lunar systems.
    - **CRITICAL FOR TRANSIT ASSESSMENTS**: Since Tu Vi transit calculations (sao lưu, Đại Hạn,
      Tiểu Hạn, Nguyệt Hạn) operate strictly on the Lunar calendar, you **MUST** convert any Solar
      target periods (e.g. "October 2026") using this tool before calling `get_van_han`.
    - Do NOT use this tool if you only need base chart calculation, as chart generation tools
      (`generate_horoscope` and `get_saved_horoscope`) already handle birth date conversions internally.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: None. This is a pure mathematical calculation.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites
    - The date to convert must represent a valid Gregorian or Vietnamese Lunar date within
      calendar ranges (typically 1900-2100).

    ### Parameter Guidelines & Interactions
    - `day`: Day of the date to convert (1-31).
    - `month`: Month of the date to convert (1-12).
    - `year`: Year of the date to convert (four-digit year).
    - `from_solar`: If `True` (default), converts Solar to Lunar. If `False`, converts Lunar to Solar.
    - `lunar_leap`: Only applicable when `from_solar=False`. Set to `True` if the source Lunar
      month is a leap month (tháng nhuận); otherwise `False`.
    - `timezone`: Timezone offset (default: 7, matching Vietnam/ICT).

    ### Output Schema and Error Conditions
    - **Returns**: A dictionary containing:
      - `day`: Converted day (int).
      - `month`: Converted month (int).
      - `year`: Converted year (int).
      - `leap`: Boolean indicating if the Lunar month is a leap month.
    - **Errors**: Returns `{"error": "error_message"}` if date arguments are out of bounds or
      fail calendar validation.
    """
    try:
        val_err = _input.validate_calendar_convert(day, month, year, timezone=timezone)
        if val_err:
            return val_err

        if from_solar:
            return _calendar.convert_solar_to_lunar(day, month, year, timezone=timezone)
        else:
            return _calendar.convert_lunar_to_solar(day, month, year, is_leap=lunar_leap, timezone=timezone)
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    """Backward-compatible CLI entry; delegates to ``__main__.main``."""
    from .__main__ import main as _main

    _main()
