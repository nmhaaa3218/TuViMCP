# `convert_calendar`

Converts a date between Solar (Dương lịch) and Lunar (Âm lịch) calendars.

## Purpose

Translate dates back and forth. Crucial for converting Solar target timeframes to Lunar periods before calling `get_van_han`.

## Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `day` | integer | required | Day to convert |
| `month` | integer | required | Month to convert |
| `year` | integer | required | Year to convert |
| `from_solar` | boolean | true | True: Solar→Lunar. False: Lunar→Solar |
| `lunar_leap` | boolean | false | Only used if `from_solar` is False; True if input lunar month is leap |
| `timezone` | integer | 7 | Timezone offset (default: Vietnam/ICT) |

## Return Value

```json
{
  "day": 13,
  "month": 5,
  "year": 1995,
  "leap": false
}
```

On error: `{"error": "message"}`
