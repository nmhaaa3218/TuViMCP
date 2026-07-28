# -*- coding: utf-8 -*-
"""
Regression lock for `Solar.next(days, only_work_day=True)`.

After v1.4.9 removed `HolidayUtil` (PRC statutory schedule mislabeled
Vietnamese), `Solar.next` falls back to weekend-skip behavior in
`only_work_day=True` mode. These tests lock in that fallback contract.
"""
import pytest

from tuvi_mcp.lunar_calendar import Solar


def test_next_skips_weekend_when_only_work_day_true():
    """Forward 1 work-day from a Friday must land on Monday, not Saturday."""
    # 2026-02-13 is a Friday
    friday = Solar.fromYmd(2026, 2, 13)
    # 0=Sunday, 1=Monday, ..., 5=Friday, 6=Saturday
    assert friday.getWeek() == 5
    next_work = friday.next(1, only_work_day=True)
    # 2026-02-16 is Monday
    assert (next_work.getYear(), next_work.getMonth(), next_work.getDay()) == (2026, 2, 16)


def test_next_does_not_skip_weekend_when_only_work_day_false():
    """Default mode (calendar days) must NOT skip weekends."""
    friday = Solar.fromYmd(2026, 2, 13)
    next_day = friday.next(1)
    assert (next_day.getYear(), next_day.getMonth(), next_day.getDay()) == (2026, 2, 14)


def test_next_skip_saturday_only():
    """Forward 1 work-day from a Saturday must land on Monday."""
    # 2026-02-14 is a Saturday
    saturday = Solar.fromYmd(2026, 2, 14)
    assert saturday.getWeek() == 6
    next_work = saturday.next(1, only_work_day=True)
    assert (next_work.getYear(), next_work.getMonth(), next_work.getDay()) == (2026, 2, 16)


def test_next_skip_sunday_only():
    """Forward 1 work-day from a Sunday must land on Monday."""
    # 2026-02-15 is a Sunday
    sunday = Solar.fromYmd(2026, 2, 15)
    assert sunday.getWeek() == 0
    next_work = sunday.next(1, only_work_day=True)
    assert (next_work.getYear(), next_work.getMonth(), next_work.getDay()) == (2026, 2, 16)


def test_next_zero_days_with_only_work_day():
    """next(0, only_work_day=True) must not raise and must not skip days."""
    friday = Solar.fromYmd(2026, 2, 13)
    same = friday.next(0, only_work_day=True)
    assert (same.getYear(), same.getMonth(), same.getDay()) == (2026, 2, 13)


def test_next_negative_days_with_only_work_day():
    """Backward 1 work-day from a Monday must land on Friday (skip weekend)."""
    # 2026-02-16 is a Monday
    monday = Solar.fromYmd(2026, 2, 16)
    assert monday.getWeek() == 1
    prev_work = monday.next(-1, only_work_day=True)
    assert (prev_work.getYear(), prev_work.getMonth(), prev_work.getDay()) == (2026, 2, 13)


def test_next_multiple_work_days_across_weekend():
    """Forward 3 work-days from Wednesday must land on Monday (skip weekend)."""
    # 2026-02-11 is a Wednesday
    wed = Solar.fromYmd(2026, 2, 11)
    assert wed.getWeek() == 3
    three_work_days_later = wed.next(3, only_work_day=True)
    # Wed + Thu + Fri + Mon = 4 calendar days, but 3 work days = Mon 16
    yr, mo, dy = (
        three_work_days_later.getYear(),
        three_work_days_later.getMonth(),
        three_work_days_later.getDay(),
    )
    assert (yr, mo, dy) == (2026, 2, 16)


def test_next_does_not_raise_attribute_error():
    """Regression: before v1.4.9, only_work_day=True called deleted
    HolidayUtil.getHoliday and would AttributeError if it was None."""
    friday = Solar.fromYmd(2026, 2, 13)
    try:
        friday.next(1, only_work_day=True)
    except AttributeError as e:
        pytest.fail(
            f"Solar.next regressed: AttributeError accessing deleted HolidayUtil: {e}"
        )
