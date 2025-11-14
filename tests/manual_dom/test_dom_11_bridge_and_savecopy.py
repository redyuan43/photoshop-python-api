import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import (
    browse_in_bridge,
    close_and_browse_in_bridge,
    close_other_documents,
    save_document_copy,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bridge helpers + save copy smoke test")
    parser.add_argument("--bridge-path", help="Optional folder/file to reveal in Bridge")
    parser.add_argument("--close-save", action="store_true", help="Save documents when closing others")
    parser.add_argument(
        "--close-bridge",
        action="store_true",
        help="After closing the active doc, jump to Bridge (File > Close and Go to Bridge…)",
    )
    parser.add_argument("--copy-path", help="Path for Save a Copy (Alt+Ctrl+S)")
    args = parser.parse_args()

    result = {
        "close_other_documents": close_other_documents({"save": args.close_save}),
        "browse_in_bridge": browse_in_bridge({"path": args.bridge_path}) if args.bridge_path else browse_in_bridge({}),
    }
    if args.close_bridge:
        result["close_and_browse_in_bridge"] = close_and_browse_in_bridge(
            {"save": args.close_save, "path": args.bridge_path}
        )
    if args.copy_path:
        result["save_document_copy"] = save_document_copy({"path": args.copy_path})

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
