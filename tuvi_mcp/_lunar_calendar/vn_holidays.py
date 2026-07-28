# -*- coding: utf-8 -*-
"""
vn_holidays - Vietnamese Holiday & Cultural-Ritual Registry

Single source of truth for Vietnamese holidays, with explicit `scope` metadata
to distinguish official statutory days from folk practice from imported
Chinese-derived observances. Default lookup (`default=True`) returns only
`official`, `folk`, and `buddhist_vn` entries. Imported/regional entries are
accessible via `with_imported=True`.

The previous `VietnameseHoliday` module (with no scope metadata) is preserved
as a thin shim for backwards compatibility and routes through this registry.

Scope taxonomy:
    - "official":        Vietnamese statutory holiday (government decree).
    - "folk":             Widely recognized folk tradition across VN.
    - "buddhist_vn":      Vietnamese Mahayana Buddhist observance (GHPGVN
                          calendar). NOT a Chinese-Taoist festival.
    - "imported":         Chinese / Sino origin, included for opt-in only;
                          NOT part of native VN folk religion.
    - "international":    International civil observance recognized in VN.

TODO: official statutory day-off schedule (compensatory days, weekend swaps)
is intentionally out of scope. The legacy `HolidayUtil` (PRC schedule
disguised with Vietnamese labels) was removed in v1.4.9. Replace with a
Vietnamese government-schedule data source when needed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

HolidayScope = Literal["official", "folk", "buddhist_vn", "imported", "international"]

DEFAULT_SCOPES: tuple[HolidayScope, ...] = ("official", "folk", "buddhist_vn")


@dataclass(frozen=True)
class HolidayEntry:
    name: str
    scope: HolidayScope
    lunar: tuple[int, int] | None = None
    solar: tuple[int, int] | None = None
    notes: str = ""


_LUNAR: tuple[HolidayEntry, ...] = (
    HolidayEntry("Tết Nguyên Đán (Mùng 1 Tết)", "folk", lunar=(1, 1)),
    HolidayEntry("Mùng 2 Tết Nguyên Đán", "folk", lunar=(1, 2)),
    HolidayEntry("Mùng 3 Tết Nguyên Đán", "folk", lunar=(1, 3)),
    HolidayEntry("Lễ Khai Hạ (Hạ Cây Nêu)", "folk", lunar=(1, 7)),
    HolidayEntry("Ngày Vía Thần Tài đầu năm", "folk", lunar=(1, 10)),
    HolidayEntry("Giỗ Tổ Hùng Vương", "official", lunar=(3, 10),
                 notes="10/3 âm lịch; chính thức theo Quốc lệnh; lịch nghỉ theo lịch dương."),
    HolidayEntry("Lễ Phật Đản (Rằm tháng Tư)", "buddhist_vn", lunar=(4, 15),
                 notes="GHPGVN công nhận 15/4 âm lịch. KHÔNG dùng 4/8 (lịch Phật Đản Trung Hoa)."),
    HolidayEntry("Tết Đoan Ngọ (Tết Diệt sâu bọ)", "folk", lunar=(5, 5)),
    HolidayEntry("Vu Lan báo hiếu (Rằm tháng Bảy)", "buddhist_vn", lunar=(7, 15),
                 notes="Vu Lan bản địa Việt Nam; không gộp với Trung Nguyên Đạo giáo."),
    HolidayEntry("Tết Trung Thu (Rằm tháng Tám)", "folk", lunar=(8, 15)),
    HolidayEntry("Tết Trùng Thập (Tết Mới / Tết Thầy Thuốc)", "folk", lunar=(10, 10)),
    HolidayEntry("Ngày Ông Táo chầu trời (Tết Ông Công Ông Táo)", "folk", lunar=(12, 23)),
    HolidayEntry("Ngày Vía Ngọc Hoàng Thượng Đế", "imported", lunar=(1, 9),
                 notes="Tín ngưỡng Đạo giáo Trung Hoa, một số vùng Nam Bộ Việt Nam thờ. Opt-in."),
    HolidayEntry("Rằm tháng Giêng (Tết Nguyên Tiêu)", "imported", lunar=(1, 15),
                 notes="Hành Đạo giáo Trung Hoa (三元 Thượng Nguyên); opt-in."),
    HolidayEntry("Tết Hàn Thực", "imported", lunar=(3, 3),
                 notes="Nguồn gốc Trung Hoa; Việt hóa qua bánh trôi/bánh chay. Opt-in."),
    HolidayEntry("Lễ Thất Tịch", "imported", lunar=(7, 7),
                 notes="Nguồn gốc Trung Hoa (Ngưu Lang Chức Nữ). Opt-in."),
    HolidayEntry("Tết Trùng Cửu (Tết Trùng Dương)", "imported", lunar=(9, 9),
                 notes="Không phổ biến trong dân gian Việt Nam hiện đại. Opt-in."),
    HolidayEntry("Rằm tháng Mười (Tết Cơm Mới)", "imported", lunar=(10, 15),
                 notes="Có thờ ở một số địa phương; nguồn gốc Đạo giáo (三元 Hạ Nguyên). Opt-in."),
)

_SOLAR: tuple[HolidayEntry, ...] = (
    HolidayEntry("Tết Dương Lịch", "official", solar=(1, 1)),
    HolidayEntry("Ngày Giải phóng miền Nam", "official", solar=(4, 30)),
    HolidayEntry("Quốc tế Lao động", "official", solar=(5, 1)),
    HolidayEntry("Quốc khánh Việt Nam", "official", solar=(9, 2)),
    HolidayEntry("Ngày Phụ nữ Việt Nam", "official", solar=(10, 20)),
    HolidayEntry("Ngày Nhà giáo Việt Nam", "official", solar=(11, 20)),
    HolidayEntry("Ngày Thành lập QĐND Việt Nam", "official", solar=(12, 22)),
    HolidayEntry("Quốc tế Phụ nữ", "international", solar=(3, 8)),
    HolidayEntry("Quốc tế Thiếu nhi", "international", solar=(6, 1)),
    HolidayEntry("Lễ Tình Nhân (Valentine)", "imported", solar=(2, 14),
                 notes="Phương Tây, phổ biến tại VN, không phải lễ truyền thống."),
    HolidayEntry("Lễ Giáng sinh", "imported", solar=(12, 25),
                 notes="Kitô giáo; phổ biến văn hóa tại VN, không phải lễ truyền thống."),
)


class VnHolidayRegistry:
    """Single source of truth for Vietnamese holidays + cultural rituals."""

    LUNAR: tuple[HolidayEntry, ...] = _LUNAR
    SOLAR: tuple[HolidayEntry, ...] = _SOLAR

    @staticmethod
    def get_lunar(month: int, day: int, is_leap: bool = False,
                  with_imported: bool = False) -> str | None:
        """Return the first matching lunar holiday name for the given date.

        By default only `official`, `folk`, `buddhist_vn` scopes are returned.
        Pass `with_imported=True` to also include `imported` entries.
        Leap-month queries always return None (Vietnamese holidays occur on the
        principal month, not the leap duplicate).
        """
        if is_leap or month < 0:
            return None
        scopes: Iterable[HolidayScope] = (
            DEFAULT_SCOPES + (("imported",) if with_imported else ())
        )
        for entry in VnHolidayRegistry.LUNAR:
            if entry.lunar == (month, day) and entry.scope in scopes:
                return entry.name
        return None

    @staticmethod
    def get_solar(month: int, day: int, with_imported: bool = False) -> str | None:
        scopes: Iterable[HolidayScope] = (
            DEFAULT_SCOPES + (("imported",) if with_imported else ())
        )
        for entry in VnHolidayRegistry.SOLAR:
            if entry.solar == (month, day) and entry.scope in scopes:
                return entry.name
        return None

    @staticmethod
    def get_all_lunar(month: int, day: int, is_leap: bool = False) -> list[HolidayEntry]:
        """Return every entry matching the lunar date (regardless of scope)."""
        if is_leap or month < 0:
            return []
        return [e for e in VnHolidayRegistry.LUNAR if e.lunar == (month, day)]

    @staticmethod
    def get_all_solar(month: int, day: int) -> list[HolidayEntry]:
        return [e for e in VnHolidayRegistry.SOLAR if e.solar == (month, day)]


__all__ = [
    "HolidayEntry",
    "HolidayScope",
    "VnHolidayRegistry",
    "DEFAULT_SCOPES",
]
