#!/usr/bin/python3
"""Helper script to run console commands and print results."""
import io
import sys
from console import HBNBCommand


def run_console_cmd(cmd):
    """Run a single console command and return the output."""
    cons = HBNBCommand()
    captured = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured
        cons.onecmd(cmd)
    finally:
        sys.stdout = sys_stdout
    return captured.getvalue().strip()


def main():
    """Main entry point for fake console."""
    if len(sys.argv) > 1:
        # Run all arguments as a single console command
        cmd = ' '.join(sys.argv[1:])
        result = run_console_cmd(cmd)
        if result:
            print(result)
    else:
        print("Usage: create_fake_console.py <console_command>")
        print("Example: create_fake_console.py create State name=\"California\"")


if __name__ == '__main__':
    main()
