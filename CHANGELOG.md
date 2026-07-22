# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.9] - 2026-07-22

### Added
- **Comprehensive Input Validation Layer**: Added entry-point validation (`validate_birth_parameters`, `validate_transit_period`, `validate_calendar_convert`) across all MCP tools to validate birth parameters, transit periods, calendar conversion parameters, and database keys.
- **Actionable Error Feedback**: Returns structured error responses (`INVALID_INPUT_PARAMETER`, `MISSING_REQUIRED_PARAMETER`) containing explicit error details and actionable field suggestions.
- **Unreal Date & Leap Year Validation**: Dynamically detects non-existent dates (such as February 31 or 31 April) and returns exact maximum days per month (`calendar.monthrange`), handling leap vs non-leap years.

## [0.1.8] - 2026-07-15

### Added
- **Late Tý Hour Alignment (Dạ Tý)**: Rolled calculation date forward by +1 day for births occurring between 23:00 and 23:59, ensuring correct Lunar day and hourly pillars, while keeping the original solar birth date in metadata display.
- **Hourly Pillar Resolution Fix**: Corrected a bug in `ThienBan.py` where the hourly pillar (`can_gio_sinh`) was resolved using Lunar day numbers directly as Solar parameters.
- **Robust Test Coverage**: Added comprehensive test cases for late Tý hour alignments, including verification that branch-based inputs do not trigger shifting.

## [0.1.7] - 2026-06-30

### Changed
- **Comprehensive Tool Documentation**: Rewrote docstrings for all exposed MCP server tools to address system judgment checklist guidelines. Added explicit details for:
  - Local side effects (database writes, image file generation).
  - Prerequisites and error handling pathways.
  - Parameter relationships, precedence, and validation rules.
  - Sibling comparisons to help LLM agents select the correct tool.
  - Code compliance with line length boundaries (<120 characters) and updated linters.

## [0.1.6] - 2026-06-28

### Added
- **Calendar Converter Tool (`convert_calendar`)**: Expose date conversion functionality as a dedicated tool to convert between Solar (Dương lịch) and Lunar (Âm lịch) calendars.
- **Agent Instructions**: Augmented both `convert_calendar` and `get_van_han` docstrings with explicit warnings instructing agents to convert solar dates to lunar dates prior to performing Tu Vi transit analyses.
- **Robust Leap Month Verification**: Enhanced lunar-to-solar conversions with strict error check parameters verifying whether the requested leap month configuration actually exists within the target year.
- **Test Suite Enhancements**: Expanded unit tests to validate bidirectional calendar conversions and verify leap month configuration errors.

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
