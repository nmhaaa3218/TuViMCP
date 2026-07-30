#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(c) 2026 nmhaaa3218 <manh.ha.3218@gmail.com>

CLI entry point for the TuViMCP server.

Run with:
    python -m tuvi_mcp                  # stdio transport (default)
    python -m tuvi_mcp --http           # streamable-http on 127.0.0.1:1850
    python -m tuvi_mcp --http --port 9000
"""

import argparse
import sys

from ._server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Tu Vi horoscope MCP Server.")
    parser.add_argument("--http", action="store_true", help="Use streamable-http transport instead of stdio.")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host.")
    parser.add_argument("--port", type=int, default=1850, help="HTTP port.")
    args = parser.parse_args()

    if args.http:
        print(f"Starting Tu Vi MCP server on streamable-http://{args.host}:{args.port}", file=sys.stderr)
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="streamable-http")
    else:
        print("Starting Tu Vi MCP server on stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
