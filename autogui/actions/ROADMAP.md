# Action Registry Roadmap

Status legend: ✅ done | 🟡 in progress | ⬜ pending

## Documents & Sessions
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_01_hello_world.py, test_05_session_hello_world.py | basic Session connectivity | builtin (no action) | ✅ |
| test_02_create_new_document.py, test_03_new_document.py, test_11_session_new_document.py | create new document | new_document | ✅ |
| test_04_photoshop_session.py, test_06_list_documents.py, test_07_get_document_by_name.py | list/query open documents | `list_documents`, `open_document` | ✅ |
| test_08_open_psd.py | open PSD by path | open_document | ✅ |
| test_09_save_to_psd.py, test_42_save_as_pdf.py, test_43_save_as_tga.py | save / save-as | `save_document_dom`, `save_document_as` | ✅ |
| test_10_revert_changes.py | revert active document | revert_document | ✅ |
| test_12_session_document_duplicate.py | duplicate document | duplicate_document | ✅ |
| test_99_close_all_documents.py | close active / all | close_document, close_all_documents, close_other_documents | ✅ |

## View & Navigation
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_13_fit_on_screen.py | fit on screen | 
it_screen | ✅ |
| test_35_current_tool.py | report current tool | status_snapshot / legacy | ✅ |

## Smart Objects & Layers
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_20_rotate_layer.py, test_52_crop_and_rotate.py | rotate layer | TBD (
otate_layer) | ⬜ |
| test_21_convert_smartobject_* | convert smart object | `convert_layer_to_smart_object`, `rasterize_layer` | ✅ |
| test_22_operate_layerSet.py | manipulate layer sets | list_layers, ctivate_layer_*, future grouping actions | 🟡 |
| test_23_copy_and_paste.py | copy/paste layers | copy_layer, paste_layer | ⬜ |
| test_24_import_image_as_layer.py | import file as new layer | import_image_layer | ⬜ |
| test_25_replace_images.py | replace smart object contents | 
eplace_smart_object | ⬜ |
| test_53_background_removal.py | remove background layer | 
emove_background | ⬜ |

## Selection & Masks
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_29_fill_selection.py, test_30_delete_and_fill_selection.py | fill/delete selections | 
ill_selection, delete_and_fill | ⬜ |
| test_31_selection_stroke.py | stroke selection | stroke_selection | ⬜ |
| test_32_load_selection.py | load selection by channel | load_selection | ⬜ |

## Cropping & Canvas
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_33_cropping.py, test_52_crop_and_rotate.py | crop canvas | crop_document | ⬜ |
| test_34_trim.py | trim transparent edges | 	rim_document | ⬜ |

## Color & Adjustments
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_26_color.py, test_27_change_color_of_background_and_foreground.py | set foreground/background color | set_foreground_color, set_background_color | ⬜ |
| test_28_compare_colors.py | compare color values | compare_colors | ⬜ |
| test_36_toggle_proof_colors.py | toggle proof colors | 	oggle_proof_colors | ⬜ |
| test_26_color.py (SolidColor), test_45_apply_filters.py etc. | create SolidColor adjustments | pply_color_adjustment | ⬜ |

## Filters & Effects
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_45_apply_filters.py, test_48_smart_sharpen.py, test_49_session_smart_sharpen.py | built-in filters | pply_gaussian_blur (✅), pply_smart_sharpen, pply_filter presets | 🟡 |
| test_46_apply_crystallize_filter_action.py, test_47_emboss_action.py, test_50_add_slate.py | run Photoshop actions | hue_preset, 
un_action | 🟡 |

## Export & Automation
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_37_export_document.py, test_38_export_document_with_options.py | export document formats | export_document | ⬜ |
| test_39_export_layers_as_png.py, test_40_export_layers_use_export_options_saveforweb.py | export layers | export_layers | ⬜ |
| test_41_export_artboards.py | export artboards | export_artboards | ⬜ |
| test_44_create_thumbnail.py | create thumbnails | create_thumbnail | ⬜ |
| test_51_gui_tool_example.py | GUI automation sample (legacy) | rely on hotkey runner | ✅ |

## Status & Utilities
| Tests | Capability | Planned Action IDs | Status |
| --- | --- | --- | --- |
| test_35_current_tool.py | report active tool | status_snapshot | ✅ |
| test_10_revert_changes.py | revert active document | revert_document | ✅ |

## Next Steps
1. **Documents batch**: implement list_documents, get_document, open_document, save_document, close_document actions + DOM helpers.
2. **Layer utilities**: finish grouping actions (list_layers done; next: group toggles, duplicate, rotate, smart object helpers).
3. **Selections & colors**: map selection / color tests to actions.
4. **Exports & filters**: wrap export/filter demos with reusable DOM executors.

This file will be updated as each action lands in utogui/actions/actions.yaml.


