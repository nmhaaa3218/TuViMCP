#!/usr/bin/env python3
"""
Quick-start examples for the tuvi-mcp-server library.

Run from the project root:
    .venv/bin/python examples/quick_start.py

Demonstrates both the new typed ``Horoscope`` API and the legacy
function-style imports for backward compatibility.
"""

import json
import os

# Import from the public top-level API (new style, recommended).
from tuvi_mcp import Horoscope

# ---- Example 1: New typed API ----
print("=" * 50)
print("Example 1: New typed Horoscope API")
print("=" * 50)

h = Horoscope.from_birth(
    name="Nguyễn Văn A",
    year=1995, month=6, day=10,
    hour="14:30",
    gender="Nam",
    calendar="solar",
)

chart = h.chart()
print(f"Subject: {chart.thien_ban['ten']}")
print(f"  Birth year: {chart.thien_ban['can_nam']} {chart.thien_ban['chi_nam']}")
print(f"  Destiny: {chart.thien_ban['ten_cuc']} ({chart.thien_ban['hanh_cuc']})")
print(f"  Houses: {len(chart.dia_ban)}")
print(f"  Matched cách cục: {len(chart.cach_cuc)}")

# Transit / Vận Hạn analysis
print("\nVận Hạn for Lunar 2026, month 5, day 15:")
van_han = h.transit(year=2026, month=5, day=15)
print(f"  Year: {van_han['target_period']['current_year_can_chi']}")
print(f"  Age: {van_han['target_period']['current_age']}")
print(f"  Đại Hạn cung: {van_han['dai_han']['cung_chu']}")
print(f"  Tiểu Hạn cung: {van_han['tieu_han']['cung_chu']}")
print(f"  Nguyệt Hạn cung: {van_han['nguyet_han']['cung_chu']}")
print(f"  Nhật Hạn cung: {van_han['nhat_han']['cung_chu']}")

# Auspicious day evaluation
print("\nAuspicious evaluation for 27/07/2026:")
auspicious = h.auspicious(day=27, month=7, year=2026)
print(f"  Hoàng Đạo: {auspicious['ngay_hoang_dao']['ten_sao']}")
print(f"  Trực: {auspicious['truc_ngay']['ten']}")
print(f"  28 Tú: {auspicious['nhi_thap_bat_tu']['ten']}")

# ---- Example 2: Save sample JSON outputs (legacy function API) ----
print("\n" + "=" * 50)
print("Example 2: Legacy function API (for backward-compat demo)")
print("=" * 50)

try:
    from tuvi_mcp import tuvi_calculator

    chart_dict = tuvi_calculator.get_horoscope_chart(
        name="Nguyễn Văn A",
        day=10, month=6, year=1995,
        hour_val="14:30", gender_val="Nam", is_solar=True,
    )

    examples_dir = os.path.dirname(os.path.abspath(__file__))
    chart_output_path = os.path.join(examples_dir, "sample_horoscope_output.json")
    with open(chart_output_path, "w", encoding="utf-8") as f:
        json.dump(chart_dict, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved horoscope JSON: {chart_output_path}")

    van_han_dict = tuvi_calculator.get_van_han_analysis(
        name="Nguyễn Văn A",
        day=10, month=6, year=1995,
        hour_val="14:30", gender_val="Nam", is_solar=True,
        current_year=2026, current_month=5,
    )
    van_han_output_path = os.path.join(examples_dir, "sample_van_han_output.json")
    with open(van_han_output_path, "w", encoding="utf-8") as f:
        json.dump(van_han_dict, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved Vận Hạn JSON: {van_han_output_path}")
except ImportError:
    print("(Legacy function API not available — skipping sample output generation.)")

print("\nDone.")