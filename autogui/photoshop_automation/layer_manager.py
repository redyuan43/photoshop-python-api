#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Photoshop layer helper: list layers and activate by name or index."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from photoshop import Session  # type: ignore


@dataclass
class LayerRecord:
    index: int
    name: str
    visible: bool
    kind: str
    depth: int
    is_group: bool
    handle: Any


def _collect_children(layer) -> List[Any]:
    children: List[Any] = []
    # Some objects expose .layers, others separate artLayers/layerSets
    for attr in ("layers",):
        try:
            coll = getattr(layer, attr)
            for child in coll:
                children.append(child)
            if children:
                return children
        except Exception:
            continue
    for attr in ("layerSets", "artLayers"):
        try:
            coll = getattr(layer, attr)
            for child in coll:
                children.append(child)
        except Exception:
            continue
    return children


def _flatten_layers(collection, results: List[LayerRecord], depth: int = 0) -> None:
    for layer in collection:
        name = getattr(layer, "name", f"Layer_{len(results)}")
        visible = getattr(layer, "visible", True)
        kind = str(getattr(layer, "kind", "unknown"))
        try:
            children = _collect_children(layer)
        except Exception:
            children = []
        is_group = bool(children)

        record = LayerRecord(
            index=len(results),
            name=name,
            visible=visible,
            kind=kind,
            depth=depth,
            is_group=is_group,
            handle=layer,
        )
        results.append(record)

        if children:
            _flatten_layers(children, results, depth + 1)


def _build_layer_records(doc) -> List[LayerRecord]:
    layers: List[LayerRecord] = []
    _flatten_layers(doc.layers, layers, depth=0)
    return layers


def _layer_record_sort_key(record: LayerRecord) -> Tuple[int, int]:
    item_index = _resolve_layer_item_index(record.handle)
    if item_index is None:
        return (1, record.index)
    return (0, item_index)


def _resolve_layer_item_index(layer) -> Optional[int]:
    try:
        value = getattr(layer, "itemIndex", None)
    except Exception:
        return None
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _ordered_layer_records(doc) -> List[LayerRecord]:
    records = _build_layer_records(doc)
    records.sort(key=_layer_record_sort_key)
    return records


def _find_layer_position(records: List[LayerRecord], target_index: int) -> Optional[int]:
    for idx, record in enumerate(records):
        item_index = _resolve_layer_item_index(record.handle)
        if item_index is None:
            continue
        if item_index == target_index:
            return idx
    return None


def list_layers(flat: bool = True) -> List[LayerRecord]:
    """Return flattened list of layers for the active document."""
    with Session() as ps:
        doc = ps.active_document
        return _build_layer_records(doc)


def activate_layer_by_name(target: str) -> Tuple[bool, Optional[str]]:
    name_norm = target.strip().lower()
    with Session() as ps:
        doc = ps.active_document
        layers: List[LayerRecord] = []
        _flatten_layers(doc.layers, layers)
        for record in layers:
            if record.name.lower() == name_norm:
                doc.activeLayer = record.handle
                return True, record.name
    return False, None


def activate_layer_by_index(idx: int) -> Tuple[bool, Optional[str]]:
    with Session() as ps:
        doc = ps.active_document
        layers = _build_layer_records(doc)
        if 0 <= idx < len(layers):
            record = layers[idx]
            doc.activeLayer = record.handle
            return True, record.name
    return False, None


def _move_active_layer(delta: int) -> Tuple[bool, Optional[str]]:
    if delta not in (-1, 1):
        raise ValueError("delta must be -1 or 1")
    with Session() as ps:
        doc = ps.active_document
        active_layer = doc.activeLayer
        item_index = _resolve_layer_item_index(active_layer)
        if item_index is None:
            return False, "无法获取当前图层的位置"
        ordered_records = _ordered_layer_records(doc)
        current_pos = _find_layer_position(ordered_records, item_index)
        if current_pos is None:
            return False, "未能在图层列表中找到当前图层"
        target_pos = current_pos + delta
        if target_pos < 0:
            return False, "当前图层已经在最顶部"
        if target_pos >= len(ordered_records):
            return False, "当前图层已经在最底部"
        reference = ordered_records[target_pos].handle
        placement = (
            ps.ElementPlacement.PlaceBefore if delta < 0 else ps.ElementPlacement.PlaceAfter
        )
        try:
            active_layer.move(reference, placement)
        except Exception as exc:
            return False, str(exc)

        return True, getattr(active_layer, "name", None)


def move_layer_up() -> Tuple[bool, Optional[str]]:
    return _move_active_layer(delta=-1)


def move_layer_down() -> Tuple[bool, Optional[str]]:
    return _move_active_layer(delta=1)


def duplicate_active_layer() -> Tuple[bool, Optional[str]]:
    with Session() as ps:
        doc = ps.active_document
        active_layer = doc.activeLayer
        try:
            duplicated = active_layer.duplicate()
        except Exception as exc:
            return False, str(exc)

        new_layer = duplicated or doc.activeLayer
        try:
            doc.activeLayer = new_layer
        except Exception:
            # If Photoshop already switched the active layer we can ignore errors.
            pass

        return True, getattr(new_layer, "name", None)


def main():
    parser = argparse.ArgumentParser(description="Photoshop Layer Manager")
    parser.add_argument("--list", action="store_true", help="List layers as JSON")
    parser.add_argument("--activate", metavar="NAME", help="Activate layer by name")
    parser.add_argument("--activate-index", type=int, help="Activate layer by flattened index")
    parser.add_argument("--layer-up", action="store_true", help="Move active layer up (Ctrl+})")
    parser.add_argument("--layer-down", action="store_true", help="Move active layer down (Ctrl+{)")
    parser.add_argument("--duplicate", action="store_true", help="Duplicate active layer (Ctrl+J)")
    args = parser.parse_args()

    if args.list:
        payload = [
            {
                "index": rec.index,
                "name": rec.name,
                "visible": rec.visible,
                "kind": rec.kind,
                "depth": rec.depth,
                "is_group": rec.is_group,
            }
            for rec in list_layers()
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.activate:
        ok, name = activate_layer_by_name(args.activate)
        if not ok:
            print(f"[FAIL] 未找到名称 {args.activate} 的图层")
            raise SystemExit(1)
        print(f"[OK] 已切换到图层: {name}")
        return

    if args.activate_index is not None:
        ok, name = activate_layer_by_index(args.activate_index)
        if not ok:
            print(f"[FAIL] 无效的图层索引 {args.activate_index}")
            raise SystemExit(1)
        print(f"[OK] 已切换到图层: {name}")
        return

    if args.layer_up:
        ok, info = move_layer_up()
        if not ok:
            print(f"[FAIL] {info or '无法将当前图层上移'}")
            raise SystemExit(1)
        print(f"[OK] 已将当前图层上移: {info}")
        return

    if args.layer_down:
        ok, info = move_layer_down()
        if not ok:
            print(f"[FAIL] {info or '无法将当前图层下移'}")
            raise SystemExit(1)
        print(f"[OK] 已将当前图层下移: {info}")
        return

    if args.duplicate:
        ok, info = duplicate_active_layer()
        if not ok:
            print(f"[FAIL] {info or '无法复制当前图层'}")
            raise SystemExit(1)
        print(f"[OK] 已复制当前图层: {info}")
        return

    parser.print_help()
    raise SystemExit(1)


if __name__ == "__main__":
    main()
