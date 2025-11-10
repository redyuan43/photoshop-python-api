# Photoshop 快捷键自动化 - 最终版

## 🎯 快速使用

```bash
cd autogui
python photoshop_hotkey_best.py
```

**功能**: 自动检测Photoshop窗口 → 激活并最大化 → 发送快捷键 `Alt+W, K, R`

## 📁 文件列表

### 核心文件
- **photoshop_hotkey_best.py** (3.3KB) ⭐ 推荐使用
  - 使用pywinauto库，稳定可靠
  - 自动激活并最大化窗口
  - 发送快捷键序列

### 辅助文件
- **send_hotkeys_only.py** (1.7KB)
  - 手动激活后的备用方案
  - 只发送快捷键，不激活窗口

- **demo_hotkey.py** (3.5KB)
  - 演示版本，无需Photoshop
  - 模拟完整流程

### 文档
- **README.md** (5.4KB) - 详细使用说明
- **QUICK_START.md** (2.9KB) - 快速开始指南
- **SUMMARY.md** (5.0KB) - 完整项目总结

## ✅ 测试状态

**测试通过** (2025-11-10):
- ✅ 窗口检测: 成功
- ✅ 窗口激活: 成功
- ✅ 窗口最大化: 成功
- ✅ 快捷键发送: 成功
- ✅ 状态保持: 成功

**测试环境**:
- Windows 10/11
- Adobe Photoshop 2025
- Python 3.11

## 🔧 依赖安装

```bash
pip install pyautogui pywinauto
```

## 🎉 使用效果

```
正在搜索Photoshop窗口...
[OK] 找到窗口: 未命名-333.psd @ 100%(RGB/8)

正在激活窗口...
[OK] 已设置焦点
[OK] 窗口已最大化
[OK] 窗口激活完成

开始发送快捷键...
  1. Alt + W
  2. K
  3. R

[OK] 快捷键发送完成
```

## 💡 核心特性

1. **自动检测**: 支持多种窗口标题格式
2. **可靠激活**: 使用专业pywinauto库
3. **窗口管理**: 自动最大化确保可见
4. **快捷键发送**: 依次发送 Alt+W, K, R
5. **状态反馈**: 清晰的执行日志

## 📞 支持

如遇问题，请查看:
- `README.md` - 详细文档
- `QUICK_START.md` - 快速指南

---
**版本**: v1.0 - 最终版
**状态**: ✅ 生产就绪
**最后更新**: 2025-11-10
