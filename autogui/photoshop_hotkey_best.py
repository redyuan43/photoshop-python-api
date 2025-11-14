#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Photoshop hotkey automation helper (English version)."""

from __future__ import annotations

import argparse
import sys
import time
from typing import Callable, Dict, List, Optional

import pyautogui
import win32con
import win32gui


DEFAULT_WINDOW_KEYWORD = "Photoshop"

TOOL_MAP = {
    "move": {"key": "v", "name": "Move Tool"},
    "marquee": {"key": "m", "name": "Marquee Tool"},
    "lasso": {"key": "l", "name": "Lasso Tool"},
    "magic_wand": {"key": "w", "name": "Magic/Quick/Object Selection"},
    "crop": {"key": "c", "name": "Crop Tool"},
    "eyedropper": {"key": "i", "name": "Eyedropper Tool"},
    "spot_heal": {"key": "j", "name": "Spot/Healing Brush"},
    "clone_stamp": {"key": "s", "name": "Clone Stamp"},
    "history_brush": {"key": "y", "name": "History Brush"},
    "eraser": {"key": "e", "name": "Eraser"},
    "paint_bucket": {"key": "g", "name": "Paint Bucket / Gradient"},
    "dodge": {"key": "o", "name": "Dodge / Burn"},
    "pen": {"key": "p", "name": "Pen Tool"},
    "type": {"key": "t", "name": "Type Tool"},
    "path_select": {"key": "a", "name": "Path / Direct Selection"},
    "shape": {"key": "u", "name": "Shape Tools"},
    "hand": {"key": "h", "name": "Hand Tool"},
    "rotate_view": {"key": "r", "name": "Rotate View"},
    "zoom": {"key": "z", "name": "Zoom"},
}


def _enum_photoshop_windows(keyword: str) -> List[int]:
    matches: List[int] = []

    def _callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd)
        cls = win32gui.GetClassName(hwnd)
        if keyword.lower() in title.lower() or "photoshop" in cls.lower():
            matches.append(hwnd)
        return True

    win32gui.EnumWindows(_callback, None)
    return matches


def activate_photoshop_window(keyword: str) -> Optional[int]:
    print("[INFO] Activating Photoshop window...")
    candidates = _enum_photoshop_windows(keyword)
    if not candidates:
        print(f"[FAIL] No Photoshop window matches '{keyword}'.")
        return None
    hwnd = candidates[0]
    try:
        placement = win32gui.GetWindowPlacement(hwnd)
        show_cmd = placement[1] if placement else win32con.SW_RESTORE
        if show_cmd == win32con.SW_SHOWMAXIMIZED:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.2)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.2)
        print(f"[OK] Foreground window: {win32gui.GetWindowText(hwnd)}")
        return hwnd
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[FAIL] Unable to focus Photoshop: {exc}")
        return None


def _sleep():
    time.sleep(0.25)


def send_hotkeys() -> bool:
    print("[INFO] Resetting workspace via Alt+W, K, R")
    try:
        pyautogui.hotkey('alt', 'w')
        _sleep()
        pyautogui.press('k')
        _sleep()
        pyautogui.press('r')
        _sleep()
        print("[OK] Reset keys sent")
        return True
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[FAIL] Could not send reset keys: {exc}")
        return False


def _press_sequence(sequence: List[List[str]]) -> bool:
    try:
        for combo in sequence:
            pyautogui.hotkey(*combo)
            _sleep()
        print("[OK] Hotkeys sent")
        return True
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[FAIL] Hotkey sequence failed: {exc}")
        return False


def send_layer_move_hotkeys(direction: str) -> bool:
    if direction == 'both':
        sequence = [['ctrl', '['], ['ctrl', ']']]
    elif direction == 'up':
        sequence = [['ctrl', ']']]
    else:
        sequence = [['ctrl', '[']]
    print(f"[INFO] Moving layer: {direction}")
    return _press_sequence(sequence)


def send_selection_move_hotkey(direction: str) -> bool:
    mapping = {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'}
    key = mapping.get(direction, 'up')
    print(f"[INFO] Nudging selection {direction}")
    return _press_sequence([[ 'ctrl', key ]])


def send_simple_hotkey(*keys: str) -> bool:
    return _press_sequence([list(keys)])


def send_tool_hotkey(tool_id: str, cycle: bool = False) -> bool:
    tool = TOOL_MAP.get(tool_id)
    if not tool:
        print(f"[FAIL] Unknown tool: {tool_id}")
        return False
    print(f"[INFO] Switching to {tool['name']}")
    try:
        if cycle:
            pyautogui.hotkey('shift', tool['key'])
        else:
            pyautogui.press(tool['key'])
        _sleep()
        print("[OK] Tool hotkey sent")
        return True
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[FAIL] Unable to switch tool: {exc}")
        return False


HOTKEY_ACTIONS: Dict[str, Callable[[], bool]] = {
    'reset': send_hotkeys,
    'layer_move': lambda: send_layer_move_hotkeys('both'),
    'layer_up': lambda: send_layer_move_hotkeys('up'),
    'layer_down': lambda: send_layer_move_hotkeys('down'),
    'selection_up': lambda: send_selection_move_hotkey('up'),
    'selection_down': lambda: send_selection_move_hotkey('down'),
    'selection_left': lambda: send_selection_move_hotkey('left'),
    'selection_right': lambda: send_selection_move_hotkey('right'),
    'select_all': lambda: send_simple_hotkey('ctrl', 'a'),
    'deselect': lambda: send_simple_hotkey('ctrl', 'd'),
    'invert': lambda: send_simple_hotkey('ctrl', 'shift', 'i'),
    'duplicate': lambda: send_simple_hotkey('ctrl', 'j'),
    'file_new': lambda: send_simple_hotkey('ctrl', 'n'),
    'file_open': lambda: send_simple_hotkey('ctrl', 'o'),
    'file_save': lambda: send_simple_hotkey('ctrl', 's'),
    'file_save_as': lambda: send_simple_hotkey('ctrl', 'shift', 's'),
    'export_as': lambda: send_simple_hotkey('ctrl', 'alt', 'shift', 'w'),
    'file_close': lambda: send_simple_hotkey('ctrl', 'w'),
    'file_close_all': lambda: send_simple_hotkey('ctrl', 'alt', 'w'),
    'undo': lambda: send_simple_hotkey('ctrl', 'z'),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Photoshop hotkey automation tool (English)')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--layer-move', action='store_true', help='Move layer up then down (Ctrl+{ / Ctrl+})')
    group.add_argument('--layer-up', action='store_true', help='Move layer up (Ctrl+})')
    group.add_argument('--layer-down', action='store_true', help='Move layer down (Ctrl+{)')

    group.add_argument('--selection-up', action='store_true', help='Nudge selection up (Ctrl+Arrow)')
    group.add_argument('--selection-down', action='store_true', help='Nudge selection down (Ctrl+Arrow)')
    group.add_argument('--selection-left', action='store_true', help='Nudge selection left (Ctrl+Arrow)')
    group.add_argument('--selection-right', action='store_true', help='Nudge selection right (Ctrl+Arrow)')

    group.add_argument('--select-all', action='store_true', help='Select all (Ctrl+A)')
    group.add_argument('--deselect', action='store_true', help='Deselect (Ctrl+D)')
    group.add_argument('--invert', action='store_true', help='Invert selection (Ctrl+Shift+I)')
    group.add_argument('--duplicate', action='store_true', help='Duplicate layer (Ctrl+J)')

    group.add_argument('--tool', choices=sorted(TOOL_MAP.keys()), help='Switch to specific toolbar tool')
    group.add_argument('--tool-cycle', choices=sorted(TOOL_MAP.keys()), help='Cycle tool group (Shift+Key)')

    group.add_argument('--file-new', action='store_true', help='New document (Ctrl+N)')
    group.add_argument('--file-open', action='store_true', help='Open document (Ctrl+O)')
    group.add_argument('--file-save', action='store_true', help='Save document (Ctrl+S)')
    group.add_argument('--file-save-as', action='store_true', help='Save As (Ctrl+Shift+S)')
    group.add_argument('--export-as', action='store_true', help='Export As (Ctrl+Alt+Shift+W)')
    group.add_argument('--file-close', action='store_true', help='Close current document (Ctrl+W)')
    group.add_argument('--file-close-all', action='store_true', help='Close all documents (Ctrl+Alt+W)')
    group.add_argument('--undo', action='store_true', help='Undo (Ctrl+Z)')

    parser.add_argument('--taskbar-name', default=DEFAULT_WINDOW_KEYWORD, help='Substring of Photoshop window title (default: Photoshop)')
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not activate_photoshop_window(args.taskbar_name):
        sys.exit(1)

    action = None
    for key in HOTKEY_ACTIONS:
        if getattr(args, key.replace('-', '_'), False):  # fallback
            action = key
            break

    if args.layer_move:
        action = 'layer_move'
    elif args.layer_up:
        action = 'layer_up'
    elif args.layer_down:
        action = 'layer_down'
    elif args.selection_up:
        action = 'selection_up'
    elif args.selection_down:
        action = 'selection_down'
    elif args.selection_left:
        action = 'selection_left'
    elif args.selection_right:
        action = 'selection_right'
    elif args.select_all:
        action = 'select_all'
    elif args.deselect:
        action = 'deselect'
    elif args.invert:
        action = 'invert'
    elif args.duplicate:
        action = 'duplicate'
    elif args.file_new:
        action = 'file_new'
    elif args.file_open:
        action = 'file_open'
    elif args.file_save:
        action = 'file_save'
    elif args.file_save_as:
        action = 'file_save_as'
    elif args.export_as:
        action = 'export_as'
    elif args.file_close:
        action = 'file_close'
    elif args.file_close_all:
        action = 'file_close_all'
    elif args.undo:
        action = 'undo'

    if args.tool:
        if not send_tool_hotkey(args.tool, cycle=False):
            sys.exit(1)
        print("[DONE] Tool switch request finished")
        return
    if args.tool_cycle:
        if not send_tool_hotkey(args.tool_cycle, cycle=True):
            sys.exit(1)
        print("[DONE] Tool cycle request finished")
        return

    if not action:
        parser.print_help()
        sys.exit(1)

    handler = HOTKEY_ACTIONS[action]
    if not handler():
        sys.exit(1)
    print("[DONE] Hotkey command executed")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        sys.exit(0)
