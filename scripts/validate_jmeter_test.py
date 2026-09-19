#!/usr/bin/env python3
"""Validate that a JMeter test plan exists and is readable before a long run."""

import os
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_jmeter_test.py <path-to-jmx-file>", file=sys.stderr)
        return 1

    test_file = Path(sys.argv[1]).resolve()
    if not test_file.exists():
        print(f"Missing JMeter test file: {test_file}")
        print("The selected test plan could not be found. Check the workflow input or the local test path.")
        return 1

    if not test_file.is_file():
        print(f"Not a file: {test_file}")
        return 1

    if test_file.suffix.lower() != ".jmx":
        print(f"Expected a .jmx plan, got: {test_file}")
        return 1

    print(f"JMeter plan validated: {test_file}")

    jmeter_bin = os.environ.get("JMETER_HOME")
    if jmeter_bin:
        runner = Path(jmeter_bin) / "bin" / ("jmeter.bat" if os.name == "nt" else "jmeter")
        if runner.exists():
            print(f"JMeter runner found: {runner}")
        else:
            print(f"JMETER_HOME is set but the runner was not found at {runner}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
