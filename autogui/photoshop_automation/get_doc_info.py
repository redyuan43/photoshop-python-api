"""Helpers for active Photoshop document information."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..get_photoshop_status import gather_status


def get_document_status(status: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = status or gather_status()
    return data.get("document") or {}


def get_document_name(status: Optional[Dict[str, Any]] = None) -> Optional[str]:
    return get_document_status(status).get("name")


def get_document_dimensions(status: Optional[Dict[str, Any]] = None) -> Dict[str, Optional[str]]:
    doc = get_document_status(status)
    return {
        "width": doc.get("width"),
        "height": doc.get("height"),
        "resolution": doc.get("resolution"),
    }
