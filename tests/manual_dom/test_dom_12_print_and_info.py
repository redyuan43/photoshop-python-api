import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import get_document_info, print_document, print_one_copy


def main() -> None:
    parser = argparse.ArgumentParser(description="File > File Info / Print helpers")
    parser.add_argument("--print", dest="do_print", action="store_true", help="Invoke File > Print… (Ctrl+P)")
    parser.add_argument("--no-print", dest="do_print", action="store_false")
    parser.set_defaults(do_print=False)
    parser.add_argument(
        "--no-dialogs",
        action="store_true",
        help="Suppress Photoshop print dialogs when running File > Print…",
    )
    parser.add_argument(
        "--print-one-copy",
        action="store_true",
        help="Invoke File > Print One Copy (Alt+Shift+Ctrl+P) after File Info",
    )
    args = parser.parse_args()

    payload = {"file_info": get_document_info()}
    if args.do_print:
        payload["print"] = print_document({"show_dialogs": not args.no_dialogs})
    if args.print_one_copy:
        payload["print_one_copy"] = print_one_copy({})

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
