#!/usr/bin/env python3
import json
import os

# Import tuvi_calculator (Ensure project is installed or in python path)
try:
    from tuvi_mcp import tuvi_calculator
except ImportError:
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from tuvi_mcp import tuvi_calculator


def main():
    print("--------------------------------------------------")
    print("TuViMCP Quick Start & Sample Generator")
    print("--------------------------------------------------")

    # Sample Birth Details: June 10, 1995 at 14:30 (Solar, Male)
    name = "Nguyễn Văn A"
    day = 10
    month = 6
    year = 1995
    hour_val = "14:30"
    gender_val = "Nam"
    is_solar = True

    print(f"Generating horoscope for {name} ({day}/{month}/{year} {hour_val} {gender_val})...")
    chart = tuvi_calculator.get_horoscope_chart(
        name=name, day=day, month=month, year=year, hour_val=hour_val, gender_val=gender_val, is_solar=is_solar
    )

    # 1. Save horoscope chart example
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(examples_dir, exist_ok=True)

    chart_output_path = os.path.join(examples_dir, "sample_horoscope_output.json")
    with open(chart_output_path, "w", encoding="utf-8") as f:
        json.dump(chart, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved horoscope JSON output to: {chart_output_path}")

    # 2. Save transit analysis (Vận Hạn) example for year 2026, month 5
    current_year = 2026
    current_month = 5
    print(f"Generating Vận Hạn transit analysis for the year {current_year}, month {current_month}...")
    van_han = tuvi_calculator.get_van_han_analysis(
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

    van_han_output_path = os.path.join(examples_dir, "sample_van_han_output.json")
    with open(van_han_output_path, "w", encoding="utf-8") as f:
        json.dump(van_han, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved Vận Hạn JSON output to: {van_han_output_path}")

    print("\nSummary of Horoscope Thien Ban:")
    tb = chart["thien_ban"]
    for k, v in tb.items():
        print(f"  - {k}: {v}")

    print("\nSuccessfully generated example files.")


if __name__ == "__main__":
    main()
