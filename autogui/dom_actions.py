"""DOM/COM powered Photoshop actions consumable by the action registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from photoshop import Session  # type: ignore
from photoshop.api import (
    ActionDescriptor,
    ActionReference,
    JPEGSaveOptions,
    PNGSaveOptions,
    PhotoshopSaveOptions,
    SaveOptions,
)
from photoshop.api.enumerations import OpenDocumentType

from autogui.photoshop_automation import layer_manager


def _ensure_document(ps) -> Any:
    if len(ps.app.documents) > 0:
        return ps.active_document
    return ps.app.documents.add(1920, 1080, 72, "LLM_AutoDoc")


def _document_to_dict(doc) -> Dict[str, Any]:
    def safe_attr(target: Any, name: str) -> Optional[str]:
        try:
            value = getattr(target, name)
        except Exception:  # pylint: disable=broad-except
            return None
        if value is None:
            return None
        try:
            return str(value)
        except Exception:  # pylint: disable=broad-except
            return None

    return {
        "name": safe_attr(doc, "name"),
        "path": safe_attr(doc, "fullName") or safe_attr(doc, "path"),
        "width": safe_attr(doc, "width"),
        "height": safe_attr(doc, "height"),
        "resolution": safe_attr(doc, "resolution"),
        "mode": safe_attr(doc, "mode"),
    }


def _safe_layer_name(layer: Any) -> Optional[str]:
    try:
        value = getattr(layer, "name")
    except Exception:  # pylint: disable=broad-except
        return None
    if value is None:
        return None
    try:
        return str(value)
    except Exception:  # pylint: disable=broad-except
        return None


def _escape_js_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


_OPEN_TYPE_ALIASES = {
    "psd": OpenDocumentType.PhotoshopOpen,
    "psb": OpenDocumentType.PhotoshopOpen,
    "photoshop": OpenDocumentType.PhotoshopOpen,
    "jpg": OpenDocumentType.JPEGOpen,
    "jpeg": OpenDocumentType.JPEGOpen,
    "png": OpenDocumentType.PNGOpen,
    "tif": OpenDocumentType.TIFFOpen,
    "tiff": OpenDocumentType.TIFFOpen,
    "bmp": OpenDocumentType.BMPOpen,
    "gif": OpenDocumentType.CompuServeGIFOpen,
    "raw": OpenDocumentType.RawOpen,
    "pdf": OpenDocumentType.PDFOpen,
    "psd1": OpenDocumentType.PhotoshopOpen,
    "psd2": OpenDocumentType.PhotoshopOpen,
}


def _resolve_open_document_type(value: Any, path_hint: Optional[Path] = None) -> Optional[OpenDocumentType]:
    candidate = value
    if candidate is None and path_hint is not None:
        candidate = path_hint.suffix.lstrip(".")
    if candidate is None:
        return None
    if isinstance(candidate, OpenDocumentType):
        return candidate
    if isinstance(candidate, int):
        try:
            return OpenDocumentType(candidate)
        except ValueError:
            return None
    token = str(candidate).strip()
    if not token:
        return None
    token_lower = token.lower()
    if token_lower in _OPEN_TYPE_ALIASES:
        return _OPEN_TYPE_ALIASES[token_lower]
    token_compact = token.replace(" ", "")
    if token_compact in OpenDocumentType.__members__:
        return OpenDocumentType[token_compact]
    token_with_suffix = f"{token_compact}Open"
    if token_with_suffix in OpenDocumentType.__members__:
        return OpenDocumentType[token_with_suffix]
    return None


_DOCUMENT_INFO_FIELDS = [
    "author",
    "authorPosition",
    "caption",
    "captionWriter",
    "category",
    "city",
    "country",
    "copyrightNotice",
    "copyrighted",
    "creationDate",
    "credit",
    "exif",
    "headline",
    "instructions",
    "jobName",
    "keywords",
    "ownerUrl",
    "provinceState",
    "source",
    "supplementalCategories",
    "title",
    "transmissionReference",
    "urgency",
]


def fit_on_screen(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    with Session() as ps:
        doc = _ensure_document(ps)
        ps.app.runMenuItem(ps.app.charIDToTypeID("FtOn"))
        return {"document": getattr(doc, "name", None)}


def create_new_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
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


def rotate_active_layer(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    angle = float(params.get("angle", 0.0))
    anchor_name = str(params.get("anchor", "MiddleCenter"))
    with Session() as ps:
        doc = _ensure_document(ps)
        layer = doc.activeLayer
        anchor = getattr(ps.AnchorPosition, anchor_name, ps.AnchorPosition.MiddleCenter)
        layer.rotate(angle, anchor)
        return {"layer": _safe_layer_name(layer), "angle": angle, "anchor": anchor_name}


def convert_layer_to_smart_object(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    with Session() as ps:
        doc = _ensure_document(ps)
        layer = doc.activeLayer
        layer.convertToSmartObject()
        return {"layer": _safe_layer_name(layer), "status": "smart_object"}


def rasterize_layer(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    mode = str(params.get("mode", "EntireLayer"))
    with Session() as ps:
        doc = _ensure_document(ps)
        layer = doc.activeLayer
        raster_mode = getattr(ps.RasterizeType, mode, ps.RasterizeType.EntireLayer)
        layer.rasterize(raster_mode)
        return {"layer": _safe_layer_name(layer), "mode": mode}


def apply_gaussian_blur(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    radius = float(params.get("radius", 5.0))
    with Session() as ps:
        doc = _ensure_document(ps)
        layer = doc.activeLayer
        blur_options = ps.GaussianBlurOptions()
        blur_options.radius = radius
        layer.applyGaussianBlur(blur_options)
        return {"layer": _safe_layer_name(layer), "radius": radius}


def list_layers_flat(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    records = layer_manager.list_layers()
    payload = []
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
        raise ValueError("Missing layer name (target)")
    ok, name = layer_manager.activate_layer_by_name(str(target))
    if not ok:
        raise RuntimeError(f"Unable to activate layer: {target}")
    return {"active_layer": name}


def activate_layer_by_index_action(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    index_param = params.get("index")
    position = (params.get("position") or params.get("pos") or "").lower()
    records = layer_manager.list_layers()
    if not records:
        raise RuntimeError("No layers available in the current document")
    if index_param is None:
        if position in {"top", "highest", "first"}:
            idx = 0
        elif position in {"bottom", "lowest", "last"}:
            idx = len(records) - 1
        else:
            idx = len(records) - 1
    else:
        try:
            idx = int(index_param)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid layer index: {index_param}") from exc
    if idx < 0:
        idx = max(0, len(records) + idx)
    if idx >= len(records):
        raise ValueError(f"Layer index out of range: {idx}")
    ok, name = layer_manager.activate_layer_by_index(idx)
    if not ok:
        raise RuntimeError(f"Unable to activate layer index {idx}")
    return {"active_layer": name, "index": idx}


def list_documents(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    with Session() as ps:
        docs = [_document_to_dict(doc) for doc in ps.app.documents]
        return {"documents": docs, "count": len(docs)}


def open_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    file_path = params.get("path") or params.get("file") or params.get("file_path")
    if not file_path:
        raise ValueError("Missing file path to open")
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with Session(str(path), action="open") as ps:
        return {"document": _document_to_dict(ps.active_document)}


def open_document_as(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    file_path = params.get("path") or params.get("file") or params.get("file_path")
    if not file_path:
        raise ValueError("Missing file path to open")
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    doc_type_hint = params.get("format") or params.get("type") or params.get("document_type")
    doc_type = _resolve_open_document_type(doc_type_hint, path_hint=path)
    with Session() as ps:
        document = ps.app.open(str(path), int(doc_type) if doc_type is not None else None, False)
        if document is not None:
            try:
                ps.active_document = document
            except Exception:
                pass
        return {
            "document": _document_to_dict(ps.active_document),
            "document_type": doc_type.name if doc_type else None,
            "smart_object": False,
        }


def open_document_as_smart_object(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    file_path = params.get("path") or params.get("file") or params.get("file_path")
    if not file_path:
        raise ValueError("Missing file path to open")
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    doc_type_hint = params.get("format") or params.get("type") or params.get("document_type")
    doc_type = _resolve_open_document_type(doc_type_hint, path_hint=path)
    with Session() as ps:
        document = ps.app.open(str(path), int(doc_type) if doc_type is not None else None, True)
        if document is not None:
            try:
                ps.active_document = document
            except Exception:
                pass
        return {
            "document": _document_to_dict(ps.active_document),
            "document_type": doc_type.name if doc_type else None,
            "smart_object": True,
        }


def save_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    with Session() as ps:
        doc = _ensure_document(ps)
        doc.save()
        return {"document": _document_to_dict(doc), "saved": True}


def _resolve_save_options(path: Path):
    ext = path.suffix.lower().lstrip('.')
    if ext in {"", "psd", "psb"}:
        return PhotoshopSaveOptions()
    if ext == "png":
        return PNGSaveOptions()
    if ext in {"jpg", "jpeg"}:
        opts = JPEGSaveOptions()
        opts.quality = 10
        return opts
    raise ValueError(f"Unsupported save format: {ext or 'psd'}")


def save_document_as(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    target = params.get("path") or params.get("file") or params.get("file_path")
    if not target:
        raise ValueError("Missing target path for save_as")
    path = Path(target).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with Session() as ps:
        doc = _ensure_document(ps)
        options = _resolve_save_options(path)
        doc.saveAs(str(path), options)
        return {"document": _document_to_dict(doc), "path": str(path)}


def save_document_copy(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    target = params.get("path") or params.get("file") or params.get("file_path")
    if not target:
        raise ValueError("Missing target path for save copy")
    path = Path(target).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with Session() as ps:
        doc = _ensure_document(ps)
        options = _resolve_save_options(path)
        doc.saveAs(str(path), options, asCopy=True)
        return {"document": _document_to_dict(doc), "path": str(path), "copy": True}


def revert_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    with Session() as ps:
        doc = _ensure_document(ps)
        reverted = False
        primary_error = None
        try:
            doc.revert()
            reverted = True
        except Exception as exc:
            primary_error = exc

        if not reverted:
            try:
                desc = ActionDescriptor()
                ref = ActionReference()
                ref.putEnumerated(
                    ps.app.charIDToTypeID("Docu"),
                    ps.app.charIDToTypeID("Ordn"),
                    ps.app.charIDToTypeID("Trgt"),
                )
                desc.putReference(ps.app.charIDToTypeID("null"), ref)
                ps.app.executeAction(ps.app.charIDToTypeID("Rvrt"), desc, ps.DialogModes.DisplayNoDialogs)
                reverted = True
            except Exception:
                pass

        if not reverted:
            try:
                ps.app.runMenuItem(ps.app.charIDToTypeID("Rvrt"))
                reverted = True
            except Exception as exc:
                raise RuntimeError("Failed to revert document via DOM or menu command") from exc if primary_error else exc

        return {"document": _document_to_dict(doc), "reverted": True}


def duplicate_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    new_name = params.get("name") or params.get("new_name")
    with Session() as ps:
        doc = _ensure_document(ps)
        duplicated = doc.duplicate(new_name) if new_name else doc.duplicate()
        return {"document": _document_to_dict(duplicated)}


def close_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    save = bool(params.get("save", False))
    with Session() as ps:
        doc = _ensure_document(ps)
        name = getattr(doc, "name", None)
        doc.close(SaveOptions.SaveChanges if save else SaveOptions.DoNotSaveChanges)
        return {"closed": name, "saved": save}


def close_all_documents(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    save = bool(params.get("save", False))
    with Session() as ps:
        names = []
        for doc in list(ps.app.documents):
            names.append(getattr(doc, "name", None))
            doc.close(SaveOptions.SaveChanges if save else SaveOptions.DoNotSaveChanges)
        return {"closed": names, "count": len(names), "saved": save}


def close_other_documents(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    save = bool(params.get("save", False))
    with Session() as ps:
        docs = list(ps.app.documents)
        if not docs:
            return {"closed": [], "count": 0, "saved": save}
        try:
            active = ps.active_document
            active_handle = getattr(active, "app", None)
        except Exception:
            active = None
            active_handle = None
        closed = []
        option = SaveOptions.SaveChanges if save else SaveOptions.DoNotSaveChanges
        for doc in docs:
            if active_handle is not None and getattr(doc, "app", None) is active_handle:
                continue
            name = getattr(doc, "name", None)
            doc.close(option)
            closed.append(name)
        return {"closed": closed, "count": len(closed), "saved": save}


def browse_in_bridge(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    target = params.get("path") or params.get("file")
    browse_path = None
    script = "app.browseInBridge();"
    if target:
        path = Path(target).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Path not found for Bridge: {path}")
        browse_path = path
        script = f"app.browseInBridge( new File('{_escape_js_string(str(path))}') );"
    with Session() as ps:
        ps.app.doJavaScript(script)
        return {"path": str(browse_path) if browse_path else None}


def close_and_browse_in_bridge(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    save = bool(params.get("save", False))
    target = params.get("path") or params.get("file")
    browse_path = None
    if target:
        browse_path = Path(target).expanduser()
        if not browse_path.exists():
            raise FileNotFoundError(f"Path not found for Bridge: {browse_path}")
    with Session() as ps:
        try:
            doc = ps.active_document
        except Exception:
            doc = None
        name = getattr(doc, "name", None) if doc else None
        if doc:
            doc.close(SaveOptions.SaveChanges if save else SaveOptions.DoNotSaveChanges)
        if browse_path:
            script = f"app.browseInBridge( new File('{_escape_js_string(str(browse_path))}') );"
        else:
            script = "app.browseInBridge();"
        ps.app.doJavaScript(script)
        return {"closed": name, "saved": save, "browse_path": str(browse_path) if browse_path else None}


def copy_selection(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    merge = bool(params.get("merge", False))
    with Session() as ps:
        doc = _ensure_document(ps)
        if merge:
            ps.app.runMenuItem(ps.app.charIDToTypeID("CpyM"))
        else:
            doc.selection.copy()
        return {"copied": True, "merge": merge}


def paste_to_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    with Session() as ps:
        doc = _ensure_document(ps)
        layer = doc.paste()
        return {"layer": _safe_layer_name(layer)}


def import_image_as_layer(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    file_path = params.get("path") or params.get("file")
    if not file_path:
        raise ValueError("Missing image path to import")
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    with Session() as ps:
        doc = _ensure_document(ps)
        temp = ps.app.load(str(path))
        temp.activeLayer.duplicate(doc, ps.ElementPlacement.PlaceAtBeginning)
        imported_name = _safe_layer_name(doc.activeLayer)
        temp.close(SaveOptions.DoNotSaveChanges)
        return {"layer": imported_name, "source": str(path)}


def replace_layer_with_file(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    file_path = params.get("path") or params.get("file")
    if not file_path:
        raise ValueError("Missing replacement file path")
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Replacement file not found: {path}")
    with Session() as ps:
        doc = _ensure_document(ps)
        active = doc.activeLayer
        try:
            desc = ActionDescriptor()
            desc.putPath(ps.app.charIDToTypeID("null"), str(path))
            event = ps.app.stringIDToTypeID("placedLayerReplaceContents")
            ps.app.executeAction(event, desc)
            return {"layer": _safe_layer_name(active), "replaced": str(path), "mode": "smart_object"}
        except Exception:
            active.remove()
            temp = ps.app.load(str(path))
            temp.activeLayer.duplicate(doc, ps.ElementPlacement.PlaceAtBeginning)
            temp.close(SaveOptions.DoNotSaveChanges)
            return {"layer": _safe_layer_name(doc.activeLayer), "replaced": str(path), "mode": "fallback"}


def remove_background_layer(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    with Session() as ps:
        doc = _ensure_document(ps)
        try:
            bg = doc.backgroundLayer
        except Exception:
            return {"removed": False, "reason": "no background layer"}
        name = getattr(bg, "name", "Background")
        doc.activeLayer = bg
        bg.remove()
        return {"removed": True, "layer": name}


def get_document_info(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    include_empty = bool(params.get("include_empty", False))
    with Session() as ps:
        doc = _ensure_document(ps)
        info = getattr(doc, "info", None)
        payload: Dict[str, Any] = {}
        if info:
            for field in _DOCUMENT_INFO_FIELDS:
                try:
                    value = getattr(info, field)
                except Exception:
                    value = None
                if value in (None, "", []):
                    if include_empty:
                        payload[field] = value
                    continue
                payload[field] = value
        return {"document": _document_to_dict(doc), "info": payload}


def print_document(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    show_dialogs = bool(params.get("show_dialogs", True))
    with Session() as ps:
        doc = _ensure_document(ps)
        original_mode = ps.app.displayDialogs
        try:
            if not show_dialogs:
                ps.app.displayDialogs = ps.DialogModes.DisplayNoDialogs
            doc.print()
        finally:
            if not show_dialogs:
                ps.app.displayDialogs = original_mode
        return {"document": _document_to_dict(doc), "show_dialogs": show_dialogs}


def print_one_copy(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    with Session() as ps:
        doc = _ensure_document(ps)
        doc.printOneCopy()
        return {"document": _document_to_dict(doc)}


def exit_photoshop(params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    save = bool(params.get("save", False))
    force = bool(params.get("force", False))
    with Session() as ps:
        if force:
            option = SaveOptions.SaveChanges if save else SaveOptions.DoNotSaveChanges
            for doc in list(ps.app.documents):
                doc.close(option)
        ps.app.doJavaScript("app.quit();")
        return {"save": save, "force": force, "status": "quit_requested"}
