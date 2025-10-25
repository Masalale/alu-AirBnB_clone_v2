#!/usr/bin/python3
"""Basic tests for the HBNB console.

These are minimal smoke tests to ensure the console module imports and
exposes the expected class and help text. They avoid executing commands
that would exit the test process.
"""
import io
import sys
import unittest

from console import HBNBCommand


class TestConsoleBasic(unittest.TestCase):
    """Small set of non-invasive tests for console behavior."""

    def test_class_exists(self):
        """HBNBCommand should be importable and be a class."""
        self.assertTrue(hasattr(HBNBCommand, 'cmdloop'))

    def test_help_quit_outputs(self):
        """help_quit should print help text to stdout."""
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.help_quit()
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue()
        self.assertIn('Exits the program', out)

    def test_help_EOF_outputs(self):
        """help_EOF should print help text to stdout."""
        cons = HBNBCommand()
        captured = io.StringIO()
        sys_stdout = sys.stdout
        try:
            sys.stdout = captured
            cons.help_EOF()
        finally:
            sys.stdout = sys_stdout
        out = captured.getvalue()
        self.assertIn('Exits the program', out)


if __name__ == '__main__':
    unittest.main()
