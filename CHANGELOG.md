# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - 2026-08-26

### Fixed
- **Vòng Tràng Sinh Swap (`Thai` & `Dưỡng`)**: Fixed inverted negative offset indexing in `_engine/App.py` where `saoThai` and `saoDuong` were swapped during counter-clockwise transit. Step 11 is now strictly `Thai` and step 12 is `Dưỡng` for both clockwise and counter-clockwise directions.
- **Star Name Normalization (`Văn Tinh`)**: Stripped misleading `LN.` prefix from fixed birth star `Văn tinh` in `_engine/Sao.py` to prevent confusion with transit stars.
- **Center Chart Metadata Rendering**: Formatted `Hành cục` display in `_rendering.py` to show element relationship `sinh_khac` (e.g. `Kim Tứ Cục (Cục khắc Mệnh)`) instead of raw internal integer IDs.

### Added
- **Astrological Verification Tests**: Added unit test suite `tests/test_vong_trang_sinh_and_thien_giai.py` verifying Vòng Tràng Sinh clockwise/counter-clockwise ordering, star naming, and Thiên Lương school compatibility.

---

## [0.4.1] - 2026-08-03

### Added
- **Bundled Unicode Font (`Roboto`)**: Packaged open-source `Roboto-Regular.ttf` & `Roboto-Bold.ttf` directly within `tuvi_mcp._fonts` and setuptools `package-data`. Guarantees crisp rendering and full Vietnamese diacritics support (`ệ`, `ỉ`, `ử`, `ơ`, `đ`, `ấ`, `ở`...) on headless and minimal serverless environments (Vercel, AWS Lambda, Docker Alpine/Slim).
- **Custom Font Overrides**: Extended `generate_laso_image` and `Horoscope.render_chart(...)` to accept optional `font_path` and `font_bold_path` parameters for custom typography.

### Fixed
- **Headless Font Degradation**: Fixed blurry/pixelated chart images, unscalable font sizes, and corrupted Vietnamese Unicode characters caused by `ImageFont.load_default()` fallback when desktop system fonts (`Arial`, `DejaVu`) are missing on headless serverless runtimes.

---

## [0.4.0] - 2026-07-30

### Added
- **Public library API** (Phase 1 of library refactor, `f40ba0c`): new typed, ergonomic surface for Python consumers.
  - `tuvi_mcp.Horoscope` — class with `from_birth(...)`, `.chart()`, `.transit()`, `.auspicious()`, `.render_chart()` methods.
  - `tuvi_mcp.BirthInfo` — frozen, validated dataclass for birth input.
  - `tuvi_mcp.Gender` / `Calendar` — strongly-typed enums.
  - `tuvi_mcp.HoroscopeResult`, `TransitResult`, `AuspiciousResult` — typed results with `.to_dict()` + dict-like access.
- **CLI/server split** (Phase 2 of library refactor, `4ffdd9d`): `__main__.py` owns the CLI entry point; `_server.py` owns the FastMCP definitions; `server.py` and `mcp_server.py` remain as backward-compatible shims.
- **Calculator split into private modules** (Phase 3 of library refactor, `362020b`): `tuvi_calculator.py` reduced from 785 lines to a 65-line shim that re-exports from `_calendar`, `_chart`, `_input`, `_transit`, `_auspicious`. Existing imports (`from tuvi_mcp.tuvi_calculator import …`) keep working unchanged.
- **Public-facing calendar module** (`tuvi_mcp/calendar.py`): stable, semantically-named re-export of `convert_solar_to_lunar`, `convert_lunar_to_solar`, and `validate_calendar_convert` from the internal `_calendar` and `_input` modules.
- **Server consolidation** (`dd8f914`): server implementation logic fully removed from `server.py`; FastMCP registration lives only in `_server.py`.
- **Sphinx + Furo documentation site** (`c3884bb`, `46c8433`): full API reference built with `myst-parser` and `sphinx-autodoc-typehints`. Published to https://tuvimcp.readthedocs.io/en/latest/. Pages: `api/horoscope`, `api/results`, `api/enums`, `api/database`, `tools/*`, plus Vietnamese-language `quickstart`/`contributing` summaries.
- **Timezone parameter on MCP tool surface** (`9b0206f`): every MCP tool (`generate_horoscope`, `get_van_han`, `get_auspicious_info`, `convert_calendar`) now accepts `timezone: int | str | None = None`. Accepts integer hour (`7`, `-5`) or `h:30` string (`"7:30"`, `"-5:30"`); other minute values and out-of-range inputs are rejected with `INVALID_INPUT_PARAMETER` + `suggestions`. Default remains 7 (ICT). The astronomical engine (`VnCalendarUtil`) was already timezone-parameterized — this change unblocks the previously hard-coded `7` literals in the chart math pipeline.
- **Timezone threading in chart math** (`9b0206f`): `build_raw_chart`, `adjust_date_for_late_ty`, `get_horoscope_chart`, `get_van_han_analysis` now accept and propagate `timezone`. The five hard-coded `7` literals in the chart pipeline (`_chart.py:63, 64, 82, 99, 104`) and the inner `canChiNgay(timeZone=7, …)` call in `_engine/AmDuong.py:322` have been replaced with the parameter.
- **Timezone in `_auspicious.py`** (`9b0206f`): `get_auspicious_details(timezone=…)` honors tz at the Solar↔Lunar date boundary via direct `VnCalendarUtil` calls; the OO `Solar`/`Lunar` lookup path remains tz=7-anchored for tiết-khí-table lookups (documented limitation; tiết-khí NAMES are timezone-independent).
- **Timezone in `Horoscope` public API** (`9b0206f`): `BirthInfo.timezone` is now propagated through `Horoscope.chart()`, `Horoscope.transit()`, and `Horoscope.auspicious(timezone=…)`. Library users who pass `timezone=8` to `from_birth(...)` now actually get a tz=8 chart, not the previous silent tz=7 default.
- **Database timezone persistence** (`4c7d93e`): added `timezone REAL NOT NULL DEFAULT 7.0` column to `horoscopes` table in `_storage.py` with automatic `ALTER TABLE` migration for existing SQLite databases, and updated `_enrich_with_cach_cuc` to pass the stored timezone during Cách Cục evaluation.

### Changed
- **Private module separation**: Internal implementation moved to underscore-prefixed modules:
  - `auspicious.py` → `_auspicious.py` (public shim re-exports only `get_auspicious_details`)
  - `server.py` → `_server.py` (public shim preserves backward compat for `mcp`, `generate_horoscope`, etc.)
  - `_compat/` now has `__init__.py` for proper package structure.
- **Library consistency** (Phases 1–3, `f40ba0c`, `362020b`): `transit()` and `auspicious()` now return typed dataclasses (`TransitResult`, `AuspiciousResult`) matching the pattern set by `chart()` (`HoroscopeResult`). All three support attribute access, `.to_dict()`, and dict-like `__getitem__`.
- **Public Horoscope API promoted in README + quickstart** (Phase 4, `6ee8610`): the `Horoscope.from_birth()` ergonomic surface is now the documented primary entry point for library consumers. Legacy function-style imports kept and demonstrated in `examples/quick_start.py` as a fallback.
- **Lunar calendar consolidation + ansaotuvi removal** (`760ee7c`): `_lunar_calendar/util/` directory restructured; deprecated `tuvi_mcp.ansaotuvi` engine files removed in favor of the Vietnamese `VnCalendarUtil` path.
- **Transit calculation optimization** (`4c7d93e`): `get_van_han_analysis` no longer redundantly rebuilds the chart twice via `build_raw_chart`; it now reuses birth lunar metadata directly from the `get_horoscope_chart` call result.
- **Timezone type annotations** (`9f6dae3`): standardized `timezone: float = 7.0` annotations across `validate_birth_parameters`, `validate_calendar_convert`, `convert_solar_to_lunar`, and `convert_lunar_to_solar` to cleanly allow half-hour offsets (e.g., 5.5 for IST).
- **Style cleanup** (`b4ecee5`): ruff issues cleaned up across all new modules introduced by Phases 1–4.

### Fixed
- **`convert_calendar` MCP tool validation** — MCP tool now correctly passes `from_solar` and `lunar_leap` parameters to `validate_calendar_convert` so Lunar→Solar conversions undergo lunar date existence checking.
- **`BirthInfo.parse_hour`** — now delegates to `_coerce_hour` instead of maintaining duplicate conversion logic.
- **Hour validation** — `_coerce_hour` raises `ValueError` for values > 23 (previously silently wrapped via `% 24`).
- **Chart error handling** — `chart()` raises `ValueError` on validation failure instead of returning an empty `HoroscopeResult` wrapping an error dict.
- **`__getitem__` raises `KeyError`** (not `AttributeError`) for missing keys — correct dict-like behavior.

### Tests
- **17 new tests** in `tests/test_library_api.py` covering the new typed `Horoscope` API, `BirthInfo` validation, and the `to_dict` / `__getitem__` result surfaces.
- **28 new tests** in `tests/test_mcp_timezone.py` covering `coerce_timezone` validation (int / `h:30` string / hard-error cases), default-unchanged behavior at tz=7, Tết 1968 / Tết 1985 / Tết 2007 / Tết 2026 boundary divergence between tz=7 and tz=8, late-Tý hour-23 rolling under tz=8, and cross-validation against online-published Vietnamese/Chinese calendar data.
- **2 new tests** in `tests/test_library_api.py` confirming `Horoscope.chart()` honors `BirthInfo.timezone` and `Horoscope.auspicious(timezone=…)` overrides at the boundary date.

### Notes
- All existing imports (`from tuvi_mcp import tuvi_calculator`, `from tuvi_mcp.server import mcp`, `from tuvi_mcp.auspicious_calculator import get_auspicious_details`, etc.) continue to work unchanged. The new API is purely additive.
- Library users who already passed `timezone=8` to `Horoscope.from_birth(...)` previously got a tz=7 chart silently. After this release, that input is honored end-to-end through the chart math pipeline.
- Vietnamese Tử Vi community consensus (per lyso.vn masters) is that the local civil time at the birthplace is the canonical input — not a converted UTC instant. The `timezone` parameter here represents that civil timezone used for boundary-rounding of astronomical events (lunar day, tiết-khí, Đông chí), not a UTC conversion. Civil hour branch (chi giờ) is always derived from the user-supplied local clock time.

---

## [0.3.1] - 2026-07-28

### Added
- **Nhật Hạn (daily transit) support**: `get_van_han_analysis` and the `get_van_han` MCP tool now accept an optional `current_day` parameter (1-30). When provided, the result includes a `nhat_han` entry identifying the active daily cycle cung, derived clockwise from the active Nguyệt Hạn cung. Day 1 collapses to Nguyệt Hạn; day 13 wraps back to it. (ee49ea2)
- **Daily transit input validation**: `current_day` is now rejected with `INVALID_INPUT_PARAMETER` if it falls outside 1-30, matching the upper bound of a lunar month. (ee49ea2)
- **Regression tests** for Nhật Hạn — null without `current_day`, equivalence with Nguyệt Hạn on day 1, clockwise progression on day 2, wrap-around at day 13, off-by-one at day 12, and validation errors at day 0 and 31. (ee49ea2)

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
