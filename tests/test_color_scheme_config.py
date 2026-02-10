#!/usr/bin/env python3
"""
Tests for configurable color schemes.
"""

import os
import sys
import tempfile

import pytest
from colorama import Fore

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from color_scheme import ColorScheme
from config_loader import ConfigLoader


@pytest.fixture(autouse=True)
def reset_color_scheme():
    """Ensure color palette is reset between tests."""
    ColorScheme.reset_to_default()
    yield
    ColorScheme.reset_to_default()


def _write_config(content: str) -> str:
    """Write temporary config content and return path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(content)
        return f.name


def test_default_color_scheme_is_monokai_when_missing():
    """Config without color_scheme should default to monokai."""
    config_path = _write_config('default_interval = "1s"\n\n[[files]]\npath = ""\ncommand = "echo ok"\n')
    try:
        config = ConfigLoader.load_config(config_path)
        assert config["color_scheme"] == ColorScheme.DEFAULT_COLOR_SCHEME
        assert "38;2;166;226;46" in Fore.GREEN
    finally:
        os.unlink(config_path)


def test_supported_color_scheme_is_applied():
    """Config with supported color_scheme should be applied."""
    config_path = _write_config('color_scheme = "classic"\n\n[[files]]\npath = ""\ncommand = "echo ok"\n')
    try:
        config = ConfigLoader.load_config(config_path)
        assert config["color_scheme"] == "classic"
        assert Fore.GREEN == "\x1b[32m"
    finally:
        os.unlink(config_path)


def test_invalid_color_scheme_falls_back_to_default():
    """Unsupported color_scheme should fall back to default palette."""
    config_path = _write_config('color_scheme = "unknown"\n\n[[files]]\npath = ""\ncommand = "echo ok"\n')
    try:
        config = ConfigLoader.load_config(config_path)
        assert config["color_scheme"] == ColorScheme.DEFAULT_COLOR_SCHEME
        assert "38;2;166;226;46" in Fore.GREEN
    finally:
        os.unlink(config_path)


def test_custom_color_scheme_from_table():
    """Custom color codes in table format should override palette."""
    config_path = _write_config(
        """
default_interval = "1s"

[color_scheme]
green = "#102030"
yellow = "38;2;40;50;60"
red = "10,20,30"

[[files]]
path = ""
command = "echo ok"
"""
    )
    try:
        config = ConfigLoader.load_config(config_path)
        assert config["color_scheme"] == "custom"
        assert Fore.GREEN == "\033[38;2;16;32;48m"
        assert Fore.YELLOW == "\033[38;2;40;50;60m"
        assert Fore.RED == "\033[38;2;10;20;30m"
    finally:
        os.unlink(config_path)


def test_custom_color_scheme_accepts_whitespace_in_components():
    """RGB values with spaces should be parsed."""
    config_path = _write_config(
        """
[color_scheme]
red = "10, 20, 30"

[[files]]
path = ""
command = "echo ok"
"""
    )
    try:
        ConfigLoader.load_config(config_path)
        assert Fore.RED == "\033[38;2;10;20;30m"
    finally:
        os.unlink(config_path)


def test_invalid_38_2_segment_falls_back_to_default_component():
    """Invalid 38;2 segment should not override the default palette."""
    default_red = Fore.RED
    config_path = _write_config(
        """
[color_scheme]
red = "38;2;999;999;999"

[[files]]
path = ""
command = "echo ok"
"""
    )
    try:
        ConfigLoader.load_config(config_path)
        assert Fore.RED == default_red
    finally:
        os.unlink(config_path)
