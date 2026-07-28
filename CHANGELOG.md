# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2026-07-28

### Fixed
- **Lục Hợp mapping corrected**: `get_luc_hop_cung` now uses canonical pairs (Tý-Sửu, Dần-Hợi, Mão-Tuất, Thìn-Dậu, Tỵ-Thân, Ngọ-Mùi) instead of an unrelated mapping, enabling rule 51 (Khoa Minh Lộc Ám Cách) to evaluate correctly. (92c4b43)
- **`has_star` attribute filter**: Fixed dead-code in the `star_attr` path where an unconditional `return True` after the attribute check made the filter non-functional. (85f79a5)
- **Case-insensitive `cung_chu` lookup**: `get_cung_by_chu` now lowercases both sides of the comparison. The chart serializer emits mixed casing (`Quan lộc` / `Tài bạch` / `Điền trạch`) while rule conditions use canonical capitalization (`Quan Lộc` / `Tài Bạch` / `Điền Trạch`). Previously rules 18 (Minh Châu Xuất Hải) and 48 (Nhật Nguyệt Chiếu Bích) silently never matched. (b7b1dd6)
- **Cách Cục 51 stub fields filled**: Rule 51 (Khoa Minh Lộc Ám Cách) shipped with empty `description` and `reason` fields; now derived from its existing `binh_chu` text. (b7b1dd6)
- **CI dependency upper bound**: `mcp` v2.0.0 removed `mcp.server.fastmcp` (`FastMCP` lives in `mcp.server.mcpserver` in v2). The previously unbounded `mcp>=1.27.2` resolved to 2.0.0 on CI, breaking all 4 tests that import from `mcp_server.py`. Pinned to `mcp>=1.27.2,<2.0.0`. (cfd7087)

### Refactored
- **Eager JSON load**: The 51-Cách-Cục rule dataset (`cach_cuc.json`) is now loaded at module import time instead of on the first `evaluate_cach_cuc` call. Removes the mutable `_CACH_CUC_DATA` global and eliminates a race condition under concurrent requests. (b7b1dd6)
- **Tam Phương condition dispatch collapsed**: 7 near-identical `if "tam_phuong_*" in cond` blocks replaced with a single dispatch loop over the canonical key set. (b7b1dd6)
- **Database enrichment for saved horoscopes**: `get_saved_horoscope_by_id` and `get_saved_horoscope_by_name` now attach an evaluated `cach_cuc` list to the returned dict. (b7b1dd6)
- **MCP server made stateless**: Removed database dependency and the `save_horoscope`/`get_saved_horoscope`/`delete_saved_horoscope` MCP tools. The server no longer requires SQLite for operation. (3c866f8)
- **Lunar calendar localized to Vietnamese**: Complete replacement of Chinese-based calendar modules with `VnCalendarUtil` containing the official Vietnamese algorithm. (0a2b4a4, 5d24e2a, 44106d3)
- **Auspicious calculator extracted**: `get_auspicious_details` separated into its own module with eight-character and auspicious calculation logic. (281b86e)

### Added
- **Comprehensive coverage suite**: 63 new tests across 6 phases — negative star-name matching, dataset integrity, condition-key synthetic matrix, real-chart smoke pins for all 51 rules, 200-chart property fuzz, and MCP surface end-to-end. (cfd7087)
- **Regression tests** for Solar.next and calendar conversion engine boundaries. (0a2b4a4)
- **Holiday registry and Vietnamese astronomical term tracking** in VnCalendarUtil. (34e0b6b)

## [0.2.0] - 2026-07-22

### Added
- **51 Cách Cục Evaluation Engine**: Added automatic pattern recognition for all 51 traditional astrological formations (**51 Cách Cục Trung Châu Phái**) directly integrated into chart generation APIs (`generate_horoscope` and `get_saved_horoscope`).
- **Data-Driven Rules Dataset (`tuvi_mcp/data/cach_cuc.json`)**: Extracted and structured complete metadata, poems (**Cổ Ca**), Vương Đình Chi commentary (**Bình Chú**), Pros & Cons (**Ưu/Khuyết điểm**), and declarative evaluation conditions for all 51 cách cục.
- **Exact Star Name Matching**: Implemented exact normalized string matching in `cach_cuc_evaluator.py` to ensure zero false-positive partial matches.
- **Comprehensive Test Suite**: Added dedicated unit tests validating cách cục evaluation schemas, specific pattern matches (e.g. Thạch Trung Ẩn Ngọc), and malformed input handling.

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
