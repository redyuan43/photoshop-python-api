from pathlib import Path

path = Path(''photoshop_hotkey_best.py'')
text = path.read_text(encoding='utf-8')
marker = '\nif __name__ == "__main__":'

insertion = '''

def send_new_document_hotkey():
    """Send Ctrl+N to create a new document."""
    print("\n[INFO] Ctrl+N -> New Document")
    try:
        pyautogui.hotkey(''ctrl'', ''n'')
        time.sleep(0.5)
        print("[OK] New document command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+N: {exc}")
        return False


def send_open_document_hotkey():
    """Send Ctrl+O to open a document."""
    print("\n[INFO] Ctrl+O -> Open Document")
    try:
        pyautogui.hotkey(''ctrl'', ''o'')
        time.sleep(0.5)
        print("[OK] Open document command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+O: {exc}")
        return False


def send_save_hotkey():
    """Send Ctrl+S to save the active document."""
    print("\n[INFO] Ctrl+S -> Save Document")
    try:
        pyautogui.hotkey(''ctrl'', ''s'')
        time.sleep(0.5)
        print("[OK] Save command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+S: {exc}")
        return False


def send_save_as_hotkey():
    """Send Ctrl+Shift+S to trigger Save As."""
    print("\n[INFO] Ctrl+Shift+S -> Save As")
    try:
        pyautogui.hotkey(''ctrl'', ''shift'', ''s'')
        time.sleep(0.5)
        print("[OK] Save As command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+Shift+S: {exc}")
        return False


def send_export_hotkey():
    """Send Ctrl+Alt+Shift+W to export."""
    print("\n[INFO] Ctrl+Alt+Shift+W -> Export")
    try:
        pyautogui.hotkey(''ctrl'', ''alt'', ''shift'', ''w'')
        time.sleep(0.5)
        print("[OK] Export command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+Alt+Shift+W: {exc}")
        return False


def send_close_document_hotkey():
    """Send Ctrl+W to close the active document."""
    print("\n[INFO] Ctrl+W -> Close Document")
    try:
        pyautogui.hotkey(''ctrl'', ''w'')
        time.sleep(0.5)
        print("[OK] Close document command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+W: {exc}")
        return False


def send_close_all_hotkey():
    """Send Ctrl+Alt+W to close all documents."""
    print("\n[INFO] Ctrl+Alt+W -> Close All Documents")
    try:
        pyautogui.hotkey(''ctrl'', ''alt'', ''w'')
        time.sleep(0.5)
        print("[OK] Close all command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+Alt+W: {exc}")
        return False


def send_undo_hotkey():
    """Send Ctrl+Z to undo last action."""
    print("\n[INFO] Ctrl+Z -> Undo")
    try:
        pyautogui.hotkey(''ctrl'', ''z'')
        time.sleep(0.5)
        print("[OK] Undo command sent")
        return True
    except Exception as exc:
        print(f"[FAIL] Failed to send Ctrl+Z: {exc}")
        return False
'''

if marker not in text:
    raise SystemExit(''Marker not found'')

path.write_text(text.replace(marker, insertion + marker, 1), encoding='utf-8')
