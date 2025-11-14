import sys
from pathlib import Path
import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import (
    import_image_as_layer,
    replace_layer_with_file,
    remove_background_layer,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Import/replace image content and optionally remove background")
    parser.add_argument("--import-path", help="Path to image placed as new layer", default=None)
    parser.add_argument("--replace-path", help="Path to replace active layer/smart object", default=None)
    parser.add_argument("--remove-background", action="store_true", help="Remove background layer after operations")
    args = parser.parse_args()

    result = {}
    if args.import_path:
        result["import"] = import_image_as_layer({"path": str(Path(args.import_path).expanduser())})
    if args.replace_path:
        result["replace"] = replace_layer_with_file({"path": str(Path(args.replace_path).expanduser())})
    if args.remove_background:
        result["remove_background"] = remove_background_layer()
    print(json.dumps(result or {"info": "no ops requested"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
