import sys
from pathlib import Path
import argparse
import json

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import rotate_active_layer
from photoshop import Session  # type: ignore


def _capture_layer_state() -> dict:
    with Session() as ps:
        doc = ps.active_document
        layer = doc.activeLayer
        bounds = getattr(layer, "bounds", None)
        try:
            bounds_repr = [str(value) for value in bounds] if bounds else None
        except Exception:
            bounds_repr = None
        return {
            "document": getattr(doc, "name", None),
            "layer": getattr(layer, "name", None),
            "kind": str(getattr(layer, "kind", None)),
            "visible": getattr(layer, "visible", None),
            "bounds": bounds_repr,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rotate the active layer via DOM")
    parser.add_argument("--angle", type=float, default=45.0, help="Angle in degrees (clockwise positive)")
    parser.add_argument("--anchor", default="MiddleCenter", help="Anchor name (e.g., MiddleCenter, TopLeft)")
    args = parser.parse_args()

    print("[INFO] Capturing layer state before rotation...", flush=True)
    state_before = _capture_layer_state()

    print(f"[INFO] Rotating active layer by {args.angle}° (anchor={args.anchor})...", flush=True)
    payload = rotate_active_layer({"angle": args.angle, "anchor": args.anchor})

    print("[INFO] Capturing layer state after rotation...", flush=True)
    state_after = _capture_layer_state()

    result = {
        "request": {"angle": args.angle, "anchor": args.anchor},
        "rotate": payload,
        "state_before": state_before,
        "state_after": state_after,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
