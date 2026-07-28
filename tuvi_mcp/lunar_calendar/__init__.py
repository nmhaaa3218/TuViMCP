# -*- coding: utf-8 -*-
__version__ = '1.4.9'

# Order matters: Solar must be importable before Lunar (circular ref).
from .Holiday import Holiday
from .JieQi import JieQi
from .NineStar import NineStar
from .Solar import Solar
from .SolarWeek import SolarWeek
from .SolarMonth import SolarMonth
from .SolarSeason import SolarSeason
from .SolarHalfYear import SolarHalfYear
from .SolarYear import SolarYear
from .LunarTime import LunarTime
from .Lunar import Lunar
from .LunarYear import LunarYear
from .LunarMonth import LunarMonth
from .util import VnCalendarUtil
from .VietnameseHoliday import VietnameseHoliday
from .vn_holidays import HolidayEntry, HolidayScope, VnHolidayRegistry

# Native Vietnamese Aliases
LichAm = Lunar
LichDuong = Solar

