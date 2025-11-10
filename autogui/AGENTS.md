# Repository Guidelines

## Project Structure & Module Organization
`photoshop_hotkey_best.py` is the single entry point that contains window discovery, activation, and every hotkey routine; keep new automation helpers close to it or extract them into small modules inside `autogui/` only when reuse is clear. Documentation artifacts (`README.md`, `QUICK_START.md`, `SUMMARY.md`, `COMPLETE.md`, `FINAL.md`, `PARAMETERS.md`) double as test evidence, so update them whenever behavior changes. Avoid committing PSDs, logs, or temporary scripts; stash that material outside the repo.

## Build, Test, and Development Commands
- `py -3 -m venv .venv; .\.venv\Scripts\activate` - create an isolated environment for pywinauto/pyautogui.
- `pip install pywinauto pyautogui pygetwindow` - install the only runtime dependencies until a requirements file is introduced.
- `python photoshop_hotkey_best.py --help` - verify CLI wiring and discover flags.
- `python photoshop_hotkey_best.py --layer-move` (or `--selection-up`, `--select-all`) - run an end-to-end smoke test against an open Photoshop window.

## Coding Style & Naming Conventions
Use Python 3.10+, 4-space indentation, and UTF-8 files. Follow the existing naming pattern: verb-based helpers (`send_layer_move_hotkeys`), snake_case variables, and hyphenated CLI flags wired via argparse. Keep docstrings imperative and log messages concise. When platform-specific code is added, guard imports with `if sys.platform.startswith("win"):`. Prefer `black` (line length 100) plus `ruff` or `flake8` before large refactors.

## Testing Guidelines
Automated tests are not present yet, so treat manual passes as required deliverables. For every new option capture: command used, console output, detection of the Photoshop window, and observed action (e.g., layer moved). Cover three scenarios before opening a PR: default reset (`python photoshop_hotkey_best.py`), bidirectional layer moves (`--layer-move`), and at least one selection or select-all command. Document anomalies in `SUMMARY.md` or the PR body.

## Commit & Pull Request Guidelines
Commits use `type: summary` (see `feat: 清理项目并准备GitHub提交`) and should remain focused on one behavior. Pull requests must include a short description, checklist of affected CLI flags, manual test log snippets, screenshots or GIFs if UI state changed, and links to issues/tasks. Call out any dependency changes or new Windows permissions.

## Security & Configuration Tips
Automation assumes Windows with Photoshop already running; fail fast with clear errors when the window is missing. Never hard-code user paths or document names, and pass them via arguments or configuration files kept out of VCS. Leave `pyautogui.FAILSAFE` enabled and add brief sleeps after focus changes to prevent runaway inputs. When editing the regex list in `find_photoshop_window()`, test against both Chinese and English UI titles to avoid missing localized builds.
