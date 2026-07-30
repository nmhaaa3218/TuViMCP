# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. The implementation moved to
``tuvi_mcp._auspicious``. This module re-exports the public function
``get_auspicious_details`` so existing imports keep working.
"""

from ._auspicious import get_auspicious_details  # noqa: F401

__all__ = ["get_auspicious_details"]
