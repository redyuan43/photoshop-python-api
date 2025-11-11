#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick helper to read the currently active Photoshop tool via COM.

This relies on the core photoshop-python-api Application wrapper so we can
query `app.currentTool` without injecting hotkeys.
"""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_repo_on_path() -> None:
    """Make sure the project root is importable when running from /autogui."""
    repo_root = Path(__file__).resolve().parents[1]
    repo_str = str(repo_root)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)


def fetch_current_tool() -> str:
    """Return the Photoshop current tool name."""
    from photoshop import Session  # Imported lazily after adjusting sys.path

    with Session() as ps:
        return ps.app.currentTool


def main() -> None:
    print("=" * 60)
    print("Photoshop 工具检测器")
    print("=" * 60)

    ensure_repo_on_path()

    try:
        tool = fetch_current_tool()
    except Exception as exc:  # pylint: disable=broad-except
        print("[FAIL] 无法读取当前工具")
        print(f"原因: {exc}")
        print("\n排查建议:")
        print("  1. 确认 Photoshop 已经运行并打开任意文档")
        print("  2. 确认已安装 photoshop-python-api 依赖 (pip install .)")
        print("  3. 如仍失败，可尝试以管理员权限运行 PowerShell")
        sys.exit(1)

    print(f"[OK] 当前激活工具: {tool}")
    print("\n可直接在 Photoshop 内切换工具，再次运行以验证状态。")
    print("=" * 60)


if __name__ == "__main__":
    main()
