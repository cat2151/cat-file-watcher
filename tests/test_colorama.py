#!/usr/bin/env python3
"""
Tests for colorama color support in timestamp printing
"""

import os
import re
import sys
from io import StringIO

from colorama import Fore, Style

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from timestamp_printer import TimestampPrinter


class TestColoramaSupport:
    """Test cases for colorama color support."""

    def test_print_with_no_color(self):
        """Test that printing without color works as before."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Test message")

            output = captured_output.getvalue()
            assert "Test message" in output
            assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_print_with_green_color(self):
        """Test that printing with green color works."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Success message", Fore.GREEN)

            output = captured_output.getvalue()
            assert "Success message" in output
            # Colorama codes should be present
            assert Fore.GREEN in output or "\x1b[32m" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_print_with_red_color(self):
        """Test that printing with red color works."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Error message", Fore.RED)

            output = captured_output.getvalue()
            assert "Error message" in output
            # Colorama codes should be present
            assert Fore.RED in output or "\x1b[31m" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_print_with_yellow_color(self):
        """Test that printing with yellow color works."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Warning message", Fore.YELLOW)

            output = captured_output.getvalue()
            assert "Warning message" in output
            # Colorama codes should be present
            assert Fore.YELLOW in output or "\x1b[33m" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_print_with_dim_style(self):
        """Test that printing with dim style works."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(True)
            TimestampPrinter.print("Dimmed message", Style.DIM)

            output = captured_output.getvalue()
            assert "Dimmed message" in output
            # Colorama codes should be present
            assert Style.DIM in output or "\x1b[2m" in output
        finally:
            sys.stdout = sys.__stdout__

    def test_print_with_color_and_timestamp_disabled(self):
        """Test that color works even when timestamp is disabled."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(False)
            TimestampPrinter.print("Colored message", Fore.BLUE)

            output = captured_output.getvalue()
            assert "Colored message" in output
            # Should not have timestamp
            assert not re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", output)
            # Should have color
            assert Fore.BLUE in output or "\x1b[34m" in output
        finally:
            sys.stdout = sys.__stdout__
            TimestampPrinter.set_enable_timestamp(True)

    def test_multiple_colored_messages(self):
        """Test printing multiple messages with different colors."""
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            TimestampPrinter.set_enable_timestamp(False)
            TimestampPrinter.print("Green message", Fore.GREEN)
            TimestampPrinter.print("Red message", Fore.RED)
            TimestampPrinter.print("Yellow message", Fore.YELLOW)

            output = captured_output.getvalue()
            assert "Green message" in output
            assert "Red message" in output
            assert "Yellow message" in output
        finally:
            sys.stdout = sys.__stdout__
            TimestampPrinter.set_enable_timestamp(True)
