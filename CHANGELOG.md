# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-06-10

This is the initial release of the Tu Vi Horoscope MCP Server.

### Added
- **Horoscope Generation**: Convert Solar/Lunar birth details into full Tử Vi charts (Thiên Bàn and Địa Bàn with 12 houses and stars).
- **Vận Hạn (Transit Analysis)**: Support for calculation of transit stars and active Đại Hạn, Tiểu Hạn, and Nguyệt Hạn periods for a target year/month.
- **Local SQLite Persistence**: Save, retrieve, list, and delete horoscope records.
- **Flexible Hour Mapping**: Convert traditional branch names (e.g. "Ngọ", "Tý") and timestamp values to Earthly branch hours.
- **Multi-transport Support**: Runs on both standard I/O (Stdio mode for Claude/Cursor) and HTTP streamable protocol.
- **Automated Tests**: Unit testing suite using `pytest` covering calculations, parsing, and database logic.
- **CI Pipeline**: Integration of GitHub Actions testing on multiple Python versions.
- **Examples**: Included programmatic quick start scripts and actual JSON output templates under `examples/`.
