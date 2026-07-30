# `get_auspicious_info`

Evaluates auspicious days, hours, 12 Trực, 28 Tú, Tiết Khí, and travel directions for a given date.

## Purpose

Use this tool to check good/bad days for weddings, store openings, construction, travel, or any activity requiring auspicious timing. Use `generate_horoscope` for a full birth chart instead.

## Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `day` | integer | today | Day of month |
| `month` | integer | current | Month of year |
| `year` | integer | current | Year |
| `is_solar` | boolean | true | True for Solar, False for Lunar |

## Return Value

| Key | Description |
|---|---|
| `duong_lich` | Solar date string |
| `am_lich` | Lunar date string |
| `can_chi_ngay` | Day's Can-Chi pillar |
| `ngay_hoang_dao` | Hoàng Đạo / Hắc Đạo evaluation |
| `truc_ngay` | Day's Trực (12 Trực) |
| `nhi_thap_bat_tu` | Day's Tú (28 Tú) |
| `huong_xuat_hanh` | Auspicious travel directions |
| `gio_hoang_dao` | Auspicious hours |
| `tiet_khi_hien_tai` | Current solar term (Tiết Khí) |
| `tiet_khi_tiep_theo` | Next solar term |
