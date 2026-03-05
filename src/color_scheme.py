#!/usr/bin/env python3
"""Color scheme utilities for terminal output."""

import re

from colorama import Fore

DEFAULT_COLOR_SCHEME = "monokai"

_COLOR_SCHEMES: dict[str, dict[str, str]] = {
    # Monokai-inspired palette (24-bit color)
    "monokai": {
        "green": "\033[38;2;166;226;46m",
        "yellow": "\033[38;2;230;219;116m",
        "red": "\033[38;2;249;38;114m",
    },
    # Legacy/basic ANSI palette
    "classic": {
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
    },
}


class ColorScheme:
    """Handles configurable color schemes."""

    DEFAULT_COLOR_SCHEME = DEFAULT_COLOR_SCHEME
    _current_name = DEFAULT_COLOR_SCHEME

    @staticmethod
    def get_supported_schemes():
        """Return supported color scheme names.

        Returns:
            list: Sorted list of supported scheme names.
        """
        return sorted(_COLOR_SCHEMES.keys())

    @staticmethod
    def apply(color_scheme) -> tuple[str, bool]:
        """Apply the requested color scheme.

        Args:
            color_scheme: Scheme name string or custom palette table.

        Returns:
            tuple: (applied_scheme_name, used_default_fallback)
        """
        scheme_name, palette, used_default = ColorScheme._resolve_palette(color_scheme)
        ColorScheme._set_palette(palette)
        ColorScheme._current_name = scheme_name
        return scheme_name, used_default

    @staticmethod
    def reset_to_default():
        """Reset to the default color scheme."""
        ColorScheme.apply(DEFAULT_COLOR_SCHEME)

    @staticmethod
    def _resolve_palette(color_scheme) -> tuple[str, dict[str, str], bool]:
        """Resolve palette from config value."""
        default_palette = _COLOR_SCHEMES[DEFAULT_COLOR_SCHEME]

        if isinstance(color_scheme, dict):
            return "custom", ColorScheme._build_custom_palette(color_scheme), False

        if isinstance(color_scheme, str):
            normalized = color_scheme.strip().lower()
            if normalized in _COLOR_SCHEMES:
                return normalized, _COLOR_SCHEMES[normalized], False

        return DEFAULT_COLOR_SCHEME, default_palette, True

    @staticmethod
    def _build_custom_palette(config_palette: dict[str, str]) -> dict[str, str]:
        """Build a palette from user-provided color codes."""
        palette = _COLOR_SCHEMES[DEFAULT_COLOR_SCHEME].copy()
        for key in ("green", "yellow", "red"):
            code = ColorScheme._normalize_color_code(config_palette.get(key))
            if code:
                palette[key] = code
        return palette

    @staticmethod
    def _normalize_color_code(code):
        """Normalize various color code formats to ANSI escape codes."""
        if not isinstance(code, str):
            return None

        value = code.strip()
        if not value:
            return None

        # Already an escape sequence
        if value.startswith("\033[") or value.startswith("\x1b["):
            return value

        # Hex format (#RRGGBB or RRGGBB)
        hex_match = re.match(r"^#?([0-9a-fA-F]{6})$", value)
        if hex_match:
            hex_value = hex_match.group(1)
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
            return f"\033[38;2;{r};{g};{b}m"

        # RGB components separated by commas or semicolons (e.g., 255,0,0 or 255;0;0)
        rgb_parts = re.split(r"[;,]", value)
        stripped_parts = [part.strip() for part in rgb_parts]
        if len(stripped_parts) == 3 and all(part.isdigit() for part in stripped_parts):
            r, g, b = (int(part) for part in stripped_parts)
            if all(0 <= val <= 255 for val in (r, g, b)):
                return f"\033[38;2;{r};{g};{b}m"

        # Partial ANSI segment (e.g., 38;2;255;0;0)
        if value.startswith("38;2;"):
            parts = value.split(";")
            if (
                len(parts) == 5
                and parts[0] == "38"
                and parts[1] == "2"
                and all(component.strip().isdigit() for component in parts[2:])
            ):
                r, g, b = (int(component) for component in parts[2:])
                if all(0 <= val <= 255 for val in (r, g, b)):
                    return f"\033[38;2;{r};{g};{b}m"
            return None

        return None

    @staticmethod
    def _set_palette(palette: dict[str, str]):
        """Apply palette values to colorama Fore."""
        Fore.GREEN = palette.get("green", _COLOR_SCHEMES[DEFAULT_COLOR_SCHEME]["green"])
        Fore.YELLOW = palette.get("yellow", _COLOR_SCHEMES[DEFAULT_COLOR_SCHEME]["yellow"])
        Fore.RED = palette.get("red", _COLOR_SCHEMES[DEFAULT_COLOR_SCHEME]["red"])


# Initialize with default palette on import
ColorScheme.reset_to_default()
