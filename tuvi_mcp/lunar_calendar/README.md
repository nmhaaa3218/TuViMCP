# `tuvi_mcp.lunar_calendar` — Vietnamese-only scope

This package is the calendar core of the Vietnamese TuVi MCP server. Starting
with **v1.4.9**, the surface is intentionally restricted to native Vietnamese
content: official holidays, widely-recognized folk practices, Vietnamese
Buddhist observances, and Vietnamese calendar mechanics. Pure Chinese /
Japanese almanac and religion systems have been removed from the default
surface and relocated (EightChar) or deleted (Tao / Foto / Lục Diệu / Peng
Zu / HolidayUtil).

## Quick orientation

| Want... | Import from |
|---|---|
| Convert solar ↔ lunar | `tuvi_mcp.lunar_calendar.{Solar, Lunar, VnCalendarUtil}` |
| Vietnamese holidays + folk rituals | `tuvi_mcp.lunar_calendar.{VnHolidayRegistry, VietnameseHoliday}` |
| Full snapshot of a date | `lunar.get_full_info()` → `lunar_types.LunarInfo` |
| 12 Trực / 28 Tú / Hoàng-Hắc Đạo | methods on `Lunar` (`getZhiXing`, `getXiu`, `getDayTianShen*`, `getDayPosition*Desc`) |
| Tứ Trụ / Bát Tự (Sino-VN huyền học, opt-in) | `tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc.EightChar` |
| Tử Vi chart computation | `tuvi_mcp.tuvi_calculator` |

## Vietnamese-only scope

Default `lunar_calendar` exports are now:

```
Solar, Lunar, LunarYear, LunarMonth, LunarTime,
SolarWeek, SolarMonth, SolarSeason, SolarHalfYear, SolarYear,
SolarHalfYear, SolarSeason,
JieQi, NineStar,
Holiday, VietnameseHoliday, VnHolidayRegistry, HolidayEntry,
util.VnCalendarUtil
```

Removed from default surface (v1.4.9):

- `Tao`, `TaoFestival`, `util/TaoUtil.py` — pure Chinese Đạo giáo
- `Foto`, `FotoFestival`, `util/FotoUtil.py` — pure Chinese Phật giáo (Chinese roster, NOT GHPGVN)
- `ShuJiu` — Chinese 九九 winter-counting
- `Fu` — Chinese 三伏 summer-counting
- `util/HolidayUtil.py` — PRC statutory schedule mislabeled Vietnamese
- `LunarUtil.LIU_YAO` / `Lunar.getLiuYao()` — Japanese/Chinese 六曜
- `LunarUtil.PENG_ZU_GAN/ZHI` / `Lunar.getPengZu*()` — Chinese almanac taboos
- `SolarUtil.XING_ZUO` — Western zodiac
- `SolarUtil.WEEK_FESTIVAL["11-4-4"]` — US Thanksgiving

All of these are *gone* from disk. There is no opt-in path.

## Opt-in: Sino-VN huyền học

The Tứ Trụ / Bát Tự system is widely practiced in Vietnam by phong thủy
masters as a supplement to Tử Vi. Its theoretical foundation is Chinese Đông Á
metaphysics, not native Vietnamese folk religion (tín ngưỡng dân gian). It is
exposed only via an explicit subpackage:

```python
from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar
```

Do not confuse "Tứ Trụ" (四柱, four pillars of destiny) with "Tứ Bất Tử"
(四不死, the four Vietnamese folk immortals). They are unrelated terms.

## Holiday registry

`VnHolidayRegistry` (`vn_holidays.py`) is the single source of truth. Each
entry carries a `scope` tag:

| Scope | Default? | Examples |
|---|---|---|
| `official` | ✓ | Tết Dương lịch, 30/4, 1/5, 9/2, Giỗ Tổ Hùng Vương |
| `folk` | ✓ | Tết Nguyên Đán, Khai Hạ, Đoan Ngọ, Trung Thu, Ông Táo |
| `buddhist_vn` | ✓ | Phật Đản (4/15), Vu Lan (7/15) |
| `imported` | ✗ opt-in | Hàn Thực, Thất Tịch, Trùng Cửu, Ngọc Hoàng, Thượng/Hạ Nguyên |
| `international` | ✓ | 8/3, 1/6, 20/10, 20/11 |

```python
from tuvi_mcp.lunar_calendar import VnHolidayRegistry

VnHolidayRegistry.get_lunar(7, 15)                   # "Vu Lan báo hiếu (Rằm tháng Bảy)"
VnHolidayRegistry.get_lunar(7, 7, with_imported=True)  # "Lễ Thất Tịch"
VnHolidayRegistry.get_lunar(7, 7)                   # None — hidden in default scope
```

### Statutory day-off schedule: out of scope

The legacy `HolidayUtil` (PRC statutory schedule with Vietnamese labels) has
been removed. The Vietnamese-government statutory day-off schedule (compensatory
days, weekend swaps, etc.) is intentionally not implemented here. A future
contribution should encode the official Vietnamese government decision text,
not translate from any Chinese source.

## Reference-pattern adoption (library-only)

The following ergonomic helpers were added (mirroring `pyvnlunar` but adapted
for the Vietnamese-only scope). They are library-only — not exposed via MCP
tool surface.

```python
from tuvi_mcp.lunar_calendar import Lunar, Solar

lunar = Solar.fromYmd(2026, 6, 14).getLunar()

lunar.get_full_info()                 # typed LunarInfo dataclass
lunar.check_age_conflict(1990)        # list of conflicting ages (tuổi xung)
lunar.get_travel_direction()          # auspicious travel direction (Hỷ Thần)
lunar.check_travel_hour(7)            # "Hoàng Đạo" / "Hắc Đạo" for 7h
Lunar.find_good_days((1, 6, 2026), (30, 6, 2026))  # Hoàng Đạo days in range
```

## Migration notes

### From `HolidayUtil`

The class is gone. If you only need holiday NAMES (not day-off schedules),
`VnHolidayRegistry` is the replacement. If you need day-off schedules, that
is an open project.

### From `Foto`, `Tao`, `ShuJiu`, `Fu`

These are gone entirely. The deleted methods on `Lunar` (`getFoto`,
`getTao`, `getShuJiu`, `getFu`) raised `AttributeError` on call; v1.4.9
removes them. Any code that called them must be updated.

### From `Lunar.getLiuYao()` / `Lunar.getPengZu*()`

These now return `None` (or are removed). Use Vietnamese equivalents:
Hoàng Đạo / Hắc Đạo, 12 Trực, 28 Tú.

### From `EightChar` direct import

The class still exists; the import path changed:

```python
# OLD
from tuvi_mcp.lunar_calendar import EightChar

# NEW
from tuvi_mcp.lunar_calendar.sino_vn_huyen_hoc import EightChar
```

## Testing

```
pytest tests/test_native_only.py
pytest tests/test_vn_holidays.py
pytest tests/test_roundtrip_and_ref_patterns.py
pytest tests/test_eightchar_relabel.py
```

`test_native_only.py` is a structural guard: it scans the default surface for
known Chinese / foreign terms (`三元`, `五腊`, `六曜`, etc.) and fails if any
appear in executable code (comments / docstrings are tolerated for migration
notes).