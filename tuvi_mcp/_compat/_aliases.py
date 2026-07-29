# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

Module aliasing helper for backward-compatible shims.

Vendored engine code originally lived at the public path
(``tuvi_mcp.lunar_calendar``, ``tuvi_mcp.ansaotuvi``) and was moved to
private locations (``tuvi_mcp._lunar_calendar``, ``tuvi_mcp._engine``).
Many callers used the submodule form, e.g.
``from tuvi_mcp.lunar_calendar.Lunar import Lunar``. To preserve that
form without keeping duplicate module files, this helper registers the
private submodule under the public name in :mod:`sys.modules`.
"""

from __future__ import annotations

import sys
import types


def install_module_aliases(
    public_pkg: str,
    private_pkg: str,
    modules: dict[str, types.ModuleType] | None = None,
) -> int:
    """Register every submodule path of ``private_pkg`` under ``public_pkg``.

    Walks ``modules`` (typically :data:`sys.modules`) for entries whose key
    starts with ``private_pkg + "."`` and creates a matching entry under
    ``public_pkg`` pointing at the same module object. Both leaf modules
    (e.g. ``private_pkg.Lunar``) and intermediate packages (e.g.
    ``private_pkg.util``, ``private_pkg.sino_vn_huyen_hoc``) get aliased.

    This makes ``import public_pkg.X`` and
    ``from public_pkg.subpackage.X import ...`` resolve even when only the
    private module exists — the canonical use-case for our backward-compat
    shims under ``tuvi_mcp.lunar_calendar`` and ``tuvi_mcp.ansaotuvi``.

    Returns the number of aliases created.
    """
    modules = modules if modules is not None else sys.modules
    prefix_private = private_pkg + "."
    count = 0
    # Discover all module paths under private_pkg that are currently
    # loaded; this includes both leaf modules and intermediate packages.
    private_paths: list[str] = []
    for full_name in list(modules):
        if not full_name.startswith(prefix_private):
            continue
        tail = full_name[len(prefix_private):]
        if not tail:
            continue
        private_paths.append(tail)
    # Register longest paths first so intermediate entries already exist
    # when a child references them. Use dedup + sort.
    for tail in sorted(set(private_paths), key=lambda s: s.count("."), reverse=True):
        target = public_pkg + "." + tail
        if target in modules:
            continue
        modules[target] = modules[private_pkg + "." + tail]
        count += 1
    return count


__all__ = ["install_module_aliases"]
