import sys
from pathlib import Path
import argparse
import json

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from autogui.dom_actions import convert_layer_to_smart_object, rasterize_layer
from photoshop import Session  # type: ignore
from photoshop.api.enumerations import LayerKind  # type: ignore

SMART_OBJECT_KIND_VALUE = int(LayerKind.SmartObjectLayer)

SMART_OBJECT_JS = """
var ref = new ActionReference();
ref.putEnumerated(charIDToTypeID("Lyr "), charIDToTypeID("Ordn"), charIDToTypeID("Trgt"));
var desc = executeActionGet(ref);
desc.hasKey(stringIDToTypeID("smartObject"));
"""


def _capture_layer_state() -> dict:
    with Session() as ps:
        doc = ps.active_document
        layer = doc.activeLayer
        kind = getattr(layer, "kind", None)
        kind_str = str(kind)
        kind_repr = repr(kind)
        kind_value = None
        try:
            kind_value = int(kind)
        except Exception:
            kind_value = None

        js_flag = None
        try:
            js_result = ps.app.doJavaScript(SMART_OBJECT_JS)
            if isinstance(js_result, str):
                lowered = js_result.strip().lower()
                if lowered in {"true", "false"}:
                    js_flag = lowered == "true"
                else:
                    js_flag = lowered not in {"0", "", "false"}
            else:
                js_flag = bool(js_result)
        except Exception:
            js_flag = None

        is_smart = bool(js_flag) if js_flag is not None else False

        if not is_smart and kind_value is not None:
            is_smart = kind_value == SMART_OBJECT_KIND_VALUE

        if not is_smart and ("SmartObject" in kind_str or "SmartObject" in kind_repr):
            is_smart = True

        if not is_smart:
            smart_handle = None
            try:
                smart_handle = getattr(layer, "smartObject")
            except Exception:
                smart_handle = None
            if smart_handle is not None:
                is_smart = True

        return {
            "layer": getattr(layer, "name", None),
            "kind": kind_str,
            "kind_repr": kind_repr,
            "kind_value": kind_value,
            "smart_object_flag": js_flag,
            "is_smart_object": is_smart,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert/rasterize active layer")
    parser.add_argument("--raster-mode", default="EntireLayer", help="Rasterize mode (default EntireLayer)")
    args = parser.parse_args()

    state_before = _capture_layer_state()
    convert_payload = convert_layer_to_smart_object()
    state_after_convert = _capture_layer_state()

    raster_payload = rasterize_layer({"mode": args.raster_mode})
    state_after_raster = _capture_layer_state()

    result = {
        "state_before": state_before,
        "convert": convert_payload,
        "state_after_convert": state_after_convert,
        "rasterize": raster_payload,
        "state_after_raster": state_after_raster,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
