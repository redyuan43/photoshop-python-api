import sys
from pathlib import Path
import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import open_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Open a document via DOM")
    parser.add_argument("path", help="PSD/PSB/image path to open")
    args = parser.parse_args()

    payload = open_document({"path": str(Path(args.path).expanduser())})
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
