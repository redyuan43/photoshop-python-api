# Photoshop Python API 功能验证指南

## 🚀 快速开始

### 环境要求
- Windows 10/11
- Adobe Photoshop CC 2017 或更高版本
- Python 3.8+
- 管理员权限（用于COM接口访问）

### 安装与设置
```bash
# 安装 API
pip install photoshop-python-api

# 克隆项目获取示例代码
git clone https://github.com/loonghao/photoshop-python-api.git
cd photoshop-python-api

# 安装开发依赖
poetry install
```

## 🧪 功能验证清单

### 1️⃣ 基础连接测试 (必须先通过)
```python
# test_basic_connection.py
import photoshop.api as ps

try:
    app = ps.Application()
    print(f"✅ Photoshop 连接成功!")
    print(f"📱 Photoshop 版本: {app.version}")
    print(f"🎨 当前工具: {app.currentTool}")
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print("🔧 解决方案:")
    print("1. 确保 Photoshop 已打开")
    print("2. 以管理员身份运行 Python")
    print("3. 检查 Photoshop 版本兼容性")
```

### 2️⃣ 文档操作验证
```python
# test_document_operations.py
import photoshop.api as ps
import os

def test_document_operations():
    app = ps.Application()

    # 创建新文档
    doc = app.documents.add(800, 600, 72, "测试文档")
    print("✅ 创建新文档成功")

    # 测试文档属性
    print(f"📏 文档尺寸: {doc.width} x {doc.height}")
    print(f"🎨 颜色模式: {doc.mode}")
    print(f"📊 分辨率: {doc.resolution}")

    # 保存文档
    save_path = os.path.expanduser("~/Desktop/test_doc.psd")
    doc.saveAs(save_path)
    print(f"💾 文档保存成功: {save_path}")

    # 关闭文档
    doc.close()
    print("🔒 文档关闭成功")

if __name__ == "__main__":
    test_document_operations()
```

### 3️⃣ 图层操作验证
```python
# test_layer_operations.py
import photoshop.api as ps

def test_layer_operations():
    app = ps.Application()
    doc = app.documents.add(800, 600, 72, "图层测试")

    # 添加普通图层
    layer1 = doc.artLayers.add()
    layer1.name = "背景层"
    print("✅ 添加普通图层成功")

    # 添加文本图层
    layer2 = doc.artLayers.add()
    layer2.kind = ps.LayerKind.TextLayer
    layer2.name = "文本层"
    layer2.textItem.contents = "Hello Photoshop!"
    print("✅ 添加文本图层成功")

    # 测试图层属性
    print(f"👁️ 图层可见性: {layer1.visible}")
    print(f"🎭 混合模式: {layer1.blendMode}")
    print(f"💧 不透明度: {layer1.opacity}")

    # 图层操作
    layer1.opacity = 50
    layer1.visible = False
    print("✅ 图层属性修改成功")

    # 保存并关闭
    doc.saveAs(os.path.expanduser("~/Desktop/layer_test.psd"))
    doc.close()

if __name__ == "__main__":
    test_layer_operations()
```

### 4️⃣ 颜色操作验证
```python
# test_color_operations.py
import photoshop.api as ps

def test_color_operations():
    app = ps.Application()
    doc = app.documents.add(400, 400, 72, "颜色测试")

    # RGB 颜色测试
    red_color = ps.SolidColor()
    red_color.rgb.red = 255
    red_color.rgb.green = 0
    red_color.rgb.blue = 0
    print("✅ RGB 颜色创建成功")

    # CMYK 颜色测试
    cmyk_color = ps.SolidColor()
    cmyk_color.cmyk.cyan = 50
    cmyk_color.cmyk.magenta = 30
    cmyk_color.cmyk.yellow = 20
    cmyk_color.cmyk.black = 10
    print("✅ CMYK 颜色创建成功")

    # 应用颜色到背景
    doc.backgroundColor = red_color
    print("✅ 背景色设置成功")

    # 保存测试
    doc.saveAs(os.path.expanduser("~/Desktop/color_test.psd"))
    doc.close()

if __name__ == "__main__":
    test_color_operations()
```

### 5️⃣ 选择工具验证
```python
# test_selection_operations.py
import photoshop.api as ps

def test_selection_operations():
    app = ps.Application()
    doc = app.documents.add(800, 600, 72, "选择测试")

    # 创建矩形选择
    selection = doc.selection
    selection.select([(100, 100), (300, 100), (300, 300), (100, 300)])
    print("✅ 矩形选择创建成功")

    # 填充选择
    fill_color = ps.SolidColor()
    fill_color.rgb.blue = 255
    selection.fill(fill_color)
    print("✅ 选择区域填充成功")

    # 扩展选择
    selection.expand(10)
    print("✅ 选择扩展成功")

    # 羽化选择
    selection.feather(5)
    print("✅ 选择羽化成功")

    # 清除选择
    selection.deselect()
    print("✅ 选择清除成功")

    doc.saveAs(os.path.expanduser("~/Desktop/selection_test.psd"))
    doc.close()

if __name__ == "__main__":
    test_selection_operations()
```

### 6️⃣ 滤镜效果验证
```python
# test_filter_operations.py
import photoshop.api as ps

def test_filter_operations():
    app = ps.Application()
    doc = app.documents.add(400, 400, 72, "滤镜测试")

    # 创建一个图层用于测试滤镜
    layer = doc.artLayers.add()

    # 添加噪点滤镜
    layer.applyAddNoise(10, ps.NoiseDistribution.GAUSSIAN, False)
    print("✅ 添加杂色滤镜成功")

    # 应用高斯模糊
    layer.applyGaussianBlur(2.0)
    print("✅ 高斯模糊滤镜成功")

    # 应用浮雕效果
    layer.applyEmboss(135, 5, 100, 100)
    print("✅ 浮雕滤镜成功")

    doc.saveAs(os.path.expanduser("~/Desktop/filter_test.psd"))
    doc.close()

if __name__ == "__main__":
    test_filter_operations()
```

### 7️⃣ 文件导出验证
```python
# test_export_operations.py
import photoshop.api as ps
import os

def test_export_operations():
    app = ps.Application()
    doc = app.documents.add(800, 600, 72, "导出测试")

    # 添加一些内容
    layer = doc.artLayers.add()
    text_color = ps.SolidColor()
    text_color.rgb.green = 255
    layer.kind = ps.LayerKind.TextLayer
    layer.textItem.contents = "Export Test"
    layer.textItem.size = 40

    desktop = os.path.expanduser("~/Desktop/")

    # 导出为 JPEG
    jpeg_options = ps.JPEGSaveOptions(quality=8)
    doc.saveAs(desktop + "export_test.jpg", jpeg_options)
    print("✅ JPEG 导出成功")

    # 导出为 PNG
    png_options = ps.PNGSaveOptions()
    doc.saveAs(desktop + "export_test.png", png_options)
    print("✅ PNG 导出成功")

    # 导出为 PDF
    pdf_options = ps.PDFSaveOptions()
    doc.saveAs(desktop + "export_test.pdf", pdf_options)
    print("✅ PDF 导出成功")

    doc.close()

if __name__ == "__main__":
    test_export_operations()
```

### 8️⃣ Session 上下文验证
```python
# test_session_context.py
from photoshop import Session

def test_session_context():
    # 测试新文档会话
    with Session(action="new_document") as ps:
        doc = ps.active_document
        print("✅ Session 新文档创建成功")

        # 添加文本
        text_color = ps.SolidColor()
        text_color.rgb.red = 255
        layer = doc.artLayers.add()
        layer.kind = ps.LayerKind.TextLayer
        layer.textItem.contents = "Session Test"
        layer.textItem.color = text_color
        print("✅ Session 内操作成功")

        # 自动保存和关闭
        doc.saveAs(os.path.expanduser("~/Desktop/session_test.psd"))

    print("✅ Session 自动清理成功")

if __name__ == "__main__":
    test_session_context()
```

## 🔧 常见问题解决方案

### 问题 1: COM 连接失败
```python
# 解决方案代码
import os
import pythoncom

# 确保 COM 初始化
pythoncom.CoInitialize()

# 使用正确的程序 ID
try:
    app = ps.Application(version="2023")  # 指定版本
except:
    # 尝试其他版本
    for version in ["2024", "2022", "2021", "2020"]:
        try:
            app = ps.Application(version=version)
            print(f"✅ 连接到 Photoshop {version} 成功")
            break
        except:
            continue
```

### 问题 2: 权限不足
```cmd
# 以管理员身份运行命令提示符
runas /user:Administrator cmd

# 或者在 Python 脚本中请求管理员权限
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
```

### 问题 3: Photoshop 未启动
```python
# 自动启动 Photoshop
import subprocess
import time

def start_photoshop():
    photoshop_path = r"C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe"
    try:
        subprocess.Popen([photoshop_path])
        time.sleep(5)  # 等待启动
        print("✅ Photoshop 启动成功")
    except Exception as e:
        print(f"❌ Photoshop 启动失败: {e}")
```

## 📊 验证结果记录表

| 功能模块 | 测试状态 | 备注 |
|---------|---------|------|
| 基础连接 | ⬜ | ✅ 成功 / ❌ 失败 / ⚠️ 部分成功 |
| 文档操作 | ⬜ | |
| 图层操作 | ⬜ | |
| 颜色系统 | ⬜ | |
| 选择工具 | ⬜ | |
| 滤镜效果 | ⬜ | |
| 文件导出 | ⬜ | |
| Session管理 | ⬜ | |

## 🚨 性能监控

### 内存使用监控
```python
import psutil
import time

def monitor_performance():
    process = psutil.Process()

    # 记录开始内存
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"开始内存使用: {start_memory:.2f} MB")

    # 执行 Photoshop 操作
    # ... 你的代码 ...

    # 记录结束内存
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"结束内存使用: {end_memory:.2f} MB")
    print(f"内存增长: {end_memory - start_memory:.2f} MB")
```

## 🎯 进阶验证

### 批处理测试
```python
def test_batch_processing():
    app = ps.Application()

    # 创建多个文档进行批量测试
    for i in range(5):
        doc = app.documents.add(400, 400, 72, f"批量测试_{i}")
        layer = doc.artLayers.add()
        layer.textItem.contents = f"Document {i}"
        doc.saveAs(os.path.expanduser(f"~/Desktop/batch_test_{i}.psd"))
        doc.close()

    print("✅ 批处理测试完成")
```

### 错误处理测试
```python
def test_error_handling():
    try:
        app = ps.Application()
        # 尝试打开不存在的文件
        doc = app.open("不存在的文件.psd")
    except Exception as e:
        print(f"✅ 错误捕获成功: {e}")

    try:
        # 尝试在无文档时操作图层
        doc = app.activeDocument
    except Exception as e:
        print(f"✅ 无文档错误捕获成功: {e}")
```

## 📋 验证步骤总结

1. **运行基础连接测试** - 确保环境配置正确
2. **逐一运行功能测试** - 验证各个模块
3. **记录测试结果** - 使用表格记录
4. **性能监控** - 确保没有内存泄漏
5. **错误处理测试** - 验证异常情况处理
6. **批处理测试** - 验证大数据量处理能力

按照这个指南，你就可以系统地验证所有功能了！每个测试文件都可以独立运行，建议从基础连接测试开始。