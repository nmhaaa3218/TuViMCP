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
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any

from ._chart import get_horoscope_chart as _get_horoscope_chart
from ._rendering import generate_laso_image
from ._transit import get_van_han_analysis as _get_van_han_analysis
from .auspicious import get_auspicious_details as _get_auspicious_details
from .tuvi_calculator import (
    get_van_han_analysis as _get_van_han_analysis,
)


class Gender(IntEnum):
    """Gender of the subject. Maps to ansaotuvi's 1/-1 convention."""

    MALE = 1
    FEMALE = -1


class Calendar(Enum):
    """Calendar system of the birth date."""

    SOLAR = "solar"
    LUNAR = "lunar"


@dataclass(frozen=True, slots=True)
class BirthInfo:
    """Immutable birth input container.

    Hour is the solar hour 0-23. Use ``BirthInfo.parse_hour`` to convert
    string forms ("14:30", "Ngọ", 7) to integer hours if needed.
    """

    name: str = "Khách"
    year: int = 1990
    month: int = 1
    day: int = 1
    hour: int = 12
    gender: Gender = Gender.MALE
    calendar: Calendar = Calendar.SOLAR
    timezone: int = 7

    def __post_init__(self) -> None:
        if not 1800 <= self.year <= 2100:
            raise ValueError(f"year must be between 1800 and 2100, got {self.year}")
        if not 1 <= self.month <= 12:
            raise ValueError(f"month must be between 1 and 12, got {self.month}")
        if not 1 <= self.day <= 31:
            raise ValueError(f"day must be between 1 and 31, got {self.day}")
        if not 0 <= self.hour <= 23:
            raise ValueError(f"hour must be between 0 and 23, got {self.hour}")
        if not -12 <= self.timezone <= 14:
            raise ValueError(f"timezone must be between -12 and 14, got {self.timezone}")

    @classmethod
    def parse_hour(cls, hour_val: Any) -> int:
        """Convert a flexible hour input to an integer 0-23.

        Accepts:
            - int / float 0-23 (solar hour of day)
            - int 1-12 (1-indexed Earthly Branch)
            - str "14:30", "11h15", "9pm" (clock time)
            - str "Tý", "Ngọ", ... (Earthly Branch name)
        """
        from ._input import parse_solar_hour

        return parse_solar_hour(hour_val) if parse_solar_hour(hour_val) is not None else int(hour_val) % 24


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


class Horoscope:
    """User-facing horoscope handle.

    Construct via ``Horoscope.from_birth(...)``. Then call ``.chart()``,
    ``.transit(...)``, ``.auspicious(...)``, or ``.render_chart(...)``.

    Internally wraps the module-level ``tuvi_calculator`` functions with
    parsed/validated inputs.
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
        timezone: int = 7,
    ) -> "Horoscope":
        """Construct a Horoscope from raw birth details.

        Accepts flexible inputs:
            - ``hour``: int 0-23, int 1-12 (branch index), or str ("14:30", "Ngọ")
            - ``gender``: Gender enum, int (±1), bool, or str ("Nam"/"male"/"M")
            - ``calendar``: Calendar enum or str ("solar"/"lunar")

        Raises ``ValueError`` for invalid inputs.
        """
        gender_enum = _coerce_gender(gender)
        calendar_enum = _coerce_calendar(calendar)
        hour_int = _coerce_hour(hour)
        birth = BirthInfo(
            name=name,
            year=year,
            month=month,
            day=day,
            hour=hour_int,
            gender=gender_enum,
            calendar=calendar_enum,
            timezone=timezone,
        )
        return cls(birth)

    @property
    def birth(self) -> BirthInfo:
        """The validated birth input."""
        return self._birth

    def chart(self) -> HoroscopeResult:
        """Calculate the base birth chart (Thiên Bàn + Địa Bàn + Cách Cục)."""
        raw = _get_horoscope_chart(
            name=self._birth.name,
            day=self._birth.day,
            month=self._birth.month,
            year=self._birth.year,
            hour_val=self._birth.hour,
            gender_val=int(self._birth.gender),
            is_solar=self._birth.calendar is Calendar.SOLAR,
        )
        if isinstance(raw, dict) and "error" in raw:
            return HoroscopeResult(
                thien_ban=raw,
                dia_ban=[],
                cach_cuc=[],
            )
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
    ) -> dict:
        """Calculate transit (Vận Hạn) analysis for a target Lunar period.

        Args:
            year: Target Lunar year. Defaults to current year.
            month: Target Lunar month (1-12). Default 1.
            day: Target Lunar day (1-30). Optional — when provided, returns
                 ``nhat_han`` in addition to ``nguyet_han``.

        Returns:
            dict with keys: ``person_details``, ``target_period``,
            ``transit_stars``, ``dai_han``, ``tieu_han``, ``nguyet_han``,
            and (if ``day`` given) ``nhat_han``.
        """
        if year is None:
            year = datetime.now().year
        return _get_van_han_analysis(
            name=self._birth.name,
            day=self._birth.day,
            month=self._birth.month,
            year=self._birth.year,
            hour_val=self._birth.hour,
            gender_val=int(self._birth.gender),
            is_solar=self._birth.calendar is Calendar.SOLAR,
            current_year=year,
            current_month=month,
            current_day=day,
        )

    def auspicious(self, day: int | None = None, month: int | None = None, year: int | None = None) -> dict:
        """Evaluate auspicious details for a given calendar date.

        All three parameters default to today's date if omitted.
        """
        return _get_auspicious_details(day, month, year, is_solar=True)

    def render_chart(self, chart: HoroscopeResult | dict | None = None, year: int | None = None) -> str:
        """Render the chart as a PNG image. Returns the file path."""
        if chart is None:
            chart = self.chart().to_dict()
        elif isinstance(chart, HoroscopeResult):
            chart = chart.to_dict()
        return generate_laso_image(chart, current_year=year)


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


def _coerce_hour(value: Any) -> int:
    """Convert flexible hour input to integer 0-23."""
    from ._input import parse_hour, parse_solar_hour

    if isinstance(value, bool):
        raise ValueError("hour must be int or str")
    if isinstance(value, (int, float)):
        if 1 <= value <= 12 and int(value) == value:
            branch_to_hour = {1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 9, 7: 11, 8: 13, 9: 15, 10: 17, 11: 19, 12: 21}
            return branch_to_hour[int(value)]
        return int(value) % 24
    if isinstance(value, str):
        solar_h = parse_solar_hour(value)
        if solar_h is not None:
            return solar_h
        branch = parse_hour(value)
        branch_to_hour = {1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 9, 7: 11, 8: 13, 9: 15, 10: 17, 11: 19, 12: 21}
        return branch_to_hour[branch]
    raise ValueError(f"Invalid hour: {value!r}")


__all__ = [
    "BirthInfo",
    "Calendar",
    "Gender",
    "Horoscope",
    "HoroscopeResult",
]
