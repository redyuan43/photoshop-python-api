# Photoshop Tool Mapping Guide

> Data captured via `python enumerate_tools.py --json`. LLM workflows can reference this table to translate natural-language requests into CLI flags (`--tool` / `--tool-cycle`) and then verify the active tool with `get_current_tool.py`.

| CLI flag (`--tool`) | Default hotkey | Typical tools in this group | `currentTool` names (cycle order) | | Variant hints & synonyms |
| --- | --- | --- | --- | --- |
| `move` | V | Move tool, Artboard tool | `moveTool`, `artboardTool` | moveTool (Move), artboardTool (Artboard) | moveTool (move), artboardTool (artboard) |
| `marquee` | M | Rectangular/Elliptical marquee | `marqueeRectTool`, `marqueeEllipTool` | marqueeRectTool (Rectangular), marqueeEllipTool (Elliptical) | marqueeRectTool (rectangular), marqueeEllipTool (elliptical) |
| `lasso` | L | Lasso, polygonal lasso, magnetic lasso, selection brush | `lassoTool`, `magneticLassoTool`, `polySelTool`, `selectionBrushTool` | lassoTool, magneticLassoTool, polySelTool, selectionBrushTool | lassoTool, magneticLassoTool, polySelTool, selectionBrushTool |
| `magic_wand` | W | Magic wand, quick selection, object selection | `magicWandTool`, `quickSelectTool`, `magicLassoTool` | magicWandTool (Magic wand), quickSelectTool, magicLassoTool | magicWandTool (magic wand), quickSelectTool, magicLassoTool |
| `crop` | C | Crop, perspective crop, slice, slice select | `cropTool`, `perspectiveCropTool`, `sliceTool`, `sliceSelectTool` | cropTool, perspectiveCropTool, sliceTool, sliceSelectTool | cropTool, perspectiveCropTool, sliceTool, sliceSelectTool |
| `eyedropper` | I | Eyedropper, color sampler, ruler, note, count | `eyedropperTool`, `colorSamplerTool`, `rulerTool`, `textAnnotTool`, `countTool` | eyedropperTool, colorSamplerTool, rulerTool, textAnnotTool, countTool | eyedropperTool, colorSamplerTool, rulerTool, textAnnotTool, countTool |
| `spot_heal` | J | Spot/healing brush, patch, content-aware move, remove, red eye | `spotHealingBrushTool`, `patchSelection`, `recomposeSelection`, `removeTool`, `redEyeTool`, `magicStampTool` | spotHealingBrushTool, patchSelection, recomposeSelection, removeTool, redEyeTool, magicStampTool | spotHealingBrushTool, patchSelection, recomposeSelection, removeTool, redEyeTool, magicStampTool |
| `clone_stamp` | S | Clone stamp, pattern stamp | `cloneStampTool`, `patternStampTool` | cloneStampTool, patternStampTool | cloneStampTool, patternStampTool |
| `history_brush` | Y | History brush, art history brush | `historyBrushTool`, `artBrushTool` | historyBrushTool, artBrushTool | historyBrushTool, artBrushTool |
| `eraser` | E | Eraser, background eraser, magic eraser | `eraserTool`, `backgroundEraserTool`, `magicEraserTool` | eraserTool, backgroundEraserTool, magicEraserTool | eraserTool, backgroundEraserTool, magicEraserTool |
| `paint_bucket` | G | Paint bucket, gradient | `bucketTool`, `gradientTool` | bucketTool (Paint bucket), gradientTool (Gradient fill) | bucketTool (paint bucket), gradientTool (gradient fill) |
| `dodge` | O | Dodge, burn, sponge | `dodgeTool`, `burnInTool`, `saturationTool` | dodgeTool (Dodge), burnInTool (Burn), saturationTool (Sponge) | dodgeTool (dodge), burnInTool (burn), saturationTool (sponge) |
| `pen` | P | Pen, freeform pen, curvature pen | `penTool`, `freeformPenTool`, `curvaturePenTool` | penTool, freeformPenTool, curvaturePenTool | penTool, freeformPenTool, curvaturePenTool |
| `type` | T | Horizontal/vertical type, type masks | `typeCreateOrEditTool`, `typeVerticalCreateOrEditTool`, `typeCreateMaskTool`, `typeVerticalCreateMaskTool` | typeCreateOrEditTool (Horizontal type), typeVerticalCreateOrEditTool (Vertical type), typeCreateMaskTool, typeVerticalCreateMaskTool | typeCreateOrEditTool (horizontal type), typeVerticalCreateOrEditTool (vertical type), typeCreateMaskTool, typeVerticalCreateMaskTool |
| `path_select` | A | Path selection / direct selection | `pathComponentSelectTool`, `directSelectTool` | pathComponentSelectTool (Path selection), directSelectTool (Direct selection) | pathComponentSelectTool (path selection), directSelectTool (direct selection) |
| `shape` | U | Rectangle, ellipse, triangle, polygon, line, custom shape | `rectangleTool`, `ellipseTool`, `triangleTool`, `polygonTool`, `lineTool`, `customShapeTool` | rectangleTool, ellipseTool, triangleTool, polygonTool, lineTool, customShapeTool | rectangleTool, ellipseTool, triangleTool, polygonTool, lineTool, customShapeTool |
| `hand` | H | Hand tool | `handTool` | handTool (Hand/Pan) | handTool |
| `rotate_view` | R | Rotate view tool | `rotateTool` | rotateTool | rotateTool |
| `zoom` | Z | Zoom tool | `zoomTool` | zoomTool | zoomTool |


## Usage Tips

1. **Switch tools**
   ```bash
   python photoshop_hotkey_best.py --tool magic_wand
   python photoshop_hotkey_best.py --tool-cycle magic_wand  # cycle to quick select / object select
   ```

2. **Verify the active tool**
   ```bash
   python get_current_tool.py  # e.g., prints quickSelectTool
   ```

3. **Batch enumeration (for LLM planners)**
   ```bash
   python enumerate_tools.py --json          # includes Shift cycles
   python enumerate_tools.py --primary-only  # only primary hotkeys
   ```

Re-run the enumeration when Photoshop updates tool variants to refresh this mapping.

## Additional Shortcut Commands

The following actions live in `photoshop_hotkey_best.py` and can be triggered via CLI flags or by `tool_llm_runner.py` when a toolbar tool is not the best answer.

| Action ID | CLI flag(s) | Description | Shortcut |
| --- | --- | --- | --- |
| reset | *(default)* | Reset workspace (Alt+W, K, R) | Alt+W → K → R |
| layer_up | `--layer-up` | Move layer up | Ctrl+} |
| layer_down | `--layer-down` | Move layer down | Ctrl+{ |
| duplicate | `--duplicate` | Duplicate layer | Ctrl+J |
| selection_layer_up | `--selection-layer-up` | Select previous layer | Alt+] |
| selection_layer_down | `--selection-layer-down` | Select next layer | Alt+[ |
| selection_layer_up | `--selection-layer-up` | Select previous layer | Alt+] |
| selection_layer_down | `--selection-layer-down` | Select next layer | Alt+[ |
| selection_layer_up | `--selection_layer_up` | Move layer up | Alt+] |
| selection_layer_down | `--selection_layer_down` | Move layer down | Alt+[ |
| selection_up | `--selection-up` | Nudge selection upward | Ctrl+↑ |
| selection_down | `--selection-down` | Nudge selection downward | Ctrl+↓ |
| selection_left | `--selection-left` | Nudge selection left | Ctrl+← |
| selection_right | `--selection-right` | Nudge selection right | Ctrl+→ |
| select_all | `--select-all` | Select all | Ctrl+A |
| deselect | `--deselect` | Deselect | Ctrl+D |
| invert | `--invert` | Invert selection | Ctrl+Shift+I |

| file_new | `--file-new` | New document | Ctrl+N |
| file_open | `--file-open` | Open document | Ctrl+O |
| file_save | `--file-save` | Save document | Ctrl+S |
| file_save_as | `--file-save-as` | Save As | Ctrl+Shift+S |
| export_as | `--export-as` | Export As | Ctrl+Alt+Shift+W |
| file_close | `--file-close` | Close current document | Ctrl+W |
| file_close_all | `--file-close-all` | Close all documents | Ctrl+Alt+W |
| undo | `--undo` | Undo last action | Ctrl+Z |
| screenshot | `python screenshot_photoshop.py --out shots/<timestamp>.png` | Capture the current Photoshop window screenshot | Taskbar activation + window capture |

`tool_llm_runner.py` considers both the tool table and this command list when translating natural-language instructions into actual Photoshop hotkeys.
