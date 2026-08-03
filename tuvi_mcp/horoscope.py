# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Public horoscope library API.

Provides a clean, typed wrapper around the internal calculation functions:
    - ``Horoscope`` — main user-facing class
    - ``BirthInfo`` — immutable birth input container
    - ``Gender`` / ``Calendar`` — strongly-typed enums
    - ``HoroscopeResult`` — typed chart result with dict serialization

All public methods return JSON-serializable dicts (via ``HoroscopeResult.to_dict()``)
suitable for MCP responses, REST APIs, or direct consumption.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum, IntEnum
from typing import Any

from ._auspicious import get_auspicious_details as _get_auspicious_details
from ._chart import get_horoscope_chart as _get_horoscope_chart
from ._input import map_hour_of_day_to_branch
from ._rendering import generate_laso_image
from ._transit import get_van_han_analysis as _get_van_han_analysis


class Gender(IntEnum):
    """Gender of the subject. Maps to ansaotuvi's 1/-1 convention."""

    MALE = 1
    FEMALE = -1


class Calendar(Enum):
    """Calendar system of the birth date."""

    SOLAR = "solar"
    LUNAR = "lunar"


_BRANCH_START_HOUR: dict[int, int] = {
    1: 0,
    2: 1,
    3: 3,
    4: 5,
    5: 7,
    6: 9,
    7: 11,
    8: 13,
    9: 15,
    10: 17,
    11: 19,
    12: 21,
}


def _coerce_hour(value: Any) -> int:
    """Convert a flexible hour input to a canonical solar hour 0-23.

    Accepts:
        - int / float 0-23 (solar hour of day)
        - int 1-12 (1-indexed Earthly Branch — resolved to start-of-window hour)
        - str "14:30", "11h15", "9pm" (clock time)
        - str "Tý", "Ngọ", ... (Earthly Branch name)
    """
    from ._input import parse_hour, parse_solar_hour

    if isinstance(value, bool):
        raise ValueError("hour must be int or str")
    if isinstance(value, (int, float)):
        if 1 <= value <= 12 and int(value) == value:
            return _BRANCH_START_HOUR[int(value)]
        if 0 <= int(value) <= 23:
            return int(value) % 24
        raise ValueError(f"hour must be 0-23 (solar) or 1-12 (branch index), got {value!r}")
    if isinstance(value, str):
        solar_h = parse_solar_hour(value)
        if solar_h is not None:
            return solar_h
        branch = parse_hour(value)
        return _BRANCH_START_HOUR[branch]
    raise ValueError(f"Invalid hour: {value!r}")


def _hour_to_chart_token(hour: int) -> str:
    """Format a canonical solar hour as a 2-digit clock-time string.

    The chart layer's ``parse_hour`` interprets integers 1-12 as a branch
    index. Forcing a string token removes that ambiguity.
    """
    return f"{hour % 24:02d}:00"


@dataclass(frozen=True, slots=True)
class BirthInfo:
    """Immutable birth input container.

    ``hour`` is a canonical solar hour 0-23. Branch inputs (e.g. ``"Ngọ"``,
    ``7``) are resolved once at construction time via ``from_birth``.
    """

    name: str = "Khách"
    year: int = 1990
    month: int = 1
    day: int = 1
    hour: int = 12
    gender: Gender = Gender.MALE
    calendar: Calendar = Calendar.SOLAR
    timezone: float = 7.0

    def __post_init__(self) -> None:
        if not 1800 <= self.year <= 2100:
            raise ValueError(f"year must be between 1800 and 2100, got {self.year}")
        if not 1 <= self.month <= 12:
            raise ValueError(f"month must be between 1 and 12, got {self.month}")
        if not 1 <= self.day <= 31:
            raise ValueError(f"day must be between 1 and 31, got {self.day}")
        if not 0 <= self.hour <= 23:
            raise ValueError(f"hour must be between 0 and 23, got {self.hour}")

    @classmethod
    def parse_hour(cls, hour_val: Any) -> int:
        """Convert a flexible hour input to a canonical solar hour 0-23.

        Accepts the same forms as ``Horoscope.from_birth`` ``hour``.
        Delegates to the internal ``_coerce_hour`` to avoid duplicating
        the conversion logic.
        """
        return _coerce_hour(hour_val)

    def chart_branch(self) -> int:
        """Return the Earthly Branch index (1-12) for ``self.hour``."""
        return map_hour_of_day_to_branch(self.hour)


@dataclass(frozen=True, slots=True)
class HoroscopeResult:
    """Typed chart result with dict serialization.

    Returned by ``Horoscope.chart()``. All fields are JSON-serializable.
    """

    thien_ban: dict
    dia_ban: list
    cach_cuc: list
    transit_stars: list = field(default_factory=list)
    target_period: dict = field(default_factory=dict)
    dai_han: dict | None = None
    tieu_han: dict | None = None
    nguyet_han: dict | None = None
    nhat_han: dict | None = None

    def to_dict(self) -> dict:
        """Serialize to a plain dict (drop None values for cleaner JSON)."""
        out: dict[str, Any] = {
            "thien_ban": self.thien_ban,
            "dia_ban": self.dia_ban,
            "cach_cuc": self.cach_cuc,
        }
        if self.transit_stars:
            out["transit_stars"] = self.transit_stars
        if self.target_period:
            out["target_period"] = self.target_period
        if self.dai_han is not None:
            out["dai_han"] = self.dai_han
        if self.tieu_han is not None:
            out["tieu_han"] = self.tieu_han
        if self.nguyet_han is not None:
            out["nguyet_han"] = self.nguyet_han
        if self.nhat_han is not None:
            out["nhat_han"] = self.nhat_han
        return out

    def __getitem__(self, key: str) -> Any:
        """Dict-like access for backward compat with pre-refactor callers."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key) from None

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __iter__(self) -> Any:
        """Iterate over field names (like dict keys)."""
        return iter(self.__dataclass_fields__)


@dataclass(frozen=True, slots=True)
class TransitResult:
    """Typed transit (Vận Hạn) result with dict serialization.

    Returned by ``Horoscope.transit()``. All fields are JSON-serializable.
    Supports both attribute access (``res.target_period``) and dict-like
    access (``res["target_period"]``) for backward compatibility.
    """

    person_details: dict
    target_period: dict
    transit_stars: list
    dai_han: dict | None = None
    tieu_han: dict | None = None
    nguyet_han: dict | None = None
    nhat_han: dict | None = None

    def to_dict(self) -> dict:
        out: dict[str, Any] = {
            "person_details": self.person_details,
            "target_period": self.target_period,
            "transit_stars": self.transit_stars,
        }
        if self.dai_han is not None:
            out["dai_han"] = self.dai_han
        if self.tieu_han is not None:
            out["tieu_han"] = self.tieu_han
        if self.nguyet_han is not None:
            out["nguyet_han"] = self.nguyet_han
        if self.nhat_han is not None:
            out["nhat_han"] = self.nhat_han
        return out

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key) from None

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __iter__(self) -> Any:
        return iter(self.__dataclass_fields__)


@dataclass(frozen=True, slots=True)
class AuspiciousResult:
    """Typed auspicious day evaluation result with dict serialization.

    Returned by ``Horoscope.auspicious()``. All fields are JSON-serializable.
    Supports both attribute and dict-like access.
    """

    duong_lich: str
    am_lich: str
    can_chi_ngay: str
    ngay_hoang_dao: dict
    truc_ngay: dict
    nhi_thap_bat_tu: dict
    huong_xuat_hanh: dict
    gio_hoang_dao: list
    tiet_khi_hien_tai: str = "N/A"
    tiet_khi_tiep_theo: str = "N/A"

    def to_dict(self) -> dict:
        return {
            "duong_lich": self.duong_lich,
            "am_lich": self.am_lich,
            "can_chi_ngay": self.can_chi_ngay,
            "tiet_khi_hien_tai": self.tiet_khi_hien_tai,
            "tiet_khi_tiep_theo": self.tiet_khi_tiep_theo,
            "ngay_hoang_dao": self.ngay_hoang_dao,
            "truc_ngay": self.truc_ngay,
            "nhi_thap_bat_tu": self.nhi_thap_bat_tu,
            "huong_xuat_hanh": self.huong_xuat_hanh,
            "gio_hoang_dao": self.gio_hoang_dao,
        }

    def __getitem__(self, key: str) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key) from None

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def __iter__(self) -> Any:
        return iter(self.__dataclass_fields__)


def _coerce_gender(value: Any) -> Gender:
    if isinstance(value, Gender):
        return value
    if isinstance(value, bool):
        return Gender.MALE if value else Gender.FEMALE
    if isinstance(value, (int, float)):
        return Gender.MALE if int(value) >= 1 else Gender.FEMALE
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("nam", "male", "m", "1", "true"):
            return Gender.MALE
        if v in ("nữ", "nu", "female", "f", "-1", "false"):
            return Gender.FEMALE
    raise ValueError(f"Invalid gender: {value!r}")


def _coerce_calendar(value: Any) -> Calendar:
    if isinstance(value, Calendar):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("solar", "duong", "dương", "dương lịch"):
            return Calendar.SOLAR
        if v in ("lunar", "am", "âm"):
            return Calendar.LUNAR
    if isinstance(value, bool):
        return Calendar.SOLAR if value else Calendar.LUNAR
    raise ValueError(f"Invalid calendar: {value!r}")


class Horoscope:
    """User-facing horoscope handle.

    Construct via ``Horoscope.from_birth(...)``. Then call ``.chart()``,
    ``.transit(...)``, ``.auspicious(...)``, or ``.render_chart(...)``.
    """

    def __init__(self, birth: BirthInfo) -> None:
        self._birth = birth

    @classmethod
    def from_birth(
        cls,
        name: str = "Khách",
        year: int = 1990,
        month: int = 1,
        day: int = 1,
        hour: Any = 12,
        gender: Any = "male",
        calendar: Any = "solar",
        timezone: Any = 7,
    ) -> "Horoscope":
        """Construct a Horoscope from raw birth details.

        Accepts flexible inputs:
            - ``hour``: int 0-23 (solar hour), int 1-12 (branch index), or
              str ("14:30", "Ngọ", "Tý")
            - ``gender``: Gender enum, int (±1), bool, or str ("Nam"/"male"/"M")
            - ``calendar``: Calendar enum or str ("solar"/"lunar")

        Raises ``ValueError`` for invalid inputs.

        Note: civil hour is always interpreted as **local time at the
        birthplace**. Astronomical (sun/moon) lookup inside the engine is
        computed using UTC+7; for births far from Vietnam near a lunar-day
        boundary, results may differ by one day from tools that adjust
        the astronomical reference timezone. Apply daylight-saving-time
        adjustments *before* passing ``hour``.
        """
        gender_enum = _coerce_gender(gender)
        calendar_enum = _coerce_calendar(calendar)
        hour_int = _coerce_hour(hour)
        tz = float(timezone) if timezone is not None else 7.0
        # Note: the library API intentionally accepts any float offset (e.g. 5.75
        # for Nepal NPT), unlike the stricter MCP layer which only allows integer
        # hours and h:30 half-hour increments via coerce_timezone.
        birth = BirthInfo(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour_int,
            gender=gender_enum,
            calendar=calendar_enum,
            timezone=tz,
        )
        return cls(birth)

    @property
    def birth(self) -> BirthInfo:
        """The validated birth input."""
        return self._birth

    def chart(self) -> HoroscopeResult:
        """Calculate the base birth chart (Thiên Bàn + Địa Bàn + Cách Cục).

        Honors ``BirthInfo.timezone`` for the astronomical boundary rounding.
        """
        raw = _get_horoscope_chart(
            name=self._birth.name,
            day=self._birth.day,
            month=self._birth.month,
            year=self._birth.year,
            hour_val=_hour_to_chart_token(self._birth.hour),
            gender_val=int(self._birth.gender),
            is_solar=self._birth.calendar is Calendar.SOLAR,
            timezone=self._birth.timezone,
        )
        if isinstance(raw, dict) and "error" in raw:
            raise ValueError(raw["error"])
        return HoroscopeResult(
            thien_ban=raw.get("thien_ban", {}),
            dia_ban=raw.get("dia_ban", []),
            cach_cuc=raw.get("cach_cuc", []),
        )

    def transit(
        self,
        year: int | None = None,
        month: int = 1,
        day: int | None = None,
    ) -> TransitResult:
        """Calculate transit (Vận Hạn) analysis for a target Lunar period.

        Honors ``BirthInfo.timezone`` for the astronomical boundary rounding
        of the birth chart that transits are anchored to.

        Args:
            year: Target Lunar year. Defaults to current year.
            month: Target Lunar month (1-12). Default 1.
            day: Target Lunar day (1-30). Optional — when provided, returns
                 ``nhat_han`` in addition to ``nguyet_han``.

        Returns:
            TransitResult with fields: ``person_details``, ``target_period``,
            ``transit_stars``, ``dai_han``, ``tieu_han``, ``nguyet_han``,
            and (if ``day`` given) ``nhat_han``.
        """
        if year is None:
            year = datetime.now().year
        raw = _get_van_han_analysis(
            name=self._birth.name,
            day=self._birth.day,
            month=self._birth.month,
            year=self._birth.year,
            hour_val=_hour_to_chart_token(self._birth.hour),
            gender_val=int(self._birth.gender),
            is_solar=self._birth.calendar is Calendar.SOLAR,
            current_year=year,
            current_month=month,
            current_day=day,
            timezone=self._birth.timezone,
        )
        if isinstance(raw, dict) and "error" in raw:
            raise ValueError(raw["error"])
        return TransitResult(
            person_details=raw.get("person_details", {}),
            target_period=raw.get("target_period", {}),
            transit_stars=raw.get("transit_stars", []),
            dai_han=raw.get("dai_han"),
            tieu_han=raw.get("tieu_han"),
            nguyet_han=raw.get("nguyet_han"),
            nhat_han=raw.get("nhat_han"),
        )

    def auspicious(
        self,
        day: int | None = None,
        month: int | None = None,
        year: int | None = None,
        timezone: float | None = None,
    ) -> AuspiciousResult:
        """Evaluate auspicious details for a given calendar date.

        Any omitted component defaults to today's date. ``timezone`` defaults
        to ``BirthInfo.timezone`` when omitted (or ``7.0`` if neither set).

        Note: ``day``, ``month``, ``year`` are always interpreted as a **Solar**
        (Gregorian) date. Passing a Lunar date here will yield incorrect results;
        convert to Solar first using ``tuvi_mcp._calendar.convert_lunar_to_solar``
        if needed.

        Returns:
            AuspiciousResult with fields: ``duong_lich``, ``am_lich``,
            ``can_chi_ngay``, ``ngay_hoang_dao``, ``truc_ngay``,
            ``nhi_thap_bat_tu``, ``huong_xuat_hanh``, ``gio_hoang_dao``,
            ``tiet_khi_hien_tai``, ``tiet_khi_tiep_theo``.
        """
        today = date.today()
        tz = self._birth.timezone if timezone is None else timezone
        raw = _get_auspicious_details(
            day if day is not None else today.day,
            month if month is not None else today.month,
            year if year is not None else today.year,
            is_solar=True,
            timezone=tz,
        )
        if isinstance(raw, dict) and "error" in raw:
            raise ValueError(raw["error"])
        return AuspiciousResult(
            duong_lich=raw["duong_lich"],
            am_lich=raw["am_lich"],
            can_chi_ngay=raw["can_chi_ngay"],
            ngay_hoang_dao=raw["ngay_hoang_dao"],
            truc_ngay=raw["truc_ngay"],
            nhi_thap_bat_tu=raw["nhi_thap_bat_tu"],
            huong_xuat_hanh=raw["huong_xuat_hanh"],
            gio_hoang_dao=raw["gio_hoang_dao"],
            tiet_khi_hien_tai=raw.get("tiet_khi_hien_tai", "N/A"),
            tiet_khi_tiep_theo=raw.get("tiet_khi_tiep_theo", "N/A"),
        )

    def render_chart(
        self,
        chart: HoroscopeResult | dict | None = None,
        year: int | None = None,
        font_path: str | None = None,
        font_bold_path: str | None = None,
    ) -> str:
        """Render the chart as a PNG image. Returns the file path.

        :param chart: Pre-calculated chart result or dict. Defaults to ``self.chart().to_dict()``.
        :param year: Transit target Lunar year for display in chart header.
        :param font_path: Path to a custom TrueType (.ttf) regular font file. Defaults to bundled Roboto font.
        :param font_bold_path: Path to a custom TrueType (.ttf) bold font file.
        :return: Path to rendered PNG file in system temporary directory.
        """
        if chart is None:
            chart = self.chart().to_dict()
        elif isinstance(chart, HoroscopeResult):
            chart = chart.to_dict()
        return generate_laso_image(chart, current_year=year, font_path=font_path, font_bold_path=font_bold_path)


__all__ = [
    "AuspiciousResult",
    "BirthInfo",
    "Calendar",
    "Gender",
    "Horoscope",
    "HoroscopeResult",
    "TransitResult",
]
