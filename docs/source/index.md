# TuViMCP

A Model Context Protocol (MCP) server for Vietnamese **Tử Vi** horoscope calculation and management.

```{toctree}
:caption: Getting Started
:maxdepth: 1

installation
quickstart
```

```{toctree}
:caption: MCP Tools
:maxdepth: 1

tools/generate_horoscope
tools/get_van_han
tools/convert_calendar
tools/get_auspicious_info
```

```{toctree}
:caption: Python Library API
:maxdepth: 1

api/tuvi_mcp
api/horoscope
api/results
api/enums
api/database
```

```{toctree}
:caption: Reference
:maxdepth: 1

changelog
contributing
```

## Features

- **Horoscope Generation** — Convert Solar or Lunar birth dates into a full Tử Vi chart (Thiên Bàn and Địa Bàn with 12 houses and 100+ stars).
- **51 Cách Cục Evaluation** — Automatically recognizes all 51 traditional astrological formations (Trung Châu Phái) with poems, commentary, and pros/cons.
- **Image Rendering** — Generates beautiful, print-ready chart images with element-based colored text and geometric connecting lines.
- **Vận Hạn (Transit Analysis)** — Computes transit stars (Lưu tinh) and maps Đại Hạn, Tiểu Hạn, Nguyệt Hạn, and Nhật Hạn for any target year/month/day.
- **Auspicious Date & Time Checker** — Evaluates Hoàng Đạo/Hắc Đạo, 12 Trực, 28 Tú, Tiết Khí, travel directions, and auspicious hours.
- **Local Persistence** — Built-in SQLite database for saving, retrieving, listing, and deleting horoscope profiles.
- **Typed Python API** — `Horoscope`, `BirthInfo`, `TransitResult`, and `AuspiciousResult` with `.to_dict()` and dict-like access.

## Quick Links

- [Installation](installation.md)
- [Python Library API](api/tuvi_mcp)
- [GitHub Repository](https://github.com/nmhaaa3218/TuViMCP)
- [PyPI Package](https://pypi.org/project/tuvi-mcp-server/)
- [Changelog](changelog.md)
