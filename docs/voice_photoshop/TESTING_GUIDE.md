# Photoshop API 完整测试指南

## 概述

本指南帮助您系统性地测试所有99个Photoshop API功能。

## 快速开始

### 方式1：一键测试所有功能
```bash
python quick_test.py
```

### 方式2：交互式测试
```bash
python test_all_functions.py
# 选择 1 (交互模式)
```

## 测试类别详情

### 1. 文档操作 (document) - 10个功能
**关键功能：**
- `new_document` - 创建新文档
- `save_as_png/jpeg/pdf/psd` - 保存为各种格式
- `open_document` - 打开文档
- `close_document` - 关闭文档

**测试命令：**
```
> test document
```

### 2. 图层操作 (layer) - 17个功能
**关键功能：**
- `duplicate_layer` - 复制图层
- `rename_layer` - 重命名图层
- `set_layer_blend_mode` - 设置混合模式
- `set_layer_opacity` - 设置不透明度
- `toggle_layer_visibility` - 切换可见性

**测试命令：**
```
> test layer
```

### 3. 选择操作 (selection) - 11个功能
**关键功能：**
- `select_all` - 全选
- `create_rectangular_selection` - 创建矩形选区
- `create_elliptical_selection` - 创建椭圆选区
- `fill_selection` - 填充选区
- `stroke_selection` - 描边选区

**测试命令：**
```
> test selection
```

### 4. 变换操作 (transform) - 8个功能
**关键功能：**
- `rotate_layer` - 旋转图层 ✅ 已有验证
- `flip_horizontal` - 水平翻转
- `flip_vertical` - 垂直翻转
- `scale_layer` - 缩放图层

**测试命令：**
```
> test transform
```

### 5. 图像调整 (adjustment) - 12个功能
**关键功能：**
- `brightness_contrast` - 亮度/对比度
- `hue_saturation` - 色相/饱和度
- `color_balance` - 色彩平衡
- `levels` - 色阶
- `auto_tone` - 自动色调

**测试命令：**
```
> test adjustment
```

### 6. 滤镜效果 (filter) - 25个功能
**关键功能：**
- `smart_sharpen` - 智能锐化 ✅ 已有验证
- `gaussian_blur` - 高斯模糊
- `emboss` - 浮雕
- `pixelate_mosaic` - 马赛克
- `noise_add` - 添加杂色

**测试命令：**
```
> test filter
```

### 7. 形状绘制 (shape) - 8个功能
**关键功能：**
- `create_rectangle` - 创建矩形 ✅ 已有验证
- `create_circle` - 创建圆形
- `create_ellipse` - 创建椭圆
- `create_star` - 创建星形
- `create_polygon` - 创建多边形

**测试命令：**
```
> test shape
```

### 8. 文本操作 (text) - 11个功能
**关键功能：**
- `create_text` - 创建文本
- `set_text_font` - 设置字体
- `set_text_size` - 设置字号
- `set_text_color` - 设置颜色
- `warp_text` - 变形文字

**测试命令：**
```
> test text
```

## 常用测试命令

### 单个功能测试
```bash
# 测试智能锐化
> test smart_sharpen

# 测试新建文档
> test new_document_default

# 测试创建矩形
> test create_rectangle

# 测试旋转图层
> test rotate_layer_45
```

### 类别测试
```bash
# 测试所有滤镜
> test filter

# 测试所有文档操作
> test document

# 测试所有形状绘制
> test shape
```

### 查看功能列表
```bash
# 列出所有滤镜功能
> list filter

# 列出所有文档操作
> list document

# 列出所有形状功能
> list shape
```

### 生成报告
```bash
# 查看测试报告
> report
```

## 测试结果解读

### 成功示例
```
✅ 测试: new_document_default
  动作: new_document
  参数: {}
  ✅ 成功 (0.123s)
```

### 失败示例
```
❌ 测试: open_document
  动作: open_document
  参数: {"path": "D:/test.jpg"}
  ❌ 失败: 文件未找到或路径无效
```

### 模拟模式 vs 真实模式

**模拟模式 (Photoshop未运行):**
```
[WARNING] Photoshop模块未找到，将运行模拟模式
✅ 成功 (0.001s) - 模拟执行: new_document
```

**真实模式 (Photoshop已运行):**
```
[INFO] 连接到Photoshop成功
✅ 成功 (0.456s) - 新文档创建: 800x600 (Untitled)
```

## 验证检查清单

### 核心功能验证 (必须)
- [ ] `smart_sharpen` - 智能锐化
- [ ] `new_document` - 新建文档
- [ ] `rotate_layer` - 旋转图层
- [ ] `create_rectangle` - 创建矩形

### 高级功能验证 (建议)
- [ ] `save_as_png` - 保存PNG
- [ ] `create_circle` - 创建圆形
- [ ] `set_layer_blend_mode` - 设置混合模式
- [ ] `create_text` - 创建文本
- [ ] `gaussian_blur` - 高斯模糊
- [ ] `emboss` - 浮雕

### 专业功能验证 (可选)
- [ ] `warp_text` - 变形文字
- [ ] `motion_blur` - 动感模糊
- [ ] `pixelate_mosaic` - 马赛克
- [ ] `auto_tone` - 自动色调
- [ ] `convert_to_smart_object` - 转换为智能对象

## 错误排查

### 常见问题

1. **"未找到测试: all"**
   - 已在最新版本修复，使用 `test all`

2. **"Photoshop未运行"**
   - 这是正常的，会运行模拟模式
   - 要测试真实API，请先启动Photoshop

3. **"文件未找到"**
   - 检查文件路径是否正确
   - 或使用模拟模式测试

4. **编码错误**
   - 确保使用UTF-8编码
   - Windows建议使用PowerShell或VSCode终端

### 获取帮助
```bash
# 在交互模式中
> help

# 或在主菜单选择 4
```

## 测试报告样例

```
========================================
Photoshop API 完整功能测试报告
========================================

测试时间: 2025-11-06 14:30:00

总体统计:
---------
总测试数: 99
成功: 85 (85.9%)
失败: 14 (14.1%)

========================================
按类别统计:
========================================

文档操作 (document):
  总计: 9
  成功: 9 (100.0%)
  失败: 0 (0.0%)

图层操作 (layer):
  总计: 17
  成功: 15 (88.2%)
  失败: 2 (11.8%)

...
```

## 总结

- **总功能数**: 99个
- **涵盖类别**: 8个
- **推荐测试**: 方式1 (快速测试) + 方式2 (交互测试)
- **验证重点**: 先验证4个已有功能，再验证其他核心功能

立即开始测试：
```bash
python quick_test.py
```
