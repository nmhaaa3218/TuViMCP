# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>
Vietnamese Lunar Calendar Astronomical Engine (UTC+7).
Based on standard astronomical algorithms by Jean Meeus / Ho Ngoc Duc.
"""

import math


def jdFromDate(dd: int, mm: int, yy: int) -> int:
    """Compute integral Julian day number for day dd/mm/yyyy."""
    a = int((14 - mm) / 12.0)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = (
        dd
        + int((153 * m + 2) / 5.0)
        + 365 * y
        + int(y / 4.0)
        - int(y / 100.0)
        + int(y / 400.0)
        - 32045
    )
    if jd < 2299161:
        jd = dd + int((153 * m + 2) / 5.0) + 365 * y + int(y / 4.0) - 32083
    return jd


def jdToDate(jd: int) -> list[int]:
    """Convert a Julian day number to [day, month, year]."""
    if jd > 2299160:
        a = jd + 32044
        b = int((4 * a + 3) / 146097.0)
        c = a - int((b * 146097) / 4.0)
    else:
        b = 0
        c = jd + 32082
    d = int((4 * c + 3) / 1461.0)
    e = c - int((1461 * d) / 4.0)
    m = int((5 * e + 2) / 153.0)
    day = e - int((153 * m + 2) / 5.0) + 1
    month = m + 3 - 12 * int(m / 10.0)
    year = b * 100 + d - 4800 + int(m / 10.0)
    return [day, month, year]


def NewMoon(k: float) -> float:
    """Compute exact time of the k-th new moon after 1900-01-01 13:52 UTC."""
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180.0
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 = Jd1 + 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)

    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3

    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
    C1 = C1 + 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))

    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2

    JdNew = Jd1 + C1 - deltat
    return JdNew


def getSunLongitude(jdn: float, timeZone: float = 7.0) -> int:
    """Compute sun position index (0..11) for major solar terms."""
    T = (jdn - 2451545.5 - timeZone / 24.0) / 36525.0
    T2 = T**2
    dr = math.pi / 180.0
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL = DL + (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = L0 + DL
    omega = 125.04 - 1934.136 * T
    L = L - 0.00569 - 0.00478 * math.sin(omega * dr)
    L = L * dr
    L = L - math.pi * 2 * (math.floor(L / (math.pi * 2)))
    return int(L / math.pi * 6)


def getNewMoonDay(k: int, timeZone: float = 7.0) -> int:
    """Compute the Julian Day number of the k-th new moon in UTC+7."""
    return int(NewMoon(k) + 0.5 + timeZone / 24.0)


def getLunarMonth11(yy: int, timeZone: float = 7.0) -> int:
    """Find the start day (Julian day) of lunar month 11 of year yy."""
    off = jdFromDate(31, 12, yy) - 2415021.0
    k = int(off / 29.530588853)
    nm = getNewMoonDay(k, timeZone)
    sunLong = getSunLongitude(nm, timeZone)
    if sunLong >= 9:
        nm = getNewMoonDay(k - 1, timeZone)
    return nm


def getLeapMonthOffset(a11: int, timeZone: float = 7.0) -> int:
    """Find leap month index following month starting on day a11."""
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1
    arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
    while True:
        last = arc
        i += 1
        arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar_vn(dd: int, mm: int, yy: int, time_zone: float = 7.0) -> list[int]:
    """
    Convert Solar date dd/mm/yyyy to Vietnamese Lunar date [lunarDay, lunarMonth, lunarYear, lunarLeap].
    """
    dayNumber = jdFromDate(dd, mm, yy)
    k = int((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = getNewMoonDay(k + 1, time_zone)
    if monthStart > dayNumber:
        monthStart = getNewMoonDay(k, time_zone)

    a11 = getLunarMonth11(yy, time_zone)
    b11 = a11
    if a11 >= monthStart:
        lunarYear = yy
        a11 = getLunarMonth11(yy - 1, time_zone)
    else:
        lunarYear = yy + 1
        b11 = getLunarMonth11(yy + 1, time_zone)

    lunarDay = dayNumber - monthStart + 1
    diff = int((monthStart - a11) / 29.0)

    lunarLeap = 0
    lunarMonth = diff + 11

    if b11 - a11 > 365:
        leapMonthDiff = getLeapMonthOffset(a11, time_zone)
        if diff >= leapMonthDiff:
            lunarMonth = diff + 10
            if diff == leapMonthDiff:
                lunarLeap = 1

    if lunarMonth > 12:
        lunarMonth = lunarMonth - 12

    if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1

    return [lunarDay, lunarMonth, lunarYear, lunarLeap]


def lunar_to_solar_vn(lunarD: int, lunarM: int, lunarY: int, lunarLeap: int = 0, time_zone: float = 7.0) -> list[int]:
    """
    Convert Vietnamese Lunar date to Solar date [day, month, year].
    """
    if lunarM < 11:
        a11 = getLunarMonth11(lunarY - 1, time_zone)
        b11 = getLunarMonth11(lunarY, time_zone)
    else:
        a11 = getLunarMonth11(lunarY, time_zone)
        b11 = getLunarMonth11(lunarY + 1, time_zone)

    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunarM - 11
    if off < 0:
        off += 12

    if b11 - a11 > 365:
        leapOff = getLeapMonthOffset(a11, time_zone)
        leapM = leapOff - 2
        if leapM < 0:
            leapM += 12
        if lunarLeap != 0 and lunarM != leapM:
            return [0, 0, 0]
        elif lunarLeap != 0 or off >= leapOff:
            off += 1

    monthStart = getNewMoonDay(k + off, time_zone)
    return jdToDate(monthStart + lunarD - 1)
