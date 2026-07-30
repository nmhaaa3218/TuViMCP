# `generate_horoscope`

Generates a full Tử Vi chart from raw birth details, with optional high-quality chart image rendering.

## Purpose

Use this tool to compute and inspect an astrological birth chart from scratch for arbitrary birth details.

## Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `name` | string | "Khách" | Person's name |
| `day` | integer | required | Day of birth (1-31) |
| `month` | integer | required | Month of birth (1-12) |
| `year` | integer | required | Year of birth |
| `hour_val` | string | required | Hour (e.g. "14:30", "Ngọ", "Tý", or branch index 1-12) |
| `gender_val` | string | required | "Nam" or "Nữ" (case-insensitive) |
| `is_solar` | boolean | true | True for Solar, False for Lunar |
| `current_year` | integer | current year | Transit star year |
| `generate_image` | boolean | true | Whether to render chart as PNG |

## Return Value

If `generate_image` is `True`:
- Returns `[Image, chart_data]` — Image is a FastMCP image content block pointing to the rendered PNG.

If `generate_image` is `False`:
- Returns raw JSON with keys:
  - `thien_ban` — demographics, natal pillars, element, destiny
  - `dia_ban` — 12 houses with stars
  - `cach_cuc` — recognized astrological formations (with `id`, `name`, `category`, `description`, `reason`, `co_ca`, `binh_chu`, `uu_khuyet_diem`)

On error: `{"error": "message"}`

## Example

```json
{
  "thien_ban": {
    "ten": "Nguyễn Văn A",
    "gioi_tinh": "Nam",
    "ngay_duong": "10/6/1995",
    "ngay_am": "13/5/1995",
    "gio_sinh": "Đinh Mùi",
    "hanh_cuc": 5,
    "ten_cuc": "Thổ ngũ Cục",
    "menh_chu": "Cự môn",
    "than_chu": "Thiên cơ",
    "ban_menh": "SƠN ÐẦU HỎA"
  },
  "cach_cuc": [
    {"id": 5, "name": "Đan Trì Quế Trì Cách", "category": "Cát Cục"}
  ],
  "dia_ban": [
    {
      "cung_so": 1,
      "cung_ten": "Mậu Tý",
      "hanh_cung": "Thủy",
      "cung_chu": "Phụ mẫu",
      "sao": [{"id": 9, "name": "Tham lang", "attribute": "Hãm địa"}]
    }
  ]
}
```

See [examples/sample_horoscope_output.json](https://github.com/nmhaaa3218/TuViMCP/blob/main/examples/sample_horoscope_output.json) for the complete output.
