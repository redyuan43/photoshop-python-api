"""Helper functions to fetch active layer information."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..get_photoshop_status import gather_status


def get_layer_status(status: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Return the active layer sub-dict."""
    data = status or gather_status()
    return data.get("layer") or {}


def get_active_layer_name(status: Optional[Dict[str, Any]] = None) -> Optional[str]:
    return get_layer_status(status).get("name")


def is_layer_visible(status: Optional[Dict[str, Any]] = None) -> Optional[bool]:
    return get_layer_status(status).get("visible")
