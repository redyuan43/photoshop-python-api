from pathlib import Path
import textwrap

path = Path('photoshop_hotkey_best.py')
text = path.read_text(encoding='utf-8')

# Update docstring with file operation section
if '【文件操作】' not in text:
    doc_marker = "  --duplicate   - 复制图层 (Ctrl+J)\n"
    if doc_marker in text:
        doc_insert = """【文件操作】\n  --new-file    - 新建文件 (Ctrl+N)\n  --open-file   - 打开文件 (Ctrl+O)\n  --save        - 保存文件 (Ctrl+S)\n  --save-as     - 另存为 (Ctrl+Shift+S)\n  --export-as   - 导出为 (Ctrl+Alt+Shift+W)\n  --close-file  - 关闭当前文件 (Ctrl+W)\n  --close-all   - 关闭所有文件 (Ctrl+Alt+W)\n  --undo        - 撤销上一步 (Ctrl+Z)\n"""
        text = text.replace(doc_marker, doc_marker + "\n" + doc_insert, 1)

helpers_marker = "\ndef main():"
if 'def send_new_file_hotkey' not in text:
    helpers = textwrap.dedent('''


def send_new_file_hotkey():
    """发送新建文件快捷键: Ctrl+N"""
    print("\n开始发送新建文件快捷键...")
    print("  Ctrl + N  - 新建文件")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+N (新建文件)")
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False


def send_open_file_hotkey():
    """发送打开文件快捷键: Ctrl+O"""
    print("\n开始发送打开文件快捷键...")
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
    """发送保存文件快捷键: Ctrl+S"""
    print("\n开始发送保存文件快捷键...")
    print("  Ctrl + S  - 保存当前文件")
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
    print("  Ctrl + Alt + Shift + W  - 导出文件")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Alt+Shift+W (导出文件)")
        pyautogui.hotkey('ctrl', 'alt', 'shift', 'w')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False


def send_close_file_hotkey():
    """发送关闭文件快捷键: Ctrl+W"""
    print("\n开始发送关闭文件快捷键...")
    print("  Ctrl + W  - 关闭当前文件")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+W (关闭当前文件)")
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)
        print("\n[OK] 快捷键发送完成")
        return True
    except Exception as e:
        print(f"[FAIL] 发送失败: {e}")
        return False


def send_close_all_hotkey():
    """发送关闭全部文件快捷键: Ctrl+Alt+W"""
    print("\n开始发送关闭全部快捷键...")
    print("  Ctrl + Alt + W  - 关闭所有文件")
    print("\n请观察窗口响应...")

    try:
        print("\n发送 Ctrl+Alt+W (关闭所有文件)")
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
    ''')
    text = text.replace(helpers_marker, helpers + "\n\ndef main():", 1)

args_marker = "    group.add_argument('--duplicate', action='store_true',\n                      help='复制图层 (Ctrl+J)')\n"
if "--new-file" not in text and args_marker in text:
    new_args = """\n    # 文件与文档操作
    group.add_argument('--new-file', action='store_true',
                      help='新建文件 (Ctrl+N)')
    group.add_argument('--open-file', action='store_true',
                      help='打开文件 (Ctrl+O)')
    group.add_argument('--save', action='store_true',
                      help='保存文件 (Ctrl+S)')
    group.add_argument('--save-as', action='store_true',
                      help='另存为 (Ctrl+Shift+S)')
    group.add_argument('--export-as', action='store_true',
                      help='导出文件 (Ctrl+Alt+Shift+W)')
    group.add_argument('--close-file', action='store_true',
                      help='关闭当前文件 (Ctrl+W)')
    group.add_argument('--close-all', action='store_true',
                      help='关闭所有文件 (Ctrl+Alt+W)')
    group.add_argument('--undo', action='store_true',
                      help='撤销上一步 (Ctrl+Z)')\n"""
    text = text.replace(args_marker, args_marker + new_args, 1)

mode_marker = "    elif args.duplicate:\n        mode = 'duplicate'\n        title = '复制图层工具'\n        description = '复制图层'\n"
if "mode = 'new_file'" not in text and mode_marker in text:
    new_modes = """    elif args.new_file:\n        mode = 'new_file'\n        title = '新建文件工具'\n        description = '创建一个新文件'\n    elif args.open_file:\n        mode = 'open_file'\n        title = '打开文件工具'\n        description = '打开文件对话框'\n    elif args.save:\n        mode = 'save_file'\n        title = '保存工具'\n        description = '保存当前文件'\n    elif args.save_as:\n        mode = 'save_as'\n        title = '另存为工具'\n        description = '另存为当前文件'\n    elif args.export_as:\n        mode = 'export_as'\n        title = '导出文件工具'\n        description = '导出为其他格式'\n    elif args.close_file:\n        mode = 'close_file'\n        title = '关闭文件工具'\n        description = '关闭当前文档'\n    elif args.close_all:\n        mode = 'close_all'\n        title = '全部关闭工具'\n        description = '关闭所有打开的文档'\n    elif args.undo:\n        mode = 'undo'\n        title = '撤销工具'\n        description = '撤销最近一步操作'\n"""
    text = text.replace(mode_marker, mode_marker + new_modes, 1)

call_marker = "    elif mode == 'duplicate':\n        if not send_duplicate_layer_hotkey():\n            sys.exit(1)\n"
if "mode == 'new_file'" not in text and call_marker in text:
    new_calls = """    elif mode == 'new_file':\n        if not send_new_file_hotkey():\n            sys.exit(1)\n    elif mode == 'open_file':\n        if not send_open_file_hotkey():\n            sys.exit(1)\n    elif mode == 'save_file':\n        if not send_save_file_hotkey():\n            sys.exit(1)\n    elif mode == 'save_as':\n        if not send_save_as_hotkey():\n            sys.exit(1)\n    elif mode == 'export_as':\n        if not send_export_as_hotkey():\n            sys.exit(1)\n    elif mode == 'close_file':\n        if not send_close_file_hotkey():\n            sys.exit(1)\n    elif mode == 'close_all':\n        if not send_close_all_hotkey():\n            sys.exit(1)\n    elif mode == 'undo':\n        if not send_undo_hotkey():\n            sys.exit(1)\n"""
    text = text.replace(call_marker, call_marker + new_calls, 1)

path.write_text(text, encoding='utf-8')
