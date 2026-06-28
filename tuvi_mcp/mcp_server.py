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
    Generate a full Tu Vi (Vietnamese horoscope) chart, with optional high-quality chart image rendering.

    Args:
        name: Name of the person.
        day: Day of birth (1-31).
        month: Month of birth (1-12).
        year: Year of birth (e.g. 1990).
        hour_val: Hour of birth (e.g. "14:30", "Ngọ", "Tý", or index 1-12 where 1=Tý, 12=Hợi).
        gender_val: Gender ("Nam", "Nữ", "male", "female").
        is_solar: True if birth date is Solar (Dương lịch), False if Lunar (Âm lịch).
        current_year: Year to inspect transit stars for (defaults to current year, e.g. 2026).
        generate_image: Whether to generate and return the high-quality chart image along with the chart data.
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
    for the current month/year to inspect luck and predictions (vận hạn).

    CRITICAL: The parameters `current_year` and `current_month` represent the Lunar year and Lunar month.
    If the user asks to inspect a specific Solar period (e.g. 'October 2026'), you MUST first use
    the `convert_calendar` tool to find the corresponding Lunar month/year before calling this tool.

    Args:
        name: Name of the person.
        day: Day of birth (1-31).
        month: Month of birth (1-12).
        year: Year of birth.
        hour_val: Hour of birth (e.g. "14:30", "Ngọ").
        gender_val: Gender ("Nam" or "Nữ").
        is_solar: True if birth date is Solar (Dương lịch), False if Lunar (Âm lịch).
        current_year: Lunar year to inspect (defaults to current lunar year, e.g. 2026).
        current_month: Lunar month to inspect (1-12, default 1).
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

    CRITICAL FOR TRANSIT ASSESSMENTS: Because Tu Vi horoscope transit analyses (sao lưu, Đại Hạn, Tiểu Hạn, Nguyệt Hạn)
    are calculated strictly against the Lunar calendar, if a user asks to inspect a specific target period using
    Solar dates/months (e.g. 'October 2026' or 'May 15th, 2026'), you MUST first call this tool with `from_solar=True`
    to convert that target Solar date/month to its corresponding Lunar date/month/year. Then, pass the resulting
    Lunar month and year to other tools (such as `get_van_han`'s `current_month` and `current_year` parameters).

    Args:
        day: Day of the date to convert.
        month: Month of the date to convert.
        year: Year of the date to convert.
        from_solar: True to convert Solar to Lunar (default). False to convert Lunar to Solar.
        lunar_leap: Only used when from_solar=False. True if the input lunar month is a leap month (tháng nhuận).
        timezone: Timezone offset (default is 7 for Vietnam/ICT).
    """
    try:
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
    Save birth chart details to the local database for easy retrieval.

    Args:
        name: Name of the person.
        day: Day of birth.
        month: Month of birth.
        year: Year of birth.
        hour_val: Hour of birth (e.g. "14:30", "Ngọ").
        gender_val: Gender ("Nam" or "Nữ").
        is_solar: True if birth date is Solar, False if Lunar.
        notes: Optional comments/notes.
    """
    try:
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
    Retrieve all saved horoscopes from the local database.
    """
    try:
        return database.list_saved_horoscopes()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def get_saved_horoscope(horoscope_id: int = None, name: str = None) -> dict:
    """
    Load a saved horoscope and generate its chart. Provide either horoscope_id or name.

    Args:
        horoscope_id: The database ID of the horoscope.
        name: Name of the person (retrieves the latest record).
    """
    try:
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
    Delete a saved horoscope record from the database.

    Args:
        horoscope_id: The database ID of the horoscope to delete.
    """
    try:
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
