# Photoshop语音控制测试启动指南

## 重要提示：Windows CMD中文乱码

**Windows CMD默认使用GBK编码，无法正确显示UTF-8中文。**

## 方式1: 使用批处理文件 (推荐)

双击运行：
```bash
run_test.bat
```

这个批处理文件会自动设置UTF-8编码。

## 方式2: PowerShell中运行 (推荐)

在PowerShell中执行：
```powershell
$env:PYTHONIOENCODING="utf-8"
python test_interactive_utf8.py
```

## 方式3: 在VSCode终端中运行 (最佳)

VSCode终端默认支持UTF-8，直接运行：
```bash
python test_interactive_utf8.py
```

**注意：如果看到乱码，请使用上述任一方式。**

## 测试步骤

1. 启动脚本后，系统会显示支持的功能
2. 输入中文指令，例如：
   - "我要锐化图像"
   - "强度150，半径5"
   - "创建一个红色矩形"
   - "位置(200, 150) 大小300x200"
3. 系统会调用Gemma3n模型分析
4. 如果功能支持，会执行API调用
5. 如果不支持，会自动回复"对不起，该功能暂时无法实现"

## 多轮对话示例

```
用户: 我要锐化图像
助手: 请提供锐化参数
用户: 强度150，半径5
系统: 执行成功！
```

## 支持的功能

1. **smart_sharpen** - 智能锐化图像
2. **new_document** - 新建文档
3. **rotate_layer** - 旋转图层
4. **create_rectangle** - 创建矩形

其他功能将自动回复无法实现。

## 注意事项

- 需要确保Ollama服务运行（gemma3n:latest模型）
- 如果没有安装photoshop模块，会模拟执行
- 输入 'quit' 退出
- 输入 'status' 查看当前状态
