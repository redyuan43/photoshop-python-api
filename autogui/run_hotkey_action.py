#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wrapper to invoke photoshop_hotkey_best.py and emit JSON-friendly logs.

Usage examples:
  python run_hotkey_action.py --layer-down --json
  python run_hotkey_action.py --file-save
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="LLM-friendly runner for photoshop_hotkey_best.py",
        add_help=False,
    )
    parser.add_argument(
        "--json",
        dest="output_json",
        action="store_true",
        help="输出 JSON 结果（适合 LLM 消费）",
    )
    parser.add_argument(
        "--help",
        action="store_true",
        dest="show_help",
        help="显示底层脚本帮助",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args, passthrough = parser.parse_known_args()

    script_path = Path(__file__).with_name("photoshop_hotkey_best.py")
    cmd: List[str] = [sys.executable, str(script_path)]

    if args.show_help and "--help" not in passthrough:
        passthrough = ["--help"] + passthrough

    cmd.extend(passthrough)

    proc = subprocess.run(cmd, capture_output=True, text=True)

    if args.output_json:
        payload = {
            "status": "ok" if proc.returncode == 0 else "fail",
            "return_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "command": cmd,
            "passthrough": passthrough,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if proc.stdout:
            print(proc.stdout, end="")
        if proc.stderr:
            print(proc.stderr, file=sys.stderr, end="")

    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
