# Photoshop 语音控制系统

基于真实 Photoshop API 的语音控制实现，将自然语言转换为 Photoshop 操作。

## 核心功能

### 已实现功能（4个）

1. **智能锐化** - 基于 `tests/test_48_smart_sharpen.py` 和 `examples/session_smart_sharpen.py`
2. **新建文档** - 基于 Photoshop API
3. **旋转图层** - 基于 `tests/test_20_rotate_layer.py`
4. **创建矩形框** - 基于 `tests/test_02_create_new_document.py`

## 使用方法

### 测试模式（显示API代码）
```bash
python test_api_calls.py "锐化图像"
python test_api_calls.py "新建文档"
python test_api_calls.py "旋转图层45度"
python test_api_calls.py "创建矩形框"
```

### 实际执行模式
```bash
python voice_to_api_REAL.py "锐化图像"
python voice_to_api_REAL.py "新建文档"
python voice_to_api_REAL.py "旋转图层45度"
python voice_to_api_REAL.py "创建矩形框"
```

## 技术实现

### 真实API调用

基于 `tests/` 目录中的测试文件和 `examples/` 目录中的示例代码：

- **智能锐化：** 使用 Action Manager（`session_smart_sharpen.py`）
- **旋转图层：** 处理背景图层锁定问题（`test_20_rotate_layer.py`）
- **矩形框：** 使用 Selection API（`test_02_create_new_document.py`）
- **新建文档：** 直接调用 Photoshop API

### 系统架构

```
自然语言 -> 解析器 -> API调用生成器 -> Photoshop API
```

1. 解析自然语言命令
2. 提取参数（尺寸、位置、角度等）
3. 生成真实API调用代码
4. 通过 `photoshop-python-api` 执行

## 扩展计划

基于 `tests/` 目录继续扩展：
- 文本添加（test_01_hello_world.py）
- 图层操作（test_21_convert_smartobject.py）
- 滤镜应用（test_45_apply_filters.py, test_46_apply_crystallize_filter_action.py）
- 色彩调整（test_26_color.py）
- 保存/导出（test_37_export_document.py）

## 文件说明

- `voice_to_api_REAL.py` - 主要实现文件，包含所有4个功能的真实API调用
- `test_api_calls.py` - 测试工具，显示将要执行的API代码
- `ALL_4_FEATURES_WORKING.md` - 详细功能列表和测试结果

## 许可证

与 photoshop-python-api 项目相同。
