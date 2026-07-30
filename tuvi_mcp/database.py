# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Backward-compatible shim. Implementation moved to ``tuvi_mcp._storage``.
"""

from ._storage import (
    DB_FILE,
    delete_saved_horoscope_by_id,
    get_connection,
    get_saved_horoscope_by_id,
    get_saved_horoscope_by_name,
    init_db,
    list_saved_horoscopes,
    save_horoscope,
)

__all__ = [
    "DB_FILE",
    "delete_saved_horoscope_by_id",
    "get_connection",
    "get_saved_horoscope_by_id",
    "get_saved_horoscope_by_name",
    "init_db",
    "list_saved_horoscopes",
    "save_horoscope",
]
