import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import open_document_as, open_document_as_smart_object


def main() -> None:
    parser = argparse.ArgumentParser(description="Open files via Open As / Open as Smart Object")
    parser.add_argument("path", help="Path to the document to open")
    parser.add_argument("--format", help="Optional format hint (psd/png/jpeg/etc.)")
    parser.add_argument(
        "--smart-only",
        action="store_true",
        help="Only run the Smart Object variant (skip regular Open As)",
    )
    args = parser.parse_args()

    payload = {}
    if not args.smart_only:
        payload["open_as"] = open_document_as({"path": args.path, "format": args.format})
    payload["open_as_smart_object"] = open_document_as_smart_object({"path": args.path, "format": args.format})

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
