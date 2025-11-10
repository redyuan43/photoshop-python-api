# Photoshop 快捷键工具 - 清晰参数说明

## 🎯 **参数已重新设计，完全无歧义！**

### 📋 **基本功能**
```bash
python photoshop_hotkey_best.py
```
- 复位基本功能 (Alt+W, K, R)

### 🎨 **图层操作** (移动图层)

```bash
# 上下都移动一层
python photoshop_hotkey_best.py --layer-move
# 快捷键: Ctrl+{ (向下) → Ctrl+} (向上)

# 只向上移动一层
python photoshop_hotkey_best.py --layer-up
# 快捷键: Ctrl+} (右方括号)

# 只向下移动一层
python photoshop_hotkey_best.py --layer-down
# 快捷键: Ctrl+{ (左方括号)
```

### 🔲 **选区操作** (移动选区)

```bash
# 选区向上移动
python photoshop_hotkey_best.py --selection-up
# 快捷键: Ctrl+↑ (上箭头)

# 选区向下移动
python photoshop_hotkey_best.py --selection-down
# 快捷键: Ctrl+↓ (下箭头)

# 选区向左移动
python photoshop_hotkey_best.py --selection-left
# 快捷键: Ctrl+← (左箭头)

# 选区向右移动
python photoshop_hotkey_best.py --selection-right
# 快捷键: Ctrl+→ (右箭头)
```

### 📝 **选区管理**

```bash
python photoshop_hotkey_best.py --select-all  # 全选 (Ctrl+A)
python photoshop_hotkey_best.py --deselect    # 取消选区 (Ctrl+D)
python photoshop_hotkey_best.py --invert      # 反选 (Ctrl+Shift+I)
python photoshop_hotkey_best.py --duplicate   # 复制图层 (Ctrl+J)
```

## 📊 **完整参数表**

| 参数 | 功能 | 快捷键 | 移动对象 |
|------|------|--------|----------|
| `--layer-move` | 图层上下移动 | Ctrl+{, Ctrl+} | 图层 |
| `--layer-up` | 图层向上移动 | Ctrl+} | 图层 |
| `--layer-down` | 图层向下移动 | Ctrl+{ | 图层 |
| `--selection-up` | 选区上移 | Ctrl+↑ | 选区 |
| `--selection-down` | 选区下移 | Ctrl+↓ | 选区 |
| `--selection-left` | 选区左移 | Ctrl+← | 选区 |
| `--selection-right` | 选区右移 | Ctrl+→ | 选区 |

## ⚠️ **重要区别**

- **图层移动** `--layer-*` → 使用方括号 `[` `]`
- **选区移动** `--selection-*` → 使用方向键 `↑` `↓` `←` `→`

## 🎯 **使用场景**

### 场景1: 图层管理
```bash
# 选中图层后，移动图层顺序
python photoshop_hotkey_best.py --layer-up     # 图层上移一层
python photoshop_hotkey_best.py --layer-down   # 图层下移一层
```

### 场景2: 选区调整
```bash
# 创建选区后，微调选区位置
python photoshop_hotkey_best.py --selection-up      # 选区上移
python photoshop_hotkey_best.py --selection-right   # 选区右移
```

### 场景3: 组合操作
```bash
# 全选图层，然后调整图层顺序
python photoshop_hotkey_best.py --select-all
python photoshop_hotkey_best.py --layer-move
```

---
**版本**: v3.0 - 清晰版
**状态**: ✅ 无歧义
