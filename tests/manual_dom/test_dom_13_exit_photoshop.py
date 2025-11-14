import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import exit_photoshop


def main() -> None:
    parser = argparse.ArgumentParser(description="Exit Photoshop (File > Exit / Ctrl+Q)")
    parser.add_argument("--save", action="store_true", help="Save before quitting when --force is used")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Close all open documents automatically before exiting Photoshop",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required flag to avoid accidental exit (script aborts without it)",
    )
    args = parser.parse_args()

    if not args.confirm:
        parser.error("You must pass --confirm to intentionally exit Photoshop.")

    payload = exit_photoshop({"save": args.save, "force": args.force})
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
