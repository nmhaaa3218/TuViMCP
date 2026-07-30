# `get_van_han`

Calculates yearly transit stars and active houses (major, yearly, and monthly periods) for a target period.

## Purpose

Use this tool to perform predictive transit analysis (Vận Hạn) for a specific target timeframe.

## Calendar Prerequisites

**Critical:** `current_year`, `current_month`, and (if provided) `current_day` represent the **Lunar** year, month, and day. If inspecting a Solar timeframe (e.g. "October 2026"), you **must** convert it using `convert_calendar` first.

## Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `name` | string | required | Person's name |
| `day` | integer | required | Day of birth (1-31) |
| `month` | integer | required | Month of birth (1-12) |
| `year` | integer | required | Year of birth |
| `hour_val` | string | required | Hour (e.g. "14:30", "Ngọ") |
| `gender_val` | string | required | "Nam" or "Nữ" |
| `is_solar` | boolean | true | True for Solar, False for Lunar |
| `current_year` | integer | current year | Target Lunar year |
| `current_month` | integer | 1 | Target Lunar month (1-12) |
| `current_day` | integer | None | Target Lunar day (1-30, optional — enables Nhật Hạn) |

## Return Value

```json
{
  "person_details": {
    "name": "Nguyễn Văn A",
    "destiny_cuc": "Thổ ngũ Cục"
  },
  "target_period": {
    "current_year": 2026,
    "current_year_can_chi": "Bính Ngọ",
    "current_month_lunar": 5,
    "current_age": 32
  },
  "transit_stars": [
    {"name": "Lưu Thái Tuế", "cung_so": 7, "chi": "Ngọ"}
  ],
  "dai_han": {"cung_so": 10, "cung_chu": "Tử tức", "dai_han": 35},
  "tieu_han": {"cung_so": 7, "cung_chu": "Tật ách", "tieu_han": "Ngọ"}
}
```

See [examples/sample_van_han_output.json](https://github.com/nmhaaa3218/TuViMCP/blob/main/examples/sample_van_han_output.json) for the complete output.
