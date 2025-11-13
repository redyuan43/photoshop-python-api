#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Photoshop 快捷键自动化工具 - v3.0
功能: 使用pywinauto激活窗口并发送各种快捷键
特点: 稳定、可靠、功能完整

支持的功能:

【基本功能】
  无参数        - 复位基本功能 (Alt+W, K, R)

【图层操作】
  --layer-move  - 上下移动图层 (Ctrl+{, Ctrl+})
  --layer-up    - 图层向上移动 (Ctrl+})
  --layer-down  - 图层向下移动 (Ctrl+{)

【选区操作】
  --selection-up     - 选区向上移动 (Ctrl+↑)
  --selection-down   - 选区向下移动 (Ctrl+↓)
  --selection-left   - 选区向左移动 (Ctrl+←)
  --selection-right  - 选区向右移动 (Ctrl+→)

【选区管理】
  --select-all  - 全选图层 (Ctrl+A)
  --deselect    - 取消选区 (Ctrl+D)
  --invert      - 反选 (Ctrl+Shift+I)
  --duplicate   - 复制图层 (Ctrl+J)
"""

import pyautogui
import pywinauto
from pywinauto.application import Application
import time
import sys
import argparse
from typing import Optional

import uiautomation as auto
import win32gui

DEFAULT_TASKBAR_NAME = "Adobe Photoshop 2025 - 1 running window"


TOOL_MAP = {
    'move': {'key': 'v', 'name': '移动工具 (Move Tool)'},
    'marquee': {'key': 'm', 'name': '矩形/椭圆选框工具 (Marquee)'},
    'lasso': {'key': 'l', 'name': '套索工具 (Lasso)'},
    'magic_wand': {'key': 'w', 'name': '魔棒/快速选择工具 (Magic Wand)'},
    'crop': {'key': 'c', 'name': '裁剪工具 (Crop)'},
    'eyedropper': {'key': 'i', 'name': '吸管工具 (Eyedropper)'},
    'spot_heal': {'key': 'j', 'name': '污点修复画笔工具 (Spot Healing Brush)'},
    'clone_stamp': {'key': 's', 'name': '仿制图章工具 (Clone Stamp)'},
    'history_brush': {'key': 'y', 'name': '历史记录画笔工具 (History Brush)'},
    'eraser': {'key': 'e', 'name': '橡皮擦工具 (Eraser)'},
    'paint_bucket': {'key': 'g', 'name': '油漆桶/渐变工具 (Paint Bucket/Gradient)'},
    'dodge': {'key': 'o', 'name': '减淡/加深工具 (Dodge/Burn)'},
    'pen': {'key': 'p', 'name': '钢笔工具 (Pen)'},
    'type': {'key': 't', 'name': '横排文字工具 (Type)'},
    'path_select': {'key': 'a', 'name': '路径/直接选择工具 (Path Select)'},
    'shape': {'key': 'u', 'name': '矩形/椭圆工具 (Shape)'},
    'hand': {'key': 'h', 'name': '抓手工具 (Hand)'},
    'rotate_view': {'key': 'r', 'name': '旋转视图工具 (Rotate View)'},
    'zoom': {'key': 'z', 'name': '缩放工具 (Zoom)'},
}

def _get_taskbar_control():
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if hwnd:
        return auto.ControlFromHandle(hwnd)
    return auto.WindowControl(ClassName="Shell_TrayWnd")


def _activate_photoshop_via_taskbar(button_name: str) -> Optional[int]:
    taskbar = _get_taskbar_control()
    if not taskbar or not taskbar.Exists(0, 0):
        print("[FAIL] Taskbar not found.")
        return None

    bridge = taskbar.PaneControl(ClassName="Windows.UI.Composition.DesktopWindowContentBridge")
    if not bridge.Exists(0, 0):
        bridge = taskbar

    button = bridge.ButtonControl(Name=button_name)
    if not button.Exists(0, 0):
        button = bridge.ButtonControl(searchDepth=10, SubName="Photoshop")
        if not button.Exists(0, 0):
            print(f"[FAIL] Taskbar button '{button_name}' not found.")
            return None

    button.Click()
    time.sleep(0.5)
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        print("[FAIL] 激活失败，未检测到前台窗口。")
        return None
    return hwnd


def find_photoshop_window(taskbar_name: str):
    """通过任务栏按钮激活 Photoshop 窗口。"""
    print("正在通过任务栏激活 Photoshop 窗口...")
    hwnd = _activate_photoshop_via_taskbar(taskbar_name)
    if not hwnd:
        return None, None
    try:
        app = Application(backend='uia').connect(handle=hwnd, timeout=2)
        win = app.window(handle=hwnd)
        print(f"[OK] 激活窗口: {win.window_text()}")
        return app, win
    except Exception as exc:
        print(f"[FAIL] 无法连接 Photoshop 窗口: {exc}")
        return None, None

def activate_window(app, win):
    """使用 pywinauto 再次确保窗口处于焦点/最大化状态。"""
    print("\n正在激活窗口...")
    try:
        win.set_focus()
        time.sleep(0.2)
        print("[OK] 已设置焦点")
        should_maximize = True
        try:
            if hasattr(win, "is_maximized"):
                should_maximize = not win.is_maximized()
        except Exception:
            should_maximize = True

        if should_maximize:
            try:
                win.maximize()
                time.sleep(0.2)
                print("[OK] 窗口已最大化")
            except Exception as max_err:
                print(f"[INFO] 最大化失败，继续执行: {max_err}")
        else:
            print("[OK] 窗口已处于最大化状态")

        print("[OK] 窗口激活完成")
        return True
    except Exception as e:
        print(f"[FAIL] 激活失败: {e}")
        return False

def send_tool_hotkey(tool_id: str, cycle: bool = False):
    """切换 Photoshop 工具栏工具."""
    tool = TOOL_MAP.get(tool_id)
    if not tool:
        print(f"[FAIL] 未知工具: {tool_id}")
        return False

    action_desc = "Shift+" if cycle else ""
    action_desc += tool['key'].upper()
    print("\n开始切换工具...")
    print(f"  {tool['name']}  ({action_desc})")
    print("\n请观察工具栏变化...")

    try:
        if cycle:
            pyautogui.hotkey('shift', tool['key'])
        else:
            pyautogui.press(tool['key'])
        time.sleep(0.2)
        print("\n[OK] 工具切换完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_hotkeys():
    """发送快捷键序列: Alt+W, K, R"""
    print("\n开始发送快捷键...")
    print("  1. Alt + W")
    print("  2. K")
    print("  3. R")
    print("\n请观察窗口响应...")

    try:
        # Alt+W
        print("\n发送 Alt+W")
        pyautogui.hotkey('alt', 'w')
        time.sleep(0.5)

        # K
        print("发送 K")
        pyautogui.press('k')
        time.sleep(0.5)

        # R
        print("发送 R")
        pyautogui.press('r')
        time.sleep(0.5)

        print("\n[OK] 快捷键发送完成")
        return True

    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_layer_move_hotkeys(direction='both'):
    """发送上下移动图层的快捷键"""
    print("\n开始发送图层移动快捷键...")

    if direction == 'down' or direction == 'both':
        print("  Ctrl + {  - 向下移动图层")
    if direction == 'up' or direction == 'both':
        print("  Ctrl + }  - 向上移动图层")

    print("\n请观察窗口响应...")

    try:
        if direction == 'down' or direction == 'both':
            print("\n发送 Ctrl+{ (向下移动图层)")
            pyautogui.hotkey('ctrl', '[')
            time.sleep(0.5)

        if direction == 'up' or direction == 'both':
            print("发送 Ctrl+} (向上移动图层)")
            pyautogui.hotkey('ctrl', ']')
            time.sleep(0.5)

        print("\n[OK] 快捷键发送完成")
        return True

    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_selection_move_hotkey(direction='up'):
    """发送移动选区快捷键: Ctrl+方向键"""
    print(f"\n开始发送选区移动快捷键...")
    print(f"  Ctrl + {direction}  - 选区向{direction}移动")
    print("\n请观察窗口响应...")

    direction_map = {
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right'
    }

    try:
        direction_key = direction_map.get(direction, 'up')
        print(f"\n发送 Ctrl+{direction} (选区向{direction}移动)")
        pyautogui.hotkey('ctrl', direction_key)
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_select_all_hotkey():
    """发送全选图层快捷键: Ctrl+A"""
    print("\n开始发送全选快捷键...")
    print("  Ctrl + A  - 全选图层")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+A (全选图层)")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_deselect_hotkey():
    """发送取消选区快捷键: Ctrl+D"""
    print("\n开始发送取消选区快捷键...")
    print("  Ctrl + D  - 取消选区")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+D (取消选区)")
        pyautogui.hotkey('ctrl', 'd')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_invert_hotkey():
    """发送反选快捷键: Ctrl+Shift+I"""
    print("\n开始发送反选快捷键...")
    print("  Ctrl + Shift + I  - 反选")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Shift+I (反选)")
        pyautogui.hotkey('ctrl', 'shift', 'i')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_duplicate_layer_hotkey():
    """发送复制图层快捷键: Ctrl+J"""
    print("\n开始发送复制图层快捷键...")
    print("  Ctrl + J  - 复制图层")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+J (复制图层)")
        pyautogui.hotkey('ctrl', 'j')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_new_file_hotkey():
    """发送新建文档快捷键: Ctrl+N"""
    print("\n开始发送新建文档快捷键...")
    print("  Ctrl + N  - 新建文档")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+N (新建文档)")
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_open_file_hotkey():
    """发送打开文档快捷键: Ctrl+O"""
    print("\n开始发送打开文档快捷键...")
    print("  Ctrl + O  - 打开文件")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+O (打开文件)")
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_save_file_hotkey():
    """发送保存文档快捷键: Ctrl+S"""
    print("\n开始发送保存文档快捷键...")
    print("  Ctrl + S  - 保存文件")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+S (保存文件)")
        pyautogui.hotkey('ctrl', 's')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_save_as_hotkey():
    """发送另存为快捷键: Ctrl+Shift+S"""
    print("\n开始发送另存为快捷键...")
    print("  Ctrl + Shift + S  - 另存为")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Shift+S (另存为)")
        pyautogui.hotkey('ctrl', 'shift', 's')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_export_as_hotkey():
    """发送导出快捷键: Ctrl+Alt+Shift+W"""
    print("\n开始发送导出快捷键...")
    print("  Ctrl + Alt + Shift + W  - 导出为...")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Alt+Shift+W (导出为...)")
        pyautogui.hotkey('ctrl', 'alt', 'shift', 'w')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_close_file_hotkey():
    """发送关闭文档快捷键: Ctrl+W"""
    print("\n开始发送关闭文档快捷键...")
    print("  Ctrl + W  - 关闭当前文档")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+W (关闭当前文档)")
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_close_all_hotkey():
    """发送关闭全部快捷键: Ctrl+Alt+W"""
    print("\n开始发送关闭全部快捷键...")
    print("  Ctrl + Alt + W  - 关闭所有文档")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Alt+W (关闭所有文档)")
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def send_undo_hotkey():
    """发送撤销快捷键: Ctrl+Z"""
    print("\n开始发送撤销快捷键...")
    print("  Ctrl + Z  - 撤销上一步操作")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Z (撤销上一步操作)")
        pyautogui.hotkey('ctrl', 'z')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='Photoshop 快捷键自动化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:

【基本功能】
  python photoshop_hotkey_best.py.py                        # 复位基本功能

【图层操作】
  python photoshop_hotkey_best.py.py --layer-move           # 上下移动图层
  python photoshop_hotkey_best.py.py --layer-up             # 图层向上移动
  python photoshop_hotkey_best.py.py --layer-down           # 图层向下移动

【选区操作】
  python photoshop_hotkey_best.py.py --selection-up         # 选区向上移动
  python photoshop_hotkey_best.py.py --selection-down       # 选区向下移动
  python photoshop_hotkey_best.py.py --selection-left       # 选区向左移动
  python photoshop_hotkey_best.py.py --selection-right      # 选区向右移动

【选区管理】
  python photoshop_hotkey_best.py.py --select-all           # 全选图层
  python photoshop_hotkey_best.py.py --deselect             # 取消选区
  python photoshop_hotkey_best.py.py --invert               # 反选
  python photoshop_hotkey_best.py.py --duplicate            # 复制图层

【文件操作】
  python photoshop_hotkey_best.py.py --file-new             # 新建文档
  python photoshop_hotkey_best.py.py --file-open            # 打开文档
  python photoshop_hotkey_best.py.py --file-save            # 保存文档
  python photoshop_hotkey_best.py.py --file-save-as         # 另存为
  python photoshop_hotkey_best.py.py --export-as            # 导出文件
  python photoshop_hotkey_best.py.py --file-close           # 关闭当前文档
  python photoshop_hotkey_best.py.py --file-close-all       # 关闭所有文档
  python photoshop_hotkey_best.py.py --undo                 # 撤销上一步
        """
    )

    group = parser.add_mutually_exclusive_group()

    # 图层操作
    group.add_argument('--layer-move', action='store_true',
                      help='上下移动图层 (Ctrl+{, Ctrl+})')
    group.add_argument('--layer-up', action='store_true',
                      help='图层向上移动 (Ctrl+})')
    group.add_argument('--layer-down', action='store_true',
                      help='图层向下移动 (Ctrl+{)')

    # 选区操作
    group.add_argument('--selection-up', action='store_true',
                      help='选区向上移动 (Ctrl+↑)')
    group.add_argument('--selection-down', action='store_true',
                      help='选区向下移动 (Ctrl+↓)')
    group.add_argument('--selection-left', action='store_true',
                      help='选区向左移动 (Ctrl+←)')
    group.add_argument('--selection-right', action='store_true',
                      help='选区向右移动 (Ctrl+→)')

    # 选区管理
    group.add_argument('--select-all', action='store_true',
                      help='全选图层 (Ctrl+A)')
    group.add_argument('--deselect', action='store_true',
                      help='取消选区 (Ctrl+D)')
    group.add_argument('--invert', action='store_true',
                      help='反选 (Ctrl+Shift+I)')
    group.add_argument('--duplicate', action='store_true',
                      help='复制图层 (Ctrl+J)')

    # 工具切换
    group.add_argument('--tool', choices=sorted(TOOL_MAP.keys()),
                      help='切换到指定工具 (例如 move/marquee/pen 等)')
    group.add_argument('--tool-cycle', choices=sorted(TOOL_MAP.keys()),
                      help='使用 Shift+字母 循环工具组内选项')

    # 文件操作
    group.add_argument('--file-new', action='store_true',
                      help='新建文档 (Ctrl+N)')
    group.add_argument('--file-open', action='store_true',
                      help='打开文档 (Ctrl+O)')
    group.add_argument('--file-save', action='store_true',
                      help='保存文档 (Ctrl+S)')
    group.add_argument('--file-save-as', action='store_true',
                      help='另存为 (Ctrl+Shift+S)')
    group.add_argument('--export-as', action='store_true',
                      help='导出文件 (Ctrl+Alt+Shift+W)')
    group.add_argument('--file-close', action='store_true',
                      help='关闭当前文档 (Ctrl+W)')
    group.add_argument('--file-close-all', action='store_true',
                      help='关闭所有文档 (Ctrl+Alt+W)')
    group.add_argument('--undo', action='store_true',
                      help='撤销上一步 (Ctrl+Z)')

    parser.add_argument(
        '--taskbar-name',
        default=DEFAULT_TASKBAR_NAME,
        help='任务栏按钮名称（默认 "Adobe Photoshop 2025 - 1 running window"）',
    )

    args = parser.parse_args()

    # 确定执行的功能
    mode = 'reset'
    title = '复位工具'
    description = '复位基本功能'

    if args.layer_move:
        mode = 'layer_move_both'
        title = '图层移动工具'
        description = '上下移动图层'
    elif args.layer_up:
        mode = 'layer_up'
        title = '图层上移工具'
        description = '图层向上移动'
    elif args.layer_down:
        mode = 'layer_down'
        title = '图层下移工具'
        description = '图层向下移动'
    elif args.selection_up:
        mode = 'selection_up'
        title = '选区上移工具'
        description = '选区向上移动'
    elif args.selection_down:
        mode = 'selection_down'
        title = '选区下移工具'
        description = '选区向下移动'
    elif args.selection_left:
        mode = 'selection_left'
        title = '选区左移工具'
        description = '选区向左移动'
    elif args.selection_right:
        mode = 'selection_right'
        title = '选区右移工具'
        description = '选区向右移动'
    elif args.select_all:
        mode = 'select_all'
        title = '全选工具'
        description = '全选图层'
    elif args.deselect:
        mode = 'deselect'
        title = '取消选区工具'
        description = '取消选区'
    elif args.invert:
        mode = 'invert'
        title = '反选工具'
        description = '反选'
    elif args.duplicate:
        mode = 'duplicate'
        title = '复制图层工具'
        description = '复制图层'
    elif args.file_new:
        mode = 'file_new'
        title = '新建文档工具'
        description = '新建Photoshop文档'
    elif args.file_open:
        mode = 'file_open'
        title = '打开文档工具'
        description = '打开Photoshop文档'
    elif args.file_save:
        mode = 'file_save'
        title = '保存文档工具'
        description = '保存当前文档'
    elif args.file_save_as:
        mode = 'file_save_as'
        title = '另存为工具'
        description = '另存为新文件'
    elif args.export_as:
        mode = 'export_as'
        title = '导出工具'
        description = '导出文件'
    elif args.file_close:
        mode = 'file_close'
        title = '关闭文档工具'
        description = '关闭当前文档'
    elif args.file_close_all:
        mode = 'file_close_all'
        title = '关闭全部文档工具'
        description = '关闭所有打开的文档'
    elif args.undo:
        mode = 'undo'
        title = '撤销工具'
        description = '撤销上一步操作'
    elif args.tool:
        mode = 'tool'
        title = '工具切换'
        description = f"切换到 {args.tool}"
    elif args.tool_cycle:
        mode = 'tool_cycle'
        title = '工具循环'
        description = f"Shift 切换 {args.tool_cycle}"

    print("="*60)
    print(f"Photoshop 快捷键工具 - {title}")
    print("="*60)
    print(f"功能: {description}")

    # 1. 查找窗口
    app, win = find_photoshop_window(args.taskbar_name)
    if not app or not win:
        print("\n[FAIL] 未找到Photoshop窗口")
        print("\n请确保:")
        print("  1. Adobe Photoshop 已启动")
        print("  2. 安装依赖: pip install pywinauto pyautogui")
        sys.exit(1)

    # 2. 激活窗口
    if not activate_window(app, win):
        print("\n[FAIL] 无法激活窗口")
        sys.exit(1)

    # 3. 发送快捷键
    if mode == 'reset':
        if not send_hotkeys():
            sys.exit(1)
    elif mode == 'layer_move_both':
        if not send_layer_move_hotkeys('both'):
            sys.exit(1)
    elif mode == 'layer_up':
        if not send_layer_move_hotkeys('up'):
            sys.exit(1)
    elif mode == 'layer_down':
        if not send_layer_move_hotkeys('down'):
            sys.exit(1)
    elif mode == 'selection_up':
        if not send_selection_move_hotkey('up'):
            sys.exit(1)
    elif mode == 'selection_down':
        if not send_selection_move_hotkey('down'):
            sys.exit(1)
    elif mode == 'selection_left':
        if not send_selection_move_hotkey('left'):
            sys.exit(1)
    elif mode == 'selection_right':
        if not send_selection_move_hotkey('right'):
            sys.exit(1)
    elif mode == 'select_all':
        if not send_select_all_hotkey():
            sys.exit(1)
    elif mode == 'deselect':
        if not send_deselect_hotkey():
            sys.exit(1)
    elif mode == 'invert':
        if not send_invert_hotkey():
            sys.exit(1)
    elif mode == 'duplicate':
        if not send_duplicate_layer_hotkey():
            sys.exit(1)
    elif mode == 'file_new':
        if not send_new_file_hotkey():
            sys.exit(1)
    elif mode == 'file_open':
        if not send_open_file_hotkey():
            sys.exit(1)
    elif mode == 'file_save':
        if not send_save_file_hotkey():
            sys.exit(1)
    elif mode == 'file_save_as':
        if not send_save_as_hotkey():
            sys.exit(1)
    elif mode == 'export_as':
        if not send_export_as_hotkey():
            sys.exit(1)
    elif mode == 'file_close':
        if not send_close_file_hotkey():
            sys.exit(1)
    elif mode == 'file_close_all':
        if not send_close_all_hotkey():
            sys.exit(1)
    elif mode == 'undo':
        if not send_undo_hotkey():
            sys.exit(1)
    elif mode == 'tool':
        if not send_tool_hotkey(args.tool, cycle=False):
            sys.exit(1)
    elif mode == 'tool_cycle':
        if not send_tool_hotkey(args.tool_cycle, cycle=True):
            sys.exit(1)

    print("\n" + "="*60)
    print("[OK] 完成!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] 用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[FAIL] 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
