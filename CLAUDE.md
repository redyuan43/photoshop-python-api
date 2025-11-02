# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python API for Adobe Photoshop that enables programmatic control of Photoshop functionality using Python. The project uses COM (Component Object Model) to communicate with Photoshop on Windows platforms, making it possible to automate Photoshop tasks, manipulate documents, layers, and execute Photoshop operations programmatically.

## Key Architecture

### Core Components

- **`photoshop/api`**: Main API module containing all Photoshop object wrappers
  - `application.py`: Root Photoshop application object (entry point for all operations)
  - `_document.py`, `_artlayer.py`: Core document and layer objects
  - `colors/`: Color space implementations (RGB, CMYK, HSB, Lab, Gray)
  - `save_options/`, `open_options/`: File format options for import/export
  - `enumerations.py`, `constants.py`: Photoshop constants and enums
  - `errors.py`: Custom exception handling

- **`photoshop/session.py`**: Context manager class for Photoshop sessions
  - Provides convenient workflow management
  - Handles document operations (open, new, duplicate)
  - Manages application state and cleanup

- **COM Integration**: Uses `comtypes` library for Windows COM communication
  - All API objects inherit from `photoshop.api._core.Photoshop` base class
  - Handles COM object lifecycle and error management

### Usage Patterns

1. **Direct API Access**:
   ```python
   import photoshop.api as ps
   app = ps.Application()
   doc = app.documents.add()
   ```

2. **Session Context** (Recommended for most use cases):
   ```python
   from photoshop import Session
   with Session(action="new_document") as ps:
       doc = ps.active_document
       # Photoshop operations here
   ```

## Development Commands

### Environment Setup
```bash
# Install dependencies using Poetry
poetry install

# Install pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=photoshop

# Run specific test file
pytest tests/test_specific.py
```

### Code Quality
```bash
# Format code with Black
black photoshop/ tests/

# Sort imports with isort
isort photoshop/ tests/

# Lint with flake8
flake8 photoshop/ tests/

# Type checking with mypy
mypy photoshop/
```

### Documentation
```bash
# Build documentation locally
mkdocs serve

# Build static documentation
mkdocs build
```

## Important Implementation Details

### Windows-Only Limitation
This project only works on Windows due to COM dependency. All development and testing must be done on Windows with Photoshop installed.

### Photoshop Version Support
Supports Photoshop versions CC2017 through 2025. The API automatically detects installed Photoshop versions and can target specific versions using the `version` parameter in `Application()`.

### COM Object Management
- All Photoshop objects are COM wrappers that must be properly managed
- Objects inherit from base `Photoshop` class which handles COM communication
- Use context managers (`with` statements) when possible for automatic cleanup
- Be careful about object lifetime - COM objects can cause memory leaks if not properly released

### Error Handling
- `PhotoshopPythonAPIError`: General API errors
- `PhotoshopPythonAPICOMError`: COM-related communication errors
- Always catch these specific exceptions rather than generic ones

### Session Management
The `Session` class provides the most convenient workflow:
- Automatically handles document creation/opening
- Provides direct access to all API classes through the session object
- Manages cleanup and optional auto-close functionality
- Supports callbacks for custom cleanup logic

## Development Guidelines

### Adding New Features
1. Check if the feature exists in Photoshop's COM interface first
2. Create new wrapper classes in `photoshop/api/` following existing patterns
3. Add new enumerations/constants to appropriate files
4. Include comprehensive docstrings with examples
5. Add tests if possible (note: tests require Photoshop to be running)

### Code Style
- Follow Google Python Style Guide
- 120 character line length max
- Use double quotes for strings
- Comprehensive docstrings for all public methods and classes
- Type hints for all function signatures

### Testing Considerations
- Tests require Photoshop to be installed and running
- Many tests need to be integration tests due to COM dependency
- Use mocking judiciously for COM-independent logic
- Test both direct API usage and Session context patterns

## Common Patterns

### Creating New Documents
```python
# Direct API
app = ps.Application()
doc = app.documents.add(width=800, height=600, resolution=72, name="MyDoc")

# Session context
with Session(action="new_document") as ps:
    doc = ps.active_document
```

### Working with Layers
```python
# Access layers
active_layer = doc.activeLayer
art_layers = doc.artLayers
layer_sets = doc.layerSets

# Create new layer
new_layer = art_layers.add()
new_layer.kind = ps.LayerKind.TextLayer
```

### Saving Documents
```python
# Save with options
options = ps.JPEGSaveOptions(quality=8)
doc.saveAs("path/to/file.jpg", options, asCopy=True)
```