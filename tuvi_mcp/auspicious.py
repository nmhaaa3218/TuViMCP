# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Public auspicious-day API.

Re-exports `get_auspicious_details` from the internal `auspicious_calculator`
module under a stable, semantic name.
"""

from .auspicious_calculator import get_auspicious_details

__all__ = ["get_auspicious_details"]
