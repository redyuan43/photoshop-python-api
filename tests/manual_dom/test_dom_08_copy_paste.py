import sys
from pathlib import Path
import argparse
import json

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import copy_selection, paste_to_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy current selection and paste as new layer")
    parser.add_argument("--merge", action="store_true", help="Copy merged pixels")
    args = parser.parse_args()

    result = {
        "copy": copy_selection({"merge": args.merge}),
        "paste": paste_to_document(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
