#!/usr/bin/env python
"""
Activate Photoshop via the taskbar button and capture its window.

Usage:
    python screenshot_photoshop.py --out shots/ps.png
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import uiautomation as auto
import win32gui
from pywinauto import Application


def _get_taskbar_control():
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if hwnd:
        return auto.ControlFromHandle(hwnd)
    return auto.WindowControl(ClassName="Shell_TrayWnd")


def activate_photoshop(taskbar_name: str) -> None:
    """Click the Photoshop taskbar button."""
    taskbar = _get_taskbar_control()
    if not taskbar or not taskbar.Exists(0, 0):
        raise SystemExit("[FAIL] Taskbar not found.")

    bridge = taskbar.PaneControl(ClassName="Windows.UI.Composition.DesktopWindowContentBridge")
    if not bridge.Exists(0, 0):
        raise SystemExit("[FAIL] Taskbar DesktopWindowXamlSource pane not found.")

    button = bridge.ButtonControl(Name=taskbar_name)
    if not button.Exists(0, 0):
        raise SystemExit(f"[FAIL] Taskbar button '{taskbar_name}' not found.")

    button.Click()
    time.sleep(0.5)  # Give Photoshop a moment to come forward


def capture_foreground_window(out_path: Path) -> Path:
    """Capture whatever window is currently foreground."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        raise SystemExit("[FAIL] No foreground window detected after activation.")

    app = Application(backend="uia").connect(handle=hwnd, timeout=1)
    window = app.window(handle=hwnd)
    image = window.capture_as_image()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Activate Photoshop and capture its window.")
    parser.add_argument("--out", default="photoshop_capture.png", help="Output PNG path")
    parser.add_argument(
        "--taskbar-name",
        default="Adobe Photoshop 2025 - 1 running window",
        help="Exact taskbar button name to click before capturing",
    )
    args = parser.parse_args()

    activate_photoshop(args.taskbar_name)
    out_path = capture_foreground_window(Path(args.out))
    print(f"[OK] Saved screenshot to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
