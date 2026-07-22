#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
"""

import argparse
import sys
from datetime import datetime

from mcp.server.fastmcp import FastMCP, Image

from . import database, tuvi_calculator
from .image_generator import generate_laso_image

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
    for arbitrary birth details without retrieving from or saving to the database.
    - Contrast with `get_saved_horoscope`: Use `generate_horoscope` for new/unsaved calculations.
      Use `get_saved_horoscope` when you want to load a previously saved profile by ID or Name.
    - Contrast with `save_horoscope`: This tool does not persist details. Use `save_horoscope`
      to store details for future quick reference.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: If `generate_image` is `True`, it renders a high-quality PNG chart layout
      and saves it to a temporary path on the local filesystem, returning the file path. It is
      read-only with respect to database/user records.
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
        `cung_so` (1-12), `cung_ten` (name), `cung_chu` (domain), `sao` (list of stars), and
        optional transit/Hạn keys.
    - **Errors**: Returns an error dictionary `{"error": "error_message"}` if calculations fail
      (e.g. invalid date formats, out-of-range birth years).
    """
    try:
        # Calculate standard chart
        chart_data = tuvi_calculator.get_horoscope_chart(
            name=name, day=day, month=month, year=year, hour_val=hour_val, gender_val=gender_val, is_solar=is_solar
        )

        if "error" in chart_data:
            return chart_data

        if not generate_image:
            return chart_data

        if current_year is None:
            current_year = datetime.now().year

        # Calculate transit details
        van_han = tuvi_calculator.get_van_han_analysis(
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
) -> dict:
    """
    Calculate transit stars (sao lưu) and active houses (Đại Hạn, Tiểu Hạn, Nguyệt Hạn)
    for the target Lunar period.

    ### Purpose and Comparison
    Use this tool to perform transit/vận hạn luck analysis (inspecting star shifts, Đại Hạn,
    Tiểu Hạn, and monthly Nguyệt Hạn transits) for a specific target Lunar year and month.
    - Contrast with `generate_horoscope`: Use `get_van_han` specifically for inspecting
      luck/predictions during a specific target timeframe. Use `generate_horoscope` to get
      the static, base birth chart.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: None. This is a read-only calculation and does not write to the database
      or render filesystem files.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites & Calendar Conversions
    - **CRITICAL**: The parameters `current_year` and `current_month` represent the **Lunar** year
      and Lunar month. If the user asks to inspect a specific Solar period (e.g., 'October 2026'
      or 'May 15th, 2026'), you **MUST** first use the `convert_calendar` tool to find the
      corresponding Lunar month/year before calling this tool.

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

    ### Output Schema and Error Conditions
    - **Returns**: A dictionary containing:
      - `person_details`: Summary of demographic details (name, lunar birth date, etc.).
      - `target_period`: Contains `current_year`, `current_year_can_chi`, `current_month_lunar`,
        and `current_age` representing the target period parameters.
      - `transit_stars`: List of transit stars (e.g. Lưu Thái Tuế, Lưu Lộc Tồn) and their
        current coordinates/cung indexes.
      - `dai_han`: Details of the active 10-year major cycle house.
      - `tieu_han`: Details of the active 1-year minor cycle house.
    - **Errors**: Returns an error dictionary `{"error": "error_message"}` if birth details are
      invalid or calculation fails.
    """
    try:
        if current_year is None:
            current_year = datetime.now().year

        return tuvi_calculator.get_van_han_analysis(
            name=name,
            day=day,
            month=month,
            year=year,
            hour_val=hour_val,
            gender_val=gender_val,
            is_solar=is_solar,
            current_year=current_year,
            current_month=current_month,
        )
    except Exception as e:
        return {"error": str(e)}


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
    - The date to convert must represent a valid Gregorian or Chinese Lunar date within
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
        val_err = tuvi_calculator.validate_calendar_convert(day, month, year, timezone=timezone)
        if val_err:
            return val_err

        if from_solar:
            return tuvi_calculator.convert_solar_to_lunar(day, month, year, timezone=timezone)
        else:
            return tuvi_calculator.convert_lunar_to_solar(day, month, year, is_leap=lunar_leap, timezone=timezone)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def save_horoscope(
    name: str, day: int, month: int, year: int, hour_val: str, gender_val: str, is_solar: bool = True, notes: str = None
) -> dict:
    """
    Save birth chart details to the local SQLite database for future retrieval.

    ### Purpose and Comparison
    Use this tool to save a horoscope profile so it can be re-accessed later via ID or Name
    without entering birth details again.
    - Contrast with `generate_horoscope`: Use `save_horoscope` when you want to save details
      permanently. Use `generate_horoscope` if you only want to compute/view a chart on-the-fly
      without database persistence.
    - After saving, you can retrieve the chart using `get_saved_horoscope`.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: Modifies persistent state by inserting a new record into the local
      SQLite database (`~/.tuvi_mcp/tuvi_horoscopes.db`).
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites
    - Local SQLite database must be writable.

    ### Parameter Guidelines & Interactions
    - `name`: Name of the person (required, text).
    - `day`: Day of birth (1-31).
    - `month`: Month of birth (1-12).
    - `year`: Year of birth (four-digit year).
    - `hour_val`: Hour of birth (e.g., "14:30", "Ngọ" or index 1-12).
    - `gender_val`: Gender ("Nam" or "Nữ").
    - `is_solar`: Set to `True` (default) if birth date is Solar, `False` if Lunar.
    - `notes`: Optional textual comments or notes.

    ### Output Schema and Error Conditions
    - **Returns**: A success dictionary containing:
      - `message`: Success confirmation string.
      - `id`: The unique integer ID of the newly created database record.
    - **Errors**: Returns `{"error": "error_message"}` if birth details are invalid or
      database write fails.
    """
    try:
        if not name or not isinstance(name, str) or not name.strip():
            return {
                "error": "Input validation failed",
                "error_code": "INVALID_INPUT_PARAMETER",
                "details": ["Parameter 'name' cannot be empty when saving a horoscope."],
                "suggestions": {"name": "Provide a non-empty string for the person's name."},
            }

        val_err = tuvi_calculator.validate_birth_parameters(day, month, year, hour_val, gender_val, is_solar)
        if val_err:
            return val_err

        hour = tuvi_calculator.parse_hour(hour_val)
        gender_str = "Nam" if tuvi_calculator.parse_gender(gender_val) == 1 else "Nữ"

        record_id = database.save_horoscope(
            name=name, day=day, month=month, year=year, hour=hour, gender=gender_str, is_solar=is_solar, notes=notes
        )
        return {"message": f"Successfully saved horoscope for '{name}' with ID {record_id}.", "id": record_id}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_saved_horoscopes() -> list:
    """
    Retrieve all saved horoscope profiles from the local database.

    ### Purpose and Comparison
    Use this tool to discover previously saved horoscope records, allowing you to find their
    database IDs or names before loading them with `get_saved_horoscope` or removing them
    with `delete_saved_horoscope`.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: Read-only database query. No state modifications or file writes.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites
    - Local SQLite database must exist and be readable.

    ### Output Schema and Error Conditions
    - **Returns**: A list of dictionaries, where each dictionary represents a saved horoscope
      profile with the keys:
      - `id`: The unique integer record ID.
      - `name`: Name of the person.
      - `day`: Day of birth.
      - `month`: Month of birth.
      - `year`: Year of birth.
      - `hour`: Saved hour (as a branch index 1-12).
      - `gender`: Gender ("Nam" or "Nữ").
      - `is_solar`: Boolean (True if Solar, False if Lunar).
      - `notes`: Optional comment string.
      - `created_at`: The database insertion timestamp.
    - **Errors**: Returns a list containing an error dictionary `[{"error": "error_message"}]`
      if database query fails.
    """
    try:
        return database.list_saved_horoscopes()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def get_saved_horoscope(horoscope_id: int = None, name: str = None) -> dict:
    """
    Load a saved horoscope profile from the database and generate its astrological chart.

    ### Purpose and Comparison
    Use this tool to view or analyze a profile that has been previously saved using `save_horoscope`.
    - Contrast with `generate_horoscope`: Use `get_saved_horoscope` to avoid re-entering full
      birth parameters for recurring profiles. Use `generate_horoscope` for raw inputs not saved
      in the database.
    - Contrast with `list_saved_horoscopes`: Use `list_saved_horoscopes` to inspect what records
      exist. Use `get_saved_horoscope` to actually load the record and compute its full chart.
    - Contrast with `delete_saved_horoscope`: Use `delete_saved_horoscope` to permanently remove records.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: Read-only database retrieval and in-memory chart calculations.
      No database writes or file writes.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites
    - The target horoscope record **must** exist in the SQLite database.
    - To check existing records, first run `list_saved_horoscopes`.

    ### Parameter Guidelines & Interactions
    - **At least one** of `horoscope_id` or `name` must be provided.
    - `horoscope_id`: The unique integer ID of the saved database record.
    - `name`: The name of the saved person.
    - **Interactions & Precedence**: If both parameters are supplied, `horoscope_id` takes
      precedence. If only `name` is provided and multiple records match, the **latest** saved
      record for that name is retrieved.

    ### Output Schema and Error Conditions
    - **Returns**: A dictionary containing the full astrological chart structure (`chart_data`)
      with an added `"metadata"` section:
      - `thien_ban`: Demographic, pillars/Can-Chi, and basic zodiac metadata.
      - `dia_ban`: List of 12 houses (cung), each containing names, elements, stars, and transit info.
      - `metadata`: A dictionary with keys `{"id": <int>, "notes": <str>,
        "created_at": <timestamp>}` containing database record details.
    - **Errors**:
      - Returns `{"error": "Horoscope record not found"}` if no matching record exists in the
        database for the given ID or name.
      - Returns `{"error": "error_message"}` if database access fails.
    """
    try:
        if horoscope_id is None and (name is None or not str(name).strip()):
            return {
                "error": "Input validation failed",
                "error_code": "MISSING_REQUIRED_PARAMETER",
                "details": ["At least one of 'horoscope_id' or 'name' must be provided."],
                "suggestions": {
                    "horoscope_id": "Provide a valid integer record ID.",
                    "name": "Or provide a non-empty name string of a saved profile.",
                },
            }

        if horoscope_id is not None and (not isinstance(horoscope_id, int) or isinstance(horoscope_id, bool) or horoscope_id <= 0):
            return {
                "error": "Input validation failed",
                "error_code": "INVALID_INPUT_PARAMETER",
                "details": [f"Invalid horoscope_id '{horoscope_id}'. Must be a positive integer."],
                "suggestions": {"horoscope_id": "Use list_saved_horoscopes to find valid record IDs."},
            }

        record = None
        if horoscope_id is not None:
            record = database.get_saved_horoscope_by_id(horoscope_id)
        elif name is not None:
            record = database.get_saved_horoscope_by_name(name)

        if not record:
            return {"error": "Horoscope record not found"}

        chart = tuvi_calculator.get_horoscope_chart(
            name=record["name"],
            day=record["day"],
            month=record["month"],
            year=record["year"],
            hour_val=record["hour"],
            gender_val=record["gender"],
            is_solar=bool(record["is_solar"]),
        )
        # Include database metadata
        chart["metadata"] = {"id": record["id"], "notes": record["notes"], "created_at": record["created_at"]}
        return chart
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def delete_saved_horoscope(horoscope_id: int) -> dict:
    """
    Delete a saved horoscope record from the local SQLite database by its ID.

    ### Purpose and Comparison
    Use this tool to clean up the database or delete unwanted/incorrectly saved profiles.
    - **CAUTION**: This is a destructive write operation.
    - Contrast with `list_saved_horoscopes`: Use `list_saved_horoscopes` to check available
      profiles and verify the ID before deletion.
    - Contrast with `get_saved_horoscope`: Use `get_saved_horoscope` to load and view the record
      instead of deleting it.

    ### Side Effects, Auth, and Rate Limits
    - **Side Effects**: Permanently deletes the record from the local SQLite database.
      This action is destructive and irreversible.
    - **Auth/Rate Limits**: Runs entirely locally. No authentication or external rate limits apply.

    ### Prerequisites
    - The record with the specified ID must exist in the database.

    ### Parameter Guidelines & Interactions
    - `horoscope_id`: The unique integer ID of the saved database record to delete (required).

    ### Output Schema and Error Conditions
    - **Returns**: A dictionary containing:
      - `message`: Success confirmation string if deletion was successful.
    - **Errors**:
      - Returns `{"error": "No horoscope record found with ID <horoscope_id>."}` if the record
        does not exist.
      - Returns `{"error": "error_message"}` if database deletion fails.
    """
    try:
        if not isinstance(horoscope_id, int) or isinstance(horoscope_id, bool) or horoscope_id <= 0:
            return {
                "error": "Input validation failed",
                "error_code": "INVALID_INPUT_PARAMETER",
                "details": [f"Invalid horoscope_id '{horoscope_id}'. Must be a positive integer."],
                "suggestions": {"horoscope_id": "Use list_saved_horoscopes to find valid record IDs."},
            }

        success = database.delete_saved_horoscope_by_id(horoscope_id)
        if success:
            return {"message": f"Successfully deleted horoscope ID {horoscope_id}."}
        else:
            return {"error": f"No horoscope record found with ID {horoscope_id}."}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Tu Vi horoscope MCP Server.")
    parser.add_argument("--http", action="store_true", help="Use streamable-http transport instead of stdio.")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host.")
    parser.add_argument("--port", type=int, default=1850, help="HTTP port.")
    args = parser.parse_args()

    if args.http:
        print(f"Starting Tu Vi MCP server on streamable-http://{args.host}:{args.port}", file=sys.stderr)
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="streamable-http")
    else:
        print("Starting Tu Vi MCP server on stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
