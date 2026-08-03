# -*- coding: utf-8 -*-
"""
Tests for bundled font loading and custom font_path override in tuvi_mcp._rendering.
"""
import os
from unittest.mock import patch
from PIL import ImageFont
import pytest

from tuvi_mcp._rendering import get_font, generate_laso_image
from tuvi_mcp.horoscope import Horoscope


def test_bundled_font_resolution():
    """Verify that get_font resolves bundled Roboto fonts."""
    font_reg = get_font(size=12, bold=False)
    assert font_reg is not None
    assert isinstance(font_reg, ImageFont.FreeTypeFont)

    font_bold = get_font(size=14, bold=True)
    assert font_bold is not None
    assert isinstance(font_bold, ImageFont.FreeTypeFont)


def test_headless_environment_fallback():
    """Simulate a headless environment with no OS desktop fonts installed."""
    orig_exists = os.path.exists

    def fake_exists(path):
        # Return False for all OS system font paths, but True for bundled Roboto fonts
        if "Arial" in str(path) or "/usr/share/fonts" in str(path) or "Windows\\Fonts" in str(path):
            return False
        return orig_exists(path)

    with patch("os.path.exists", side_effect=fake_exists):
        font = get_font(size=12, bold=False)
        assert font is not None
        assert isinstance(font, ImageFont.FreeTypeFont)


def test_custom_font_path_override():
    """Verify custom font_path parameter overrides defaults."""
    bundled_path = os.path.join(os.path.dirname(__file__), "..", "tuvi_mcp", "_fonts", "Roboto-Regular.ttf")
    font = get_font(size=16, font_path=bundled_path)
    assert font is not None
    assert isinstance(font, ImageFont.FreeTypeFont)


def test_generate_laso_image_renders_with_bundled_font(tmp_path):
    """Test generating a chart PNG image using Horoscope API."""
    h = Horoscope.from_birth(name="Nguyễn Văn A", day=15, month=8, year=1995, hour=10, gender="Nam")
    img_path = h.render_chart(year=2026)

    assert os.path.exists(img_path)
    assert os.path.getsize(img_path) > 0
    assert img_path.endswith(".png")


def test_invalid_font_path_graceful_fallback():
    """Verify non-existent or invalid font_path falls back gracefully to bundled font."""
    font = get_font(size=12, font_path="/path/to/non_existent_font.ttf")
    assert font is not None
    assert isinstance(font, ImageFont.FreeTypeFont)


def test_corrupted_font_file_fallback(tmp_path):
    """Verify corrupted TTF file falls back gracefully without raising an unhandled exception."""
    bad_font_file = tmp_path / "broken.ttf"
    bad_font_file.write_text("This is not a font file.")

    font = get_font(size=12, font_path=str(bad_font_file))
    assert font is not None


def test_invalid_type_font_path():
    """Verify passing non-string invalid types (int, dict, list) to font_path is handled safely."""
    font1 = get_font(size=12, font_path=12345)
    assert font1 is not None

    font2 = get_font(size=12, font_path={"invalid": "object"})
    assert font2 is not None


def test_complete_absence_of_fonts_fallback():
    """Verify load_default fallback when both OS fonts and bundled fonts are simulated missing."""
    with patch("os.path.exists", return_value=False):
        font = get_font(size=12)
        assert font is not None


def test_render_chart_long_vietnamese_name_and_transit():
    """Test rendering chart with long Vietnamese diacritic name and transit stars."""
    h = Horoscope.from_birth(
        name="Nguyễn Hoàng Quốc Phượng Cửu Trọng Thiên",
        day=29,
        month=12,
        year=1999,
        hour=23,
        gender="Nữ",
    )
    img_path = h.render_chart(year=2026)
    assert os.path.exists(img_path)
    assert os.path.getsize(img_path) > 0
