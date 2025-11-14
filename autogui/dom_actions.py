"""DOM/COM powered Photoshop actions consumable by the action registry."""

from __future__ import annotations

from typing import Any, Dict, List

from photoshop import Session  # type: ignore
from autogui.photoshop_automation import layer_manager


def _ensure_document(ps) -> Any:
    """Return the active document, creating one if necessary."""
    if len(ps.app.documents) > 0:
        return ps.active_document
    doc = ps.app.documents.add(1920, 1080, 72, "LLM_AutoDoc")
    return doc


def fit_on_screen(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Make the active document fit on screen (menu command FtOn)."""
    params = params or {}
    with Session() as ps:
        doc = _ensure_document(ps)
        ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
        return {"document": getattr(doc, "name", None)}


def create_new_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Create a new Photoshop document with configurable size."""
    params = params or {}
    width = float(params.get("width", 1920))
    height = float(params.get("height", 1080))
    resolution = float(params.get("resolution", 72))
    name = str(params.get("name", "LLM_Document"))

    with Session() as ps:
        doc = ps.app.documents.add(width=width, height=height, resolution=resolution, name=name)
        return {
            "document": getattr(doc, "name", name),
            "width": width,
            "height": height,
            "resolution": resolution,
        }


def apply_gaussian_blur(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Apply Gaussian Blur to the active layer."""
    params = params or {}
    radius = float(params.get("radius", 5.0))

    with Session() as ps:
        doc = _ensure_document(ps)
        layer = doc.activeLayer
        blur_options = ps.GaussianBlurOptions()
        blur_options.radius = radius
        layer.applyGaussianBlur(blur_options)
        return {
            "document": getattr(doc, "name", None),
            "layer": getattr(layer, "name", None),
            "radius": radius,
        }


def list_layers_flat(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return flattened layer metadata for the active document."""
    params = params or {}
    records = layer_manager.list_layers()
    payload: List[Dict[str, Any]] = []
    for rec in records:
        payload.append(
            {
                "index": rec.index,
                "name": rec.name,
                "visible": rec.visible,
                "kind": rec.kind,
                "depth": rec.depth,
                "is_group": rec.is_group,
            }
        )
    return {"layers": payload, "count": len(payload)}


def activate_layer_by_name_action(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    target = params.get("target") or params.get("name")
    if not target:
        raise ValueError("缺少图层名称参数 (target)")
    ok, name = layer_manager.activate_layer_by_name(str(target))
    if not ok:
        raise RuntimeError(f"无法切换到图层: {target}")
    return {"active_layer": name}


def activate_layer_by_index_action(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    index_param = params.get("index")
    position = (params.get("position") or params.get("pos") or "").lower()

    records = layer_manager.list_layers()
    if not records:
        raise RuntimeError("当前文档没有可用图层")

    if index_param is None:
        if position in {"top", "highest", "first"}:
            idx = 0
        elif position in {"bottom", "lowest", "last"}:
            idx = len(records) - 1
        else:
            # 默认切到最下方的图层以符合常见语义
            idx = len(records) - 1
    else:
        try:
            idx = int(index_param)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"非法图层索引: {index_param}") from exc

    if idx < 0:
        idx = max(0, len(records) + idx)
    if idx >= len(records):
        raise ValueError(f"图层索引超出范围: {idx}")

    ok, name = layer_manager.activate_layer_by_index(idx)
    if not ok:
        raise RuntimeError(f"无法切换到图层索引 {idx}")
    return {"active_layer": name, "index": idx}
