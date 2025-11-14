import sys
from pathlib import Path
import argparse
import json

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import close_document, duplicate_document, revert_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Revert, duplicate, and close document")
    parser.add_argument("--duplicate-name", help="Name for duplicated document", default=None)
    parser.add_argument("--save-on-close", action="store_true", help="Save before closing")
    args = parser.parse_args()

    result = {
        "revert": revert_document(),
        "duplicate": duplicate_document({"name": args.duplicate_name} if args.duplicate_name else {}),
        "close": close_document({"save": args.save_on_close}),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
