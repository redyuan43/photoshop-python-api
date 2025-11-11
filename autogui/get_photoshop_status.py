#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collect richer Photoshop runtime status for LLM / automation consumers.

Exposes a JSON payload containing:
  - 当前工具
  - 当前文档核心属性 (名称、尺寸、模式、路径等)
  - 当前图层信息
  - 选区是否存在及其边界
  - 前景 / 背景色 (RGB)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def ensure_repo_on_path() -> None:
    """Add project root to sys.path when invoked from autogui/."""
    repo_root = Path(__file__).resolve().parents[1]
    repo_str = str(repo_root)
    if repo_str not in sys.path:
        sys.path.insert(0, repo_str)


def serialize_unit(value: Any) -> Optional[str]:
    """Best-effort string representation for Photoshop unit values."""
    if value is None:
        return None
    try:
        # UnitValue exposes .asString()
        as_string = value.asString()  # type: ignore[attr-defined]
        if isinstance(as_string, str):
            return as_string
    except Exception:
        pass
    return str(value)


def color_to_dict(solid_color: Any) -> Dict[str, Any]:
    """Extract RGB channels (if available) from a SolidColor object."""
    result: Dict[str, Any] = {}
    try:
        model = getattr(solid_color, "model", None)
        if model is not None:
            result["model"] = str(model)
    except Exception:
        pass

    try:
        rgb = solid_color.rgb  # type: ignore[attr-defined]
        result["rgb"] = {
            "red": getattr(rgb, "red", None),
            "green": getattr(rgb, "green", None),
            "blue": getattr(rgb, "blue", None),
        }
    except Exception:
        result["rgb"] = None
    return result


def gather_status() -> Dict[str, Any]:
    """Return the aggregated Photoshop status dictionary."""
    from photoshop import Session  # pylint: disable=import-outside-toplevel
    from photoshop.api import errors  # pylint: disable=import-outside-toplevel

    status: Dict[str, Any] = {
        "tool": None,
        "document": None,
        "layer": None,
        "selection": {"has_selection": False, "bounds": None},
        "colors": {"foreground": None, "background": None},
    }

    with Session() as ps:
        try:
            status["tool"] = ps.app.currentTool
        except Exception:
            status["tool"] = None

        try:
            doc = ps.active_document
        except errors.PhotoshopPythonAPIError:
            doc = None

        def safe_attr(target: Any, name: str, fallback: Any = None) -> Any:
            try:
                return getattr(target, name)
            except Exception:
                return fallback

        def safe_str(value: Any) -> Optional[str]:
            if value is None:
                return None
            try:
                text = str(value)
                return text if text else None
            except Exception:
                return None

        if doc:
            layer_count = None
            try:
                layers_obj = safe_attr(doc, "layers")
                if layers_obj is not None:
                    try:
                        layer_count = safe_attr(layers_obj, "length")
                    except Exception:
                        try:
                            layer_count = len(list(layers_obj))  # type: ignore[arg-type]
                        except Exception:
                            layer_count = None
            except Exception:
                layer_count = None

            status["document"] = {
                "name": safe_attr(doc, "name"),
                "path": safe_str(safe_attr(doc, "path")),
                "full_name": safe_str(safe_attr(doc, "fullName")),
                "width": serialize_unit(safe_attr(doc, "width")),
                "height": serialize_unit(safe_attr(doc, "height")),
                "resolution": serialize_unit(safe_attr(doc, "resolution")),
                "mode": safe_str(safe_attr(doc, "mode")),
                "bits_per_channel": safe_attr(doc, "bitsPerChannel"),
                "color_profile": safe_attr(doc, "colorProfileName"),
                "layers": layer_count,
            }

            # Active layer info
            try:
                layer = safe_attr(doc, "activeLayer")
            except Exception:
                layer = None

            if layer:
                status["layer"] = {
                    "name": safe_attr(layer, "name"),
                    "kind": safe_str(safe_attr(layer, "kind")),
                    "visible": safe_attr(layer, "visible"),
                    "locked": safe_attr(layer, "allLocked"),
                    "opacity": safe_attr(layer, "opacity"),
                    "fillOpacity": safe_attr(layer, "fillOpacity"),
                    "is_background": safe_attr(layer, "isBackgroundLayer"),
                }

            # Selection
            try:
                selection = safe_attr(doc, "selection")
                bounds = selection.bounds if selection else None  # type: ignore[attr-defined]
                if selection and bounds:
                    status["selection"] = {
                        "has_selection": True,
                        "bounds": [serialize_unit(val) for val in bounds],
                    }
                else:
                    raise ValueError
            except Exception:
                status["selection"] = {"has_selection": False, "bounds": None}

        # Colors are app-level and exist even without documents
        try:
            status["colors"]["foreground"] = color_to_dict(ps.app.foregroundColor)
        except Exception:
            status["colors"]["foreground"] = None
        try:
            status["colors"]["background"] = color_to_dict(ps.app.backgroundColor)
        except Exception:
            status["colors"]["background"] = None

    return status


def main() -> None:
    ensure_repo_on_path()

    try:
        status = gather_status()
    except Exception as exc:  # pylint: disable=broad-except
        print("[FAIL] 无法获取 Photoshop 状态")
        print(f"原因: {exc}")
        print("\n排查建议:")
        print("  1. 确认 Photoshop 正在运行 (至少打开一个空白文档)")
        print("  2. 已安装 photoshop-python-api 依赖 (pip install .)")
        print("  3. 如涉及权限问题，可尝试以管理员身份运行 PowerShell")
        sys.exit(1)

    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
