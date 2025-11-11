#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traverse all Photoshop toolbar hotkeys via photoshop_hotkey_best.py and report the resulting tool names.

This script:
  1. Iterates through every TOOL_MAP entry defined in photoshop_hotkey_best.py
  2. Runs `photoshop_hotkey_best.py --tool <id>` (and optionally `--tool-cycle <id>`)
  3. Invokes get_current_tool.py to capture the tool identifier from Photoshop
  4. Prints a summary table and JSON payload for downstream automation

Usage:
  python enumerate_tools.py
  python enumerate_tools.py --include-cycle
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
HOTKEY_SCRIPT = REPO_ROOT / "photoshop_hotkey_best.py"
GET_TOOL_SCRIPT = REPO_ROOT / "get_current_tool.py"


def run_command(cmd, timeout=30):
    """Run a command and capture stdout/stderr."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, "", f"Command timed out: {exc}"


def get_tool_map():
    """Import TOOL_MAP from photoshop_hotkey_best.py via exec."""
    namespace = {}
    script_text = HOTKEY_SCRIPT.read_text(encoding="utf-8")
    exec(script_text, namespace)  # pylint: disable=exec-used
    return namespace.get("TOOL_MAP", {})


def call_hotkey(tool_id, cycle=False):
    """Call photoshop_hotkey_best.py with --tool or --tool-cycle."""
    args = [sys.executable, str(HOTKEY_SCRIPT)]
    if cycle:
        args.extend(["--tool-cycle", tool_id])
    else:
        args.extend(["--tool", tool_id])
    return run_command(args)


def read_current_tool():
    """Run get_current_tool.py and extract the tool name from stdout."""
    code, out, err = run_command([sys.executable, str(GET_TOOL_SCRIPT)])
    current_tool = None
    for line in out.splitlines():
        if "当前激活工具" in line or "Current tool" in line:
            current_tool = line.split(":")[-1].strip()
            break
    return code, current_tool, out, err


def enumerate_tools(include_cycle=True):
    """Iterate tools and gather mappings."""
    tool_map = get_tool_map()
    results = []

    if not tool_map:
        raise RuntimeError("无法从 photoshop_hotkey_best.py 读取 TOOL_MAP")

    for tool_id in sorted(tool_map):
        entry = {"tool_id": tool_id, "mode": "primary", "variant_index": 0}
        code, out, err = call_hotkey(tool_id, cycle=False)
        entry["hotkey_rc"] = code
        entry["hotkey_stdout"] = out
        entry["hotkey_stderr"] = err
        tool_code, tool_name, tool_stdout, tool_stderr = read_current_tool()
        entry["current_tool_rc"] = tool_code
        entry["current_tool_name"] = tool_name
        entry["current_tool_stdout"] = tool_stdout
        entry["current_tool_stderr"] = tool_stderr
        results.append(entry)

        seen = set()
        if tool_name:
            seen.add(tool_name)

        if include_cycle:
            for idx in range(1, 12):  # arbitrary upper bound to prevent infinite loop
                cycle_entry = {"tool_id": tool_id, "mode": "cycle", "variant_index": idx}
                code, out, err = call_hotkey(tool_id, cycle=True)
                cycle_entry["hotkey_rc"] = code
                cycle_entry["hotkey_stdout"] = out
                cycle_entry["hotkey_stderr"] = err
                tool_code, tool_name, tool_stdout, tool_stderr = read_current_tool()
                cycle_entry["current_tool_rc"] = tool_code
                cycle_entry["current_tool_name"] = tool_name
                cycle_entry["current_tool_stdout"] = tool_stdout
                cycle_entry["current_tool_stderr"] = tool_stderr
                results.append(cycle_entry)

                if tool_code != 0 or not tool_name:
                    break
                if tool_name in seen:
                    break
                seen.add(tool_name)

    return results


def main():
    parser = argparse.ArgumentParser(description="Enumerate Photoshop tools via CLI hotkeys")
    parser.add_argument("--primary-only", action="store_true", help="仅遍历主快捷键，不发送 Shift+字母")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    try:
        records = enumerate_tools(include_cycle=not args.primary_only)
    except Exception as exc:
        print(f"[FAIL] 枚举失败: {exc}")
        sys.exit(1)

    unique_tools = sorted({rec["current_tool_name"] for rec in records if rec.get("current_tool_name")})

    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        for rec in records:
            print("=" * 40)
            print(f"工具 ID: {rec['tool_id']}  模式: {rec['mode']}")
            print(f"  Hotkey 返回码: {rec['hotkey_rc']}")
            print(f"  当前工具返回码: {rec['current_tool_rc']}")
            print(f"  当前工具名称: {rec['current_tool_name']}")
    print("\n=== unique currentTool 名称 ===")
    for name in unique_tools:
        print(f"  - {name}")
    print(f"\n[OK] 完成，统计 {len(records)} 条记录，覆盖 {len(unique_tools)} 种 currentTool。")


if __name__ == "__main__":
    main()
