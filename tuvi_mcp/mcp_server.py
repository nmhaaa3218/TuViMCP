#!/usr/bin/env python3
import os
import sys
import json
import argparse
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from . import database
from . import tuvi_calculator

mcp = FastMCP("TuViMCP")

@mcp.tool()
def generate_horoscope(
    name: str = "Khách",
    day: int = 1,
    month: int = 1,
    year: int = 1990,
    hour_val: str = "12:00",
    gender_val: str = "Nam",
    is_solar: bool = True
) -> str:
    """
    Generate a full Tu Vi (Vietnamese horoscope) chart in JSON format.
    
    Args:
        name: Name of the person.
        day: Day of birth (1-31).
        month: Month of birth (1-12).
        year: Year of birth (e.g. 1990).
        hour_val: Hour of birth (e.g. "14:30", "Ngọ", "Tý", or index 1-12 where 1=Tý, 12=Hợi).
        gender_val: Gender ("Nam", "Nữ", "male", "female").
        is_solar: True if birth date is Solar (Dương lịch), False if Lunar (Âm lịch).
    """
    try:
        chart = tuvi_calculator.get_horoscope_chart(
            name=name,
            day=day,
            month=month,
            year=year,
            hour_val=hour_val,
            gender_val=gender_val,
            is_solar=is_solar
        )
        return json.dumps(chart, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

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
    current_month: int = 1
) -> str:
    """
    Calculate transit stars (sao lưu) and active houses (Đại Hạn, Tiểu Hạn, Nguyệt Hạn) 
    for the current month/year to inspect luck and predictions (vận hạn).
    
    Args:
        name: Name of the person.
        day: Day of birth (1-31).
        month: Month of birth (1-12).
        year: Year of birth.
        hour_val: Hour of birth (e.g. "14:30", "Ngọ").
        gender_val: Gender ("Nam" or "Nữ").
        is_solar: True if birth date is Solar (Dương lịch), False if Lunar (Âm lịch).
        current_year: Year to inspect (defaults to current year, e.g. 2026).
        current_month: Lunar month to inspect (1-12, default 1).
    """
    try:
        if current_year is None:
            current_year = datetime.now().year
            
        analysis = tuvi_calculator.get_van_han_analysis(
            name=name,
            day=day,
            month=month,
            year=year,
            hour_val=hour_val,
            gender_val=gender_val,
            is_solar=is_solar,
            current_year=current_year,
            current_month=current_month
        )
        return json.dumps(analysis, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def save_horoscope(
    name: str,
    day: int,
    month: int,
    year: int,
    hour_val: str,
    gender_val: str,
    is_solar: bool = True,
    notes: str = None
) -> str:
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
            name=name,
            day=day,
            month=month,
            year=year,
            hour=hour,
            gender=gender_str,
            is_solar=is_solar,
            notes=notes
        )
        return json.dumps({
            "message": f"Successfully saved horoscope for '{name}' with ID {record_id}.",
            "id": record_id
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def list_saved_horoscopes() -> str:
    """
    Retrieve all saved horoscopes from the local database.
    """
    try:
        records = database.list_saved_horoscopes()
        return json.dumps(records, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_saved_horoscope(horoscope_id: int = None, name: str = None) -> str:
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
            return json.dumps({"error": "Horoscope record not found"}, ensure_ascii=False)
            
        chart = tuvi_calculator.get_horoscope_chart(
            name=record["name"],
            day=record["day"],
            month=record["month"],
            year=record["year"],
            hour_val=record["hour"],
            gender_val=record["gender"],
            is_solar=bool(record["is_solar"])
        )
        # Include database metadata
        chart["metadata"] = {
            "id": record["id"],
            "notes": record["notes"],
            "created_at": record["created_at"]
        }
        return json.dumps(chart, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def delete_saved_horoscope(horoscope_id: int) -> str:
    """
    Delete a saved horoscope record from the database.
    
    Args:
        horoscope_id: The database ID of the horoscope to delete.
    """
    try:
        success = database.delete_saved_horoscope_by_id(horoscope_id)
        if success:
            return json.dumps({"message": f"Successfully deleted horoscope ID {horoscope_id}."}, ensure_ascii=False)
        else:
            return json.dumps({"error": f"No horoscope record found with ID {horoscope_id}."}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

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
