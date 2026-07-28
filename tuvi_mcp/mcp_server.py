# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. The FastMCP server definition moved to
``tuvi_mcp.server``; this module remains so that existing imports such as
``from tuvi_mcp.mcp_server import generate_horoscope`` keep working.
"""

from .server import (
    convert_calendar,
    generate_horoscope,
    get_auspicious_info,
    get_van_han,
    mcp,
)

__all__ = ["convert_calendar", "generate_horoscope", "get_auspicious_info", "get_van_han", "mcp"]


def main():
    """Backward-compatible CLI entry; delegates to ``__main__.main``."""
    from .__main__ import main as _main

    _main()
