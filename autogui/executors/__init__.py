from __future__ import annotations

import importlib
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


HOTKEY_SCRIPT = Path(__file__).resolve().parents[1] / "photoshop_hotkey_best.py"


@dataclass
class ExecResult:
    ok: bool
    return_code: int
    stdout: str = ""
    stderr: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)


def _run_subprocess(argv: List[str]) -> ExecResult:
    proc = subprocess.run(argv, capture_output=True, text=True)
    return ExecResult(
        ok=proc.returncode == 0,
        return_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        extra={"argv": argv},
    )


def run_hotkey(flags: List[str]) -> ExecResult:
    argv = [sys.executable, str(HOTKEY_SCRIPT)] + list(flags)
    return _run_subprocess(argv)


def run_python_script(script: Path, args: Optional[List[str]] = None) -> ExecResult:
    argv = [sys.executable, str(script)] + (args or [])
    return _run_subprocess(argv)


def run_do_javascript(template: str, params: Optional[Dict[str, Any]] = None) -> ExecResult:
    from photoshop import Session  # lazy import

    script = template.format(**(params or {}))
    try:
        with Session() as ps:
            ps.app.doJavaScript(script)
        return ExecResult(ok=True, return_code=0, stdout="", stderr="", extra={"jsx": script})
    except Exception as exc:  # pylint: disable=broad-except
        return ExecResult(ok=False, return_code=1, stdout="", stderr=str(exc), extra={"jsx": script})


def run_dom_api(callable_path: str, params: Optional[Dict[str, Any]] = None) -> ExecResult:
    module_name, func_name = callable_path.split(":") if ":" in callable_path else callable_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    try:
        result = func(params or {})
        return ExecResult(ok=True, return_code=0, stdout="", stderr="", extra={"result": result})
    except Exception as exc:  # pylint: disable=broad-except
        return ExecResult(ok=False, return_code=1, stdout="", stderr=str(exc), extra={})
