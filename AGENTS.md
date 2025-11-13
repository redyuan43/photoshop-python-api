# Repository Guidelines

## Project Structure & Module Organization
The core package lives in `photoshop/` (COM bridge abstractions, version file, helpers). Automation helpers and screenshots land in `autogui/`, while end-to-end demos and CLI snippets live under `examples/` and `voice_photoshop/`. Tests are split between legacy `test/` smoke cases and the newer `tests/` suite; keep new coverage in `tests/` unless you are refactoring older files. MkDocs content sits in `docs/`, and configuration samples such as `config.example.py` plus API key docs in the repository root guide local secrets. Treat generated artifacts (`autogui/shots/`, build outputs) as throwaway and keep them out of commits.

## Build, Test, and Development Commands
Install everything with `poetry install`, then run tools through Poetry to keep the venv isolated: `poetry run python examples/basic.py` highlights API usage, `poetry run pre-commit run --all-files` enforces lint hooks, and `poetry build` creates distributable wheels. Use `poetry run verify_config.py` before sharing configs to ensure keys are masked.

## Coding Style & Naming Conventions
All Python code is auto-formatted via Black (line length 120) and import-sorted with isort’s Black profile; stick to four-space indents, snake_case functions, and UpperCamelCase classes. Keep module names short and descriptive (e.g., `layers_service.py`). Static analysis relies on Flake8, Pylint, and optional mypy; run `poetry run pre-commit` before committing to stay consistent.

## Testing Guidelines
Pytest backs the suite; name files `test_<feature>.py` and test functions `test_<behavior>`. Prefer placing fixtures in `tests/conftest.py`. Run `poetry run pytest` for the full suite or `poetry run pytest tests/test_layers.py -k export` for targeted checks. New features should ship with regression tests and maintain the “high coverage” bar described in `README.md`; add `pytest-cov` flags when validating metrics locally.

## Commit & Pull Request Guidelines
Commits follow Conventional Commits and are enforced by Commitizen; run `poetry run cz commit` for prompts (e.g., `feat: add smart-object unlock helper`). Reference related issues in the body. PRs should describe intent, summarize testing (`pytest`, manual Photoshop steps), and attach screenshots or screen recordings when UI automation is affected. Ensure CI is green and reviewers have reproduction notes.

## Security & Configuration Tips
Never commit raw API tokens or Photoshop credentials. Duplicate `config.example.py` into `config.py`, set keys through environment variables when possible, and document any sensitive setup in `API_KEYS_SETUP.md`. Run `poetry run python verify_config.py` before pushing to confirm that secrets remain redacted.
