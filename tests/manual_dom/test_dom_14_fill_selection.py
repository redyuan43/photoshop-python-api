import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import fill_selection
from photoshop import Session  # type: ignore


def ensure_test_selection(region_size: int = 400) -> None:
    with Session() as ps:
        doc = ps.app.activeDocument if len(ps.app.documents) > 0 else ps.app.documents.add(1920, 1080, 72, "FillSelectionTest")
        left = 200
        top = 200
        right = left + region_size
        bottom = top + region_size
        region = [[left, top], [right, top], [right, bottom], [left, bottom]]
        doc.selection.select(region)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill current selection with a given color")
    parser.add_argument("--color", default="#FF0000", help="Hex color (e.g., #00FF00) or R,G,B string")
    parser.add_argument("--opacity", type=float, default=100.0, help="Opacity percentage")
    parser.add_argument("--mode", help="Blend mode name (e.g., NormalBlend, Multiply)")
    parser.add_argument(
        "--preserve-transparency",
        action="store_true",
        help="Match Photoshop's Preserve Transparency flag",
    )
    parser.add_argument(
        "--prepare-selection",
        action="store_true",
        help="Automatically create a rectangular selection before fill",
    )
    args = parser.parse_args()

    if args.prepare_selection:
        ensure_test_selection()

    payload = fill_selection(
        {
            "color": args.color,
            "opacity": args.opacity,
            "mode": args.mode,
            "preserve_transparency": args.preserve_transparency,
        }
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
