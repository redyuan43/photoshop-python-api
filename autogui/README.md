# Photoshop 快捷键测试工具

## ⭐ 推荐使用

**最新推荐**: `photoshop_hotkey_best.py` - 最佳版本，稳定可靠

```bash
cd autogui

# 复位基本功能 (Alt+W, K, R)
python photoshop_hotkey_best.py

# 上下移动图层 (Ctrl+{, Ctrl+})
python photoshop_hotkey_best.py --layer-move

# 只向下移动图层
python photoshop_hotkey_best.py --layer-down

# 只向上移动图层
python photoshop_hotkey_best.py --layer-up

# 新建文档
python photoshop_hotkey_best.py --file-new

# 保存当前文档
python photoshop_hotkey_best.py --file-save
```

**已测试通过**:
- ✅ 成功检测Photoshop窗口
- ✅ 成功激活并最大化窗口
- ✅ 成功发送快捷键序列 (Alt+W, K, R)
- ✅ 成功发送图层移动快捷键 (Ctrl+{, Ctrl+})

**技术栈**:
- `pywinauto` - 专业的Windows UI自动化库，更可靠
- `pyautogui` - 发送快捷键

## 文件说明

### 0. photoshop_hotkey_best.py ⭐ **强烈推荐**
**最佳版本** - 使用pywinauto，稳定可靠，支持多功能

**功能:**
- 自动检测并激活Photoshop窗口
- 最大化窗口确保可见
- 支持多种快捷键操作:
  - 复位基本功能: `Alt + W` → `K` → `R`
  - 上下移动图层: `Ctrl + {` (向下), `Ctrl + }` (向上)
- 命令行参数支持，灵活选择功能

**特点:**
- 使用专业的pywinauto库，窗口激活更可靠
- 精简代码，执行速度更快
- 已验证在真实Photoshop环境中可用

**使用方式:**
```bash
# 复位基本功能
python photoshop_hotkey_best.py

# 上下移动图层 (依次执行向下和向上)
python photoshop_hotkey_best.py --layer-move

# 只向下移动图层
python photoshop_hotkey_best.py --layer-down

# 只向上移动图层
python photoshop_hotkey_best.py --layer-up

# 文档操作
python photoshop_hotkey_best.py --file-new
python photoshop_hotkey_best.py --file-open
python photoshop_hotkey_best.py --file-save
python photoshop_hotkey_best.py --file-save-as
python photoshop_hotkey_best.py --export-as
python photoshop_hotkey_best.py --file-close
python photoshop_hotkey_best.py --file-close-all
python photoshop_hotkey_best.py --undo

# 查看帮助
python photoshop_hotkey_best.py --help
```

**快捷键说明:**
- `Alt + W + K + R`: 复位基本功能
- `Ctrl + {`: 向下移动选择的图层
- `Ctrl + }`: 向上移动选择的图层

**测试结果:**
- ✅ 成功检测到Photoshop窗口: `未命名-333.psd @ 100%(RGB/8)`
- ✅ 成功激活并最大化窗口
- ✅ 成功发送复位快捷键序列
- ✅ 成功发送图层移动快捷键
- ✅ 窗口保持为活动状态
## 功能说明

### 1. 复位基本功能
默认模式，执行快捷键序列: `Alt + W` → `K` → `R`

```bash
python photoshop_hotkey_best.py
```

### 2. 上下移动图层
使用快捷键 `Ctrl + {` (向下) 和 `Ctrl + }` (向上) 移动选择的图层

```bash
# 依次执行向下和向上移动
python photoshop_hotkey_best.py --layer-move

# 只向下移动
python photoshop_hotkey_best.py --layer-down

# 只向上移动
python photoshop_hotkey_best.py --layer-up
```


### 3. 文件操作
使用 Photoshop 常用文件菜单快捷键，快速完成新建、打开、保存、另存为以及关闭 / 撤销操作。

```bash
# 新建 / 打开文档
python photoshop_hotkey_best.py --file-new
python photoshop_hotkey_best.py --file-open

# 保存相关
python photoshop_hotkey_best.py --file-save
python photoshop_hotkey_best.py --file-save-as
python photoshop_hotkey_best.py --export-as

# 关闭与撤销
python photoshop_hotkey_best.py --file-close
python photoshop_hotkey_best.py --file-close-all
python photoshop_hotkey_best.py --undo
```

## 执行流程

```
1. 扫描Photoshop窗口
   └─ 查找包含"Photoshop"的窗口
   └─ 筛选可见窗口
   └─ 选择最前面的窗口

2. 窗口焦点检查
   └─ 获取当前活动窗口
   └─ 如果不是Photoshop，则激活它

3. 发送快捷键序列
   └─ Alt + W (打开窗口菜单)
   └─ K (选择工具)
   └─ R (应用设置)

4. 完成
   └─ 提示用户操作完成
```

## 快捷键说明

### 1. 复位基本功能
**Alt + W + K + R**

- **Alt + W**: 打开Photoshop的窗口菜单
- **K**: 在菜单中选择特定工具或选项
- **R**: 应用选择并执行操作

### 2. 上下移动图层
**Ctrl + {** 和 **Ctrl + }**

- **Ctrl + {** (左方括号): 向下移动选择的图层
- **Ctrl + }** (右方括号): 向上移动选择的图层

注: 具体功能取决于Photoshop的当前状态和界面设置。


### 3. 文件菜单快捷键
- **Ctrl + N**: 新建 Photoshop 文档
- **Ctrl + O**: 打开文件
- **Ctrl + S**: 保存当前文档
- **Ctrl + Shift + S**: 另存为新文件
- **Ctrl + Alt + Shift + W**: 导出为...
- **Ctrl + W**: 关闭当前文档
- **Ctrl + Alt + W**: 关闭所有文档
- **Ctrl + Z**: 撤销上一次操作

## 注意事项

1. **依赖要求**
   - Windows系统（pygetwindow只支持Windows）
   - 安装Photoshop
   - 安装Python依赖包

2. **安全模式**
   - pyautogui默认安全模式：鼠标移动到屏幕左上角会中断
   - 可通过取消注释 `pyautogui.FAILSAFE = False` 禁用

3. **窗口要求**
   - Photoshop必须已启动
   - 窗口必须可见（非最小化）
   - 窗口标题包含"Photoshop"

4. **权限要求**
   - 需要能够控制窗口
   - 需要能够发送按键
   - 可能需要管理员权限（某些系统）

## 错误排查

### 错误: 未找到任何Photoshop窗口
**解决方案:**
- 启动Adobe Photoshop
- 确保Photoshop窗口可见（非最小化）
- 检查窗口标题是否包含"Photoshop"

### 错误: 无法激活窗口
**解决方案:**
- 以管理员身份运行脚本
- 检查是否有其他程序阻止窗口激活
- 确保Photoshop窗口未被完全遮挡

### 错误: 编码错误
**解决方案:**
- 这是Windows终端的GBK编码问题
- 脚本已自动将emoji替换为ASCII符号
- 如仍有问题，请使用英文版Python或设置环境变量 `PYTHONIOENCODING=utf-8`

## 扩展使用

### 修改快捷键
编辑 `send_hotkey_sequence()` 函数中的按键代码:

```python
# 示例: Ctrl+N (新建)
pyautogui.hotkey('ctrl', 'n')

# 示例: V (切换到移动工具)
pyautogui.press('v')

# 示例: Shift+Ctrl+N (新建图层)
pyautogui.hotkey('shift', 'ctrl', 'n')
```

### 添加延迟
在按键之间添加延迟:

```python
pyautogui.hotkey('alt', 'w')
time.sleep(0.5)  # 等待0.5秒
pyautogui.press('k')
```

## 示例输出

### 成功执行
```
============================================================
Photoshop 快捷键测试工具
============================================================
正在搜索Photoshop窗口...
[OK] 找到Photoshop窗口: Adobe Photoshop 2024 - [Document_1.psd]
   - 位置: (100, 100)
   - 大小: 1920 x 1080
   - 状态: 可见

------------------------------------------------------------
正在检查当前活动窗口...
[WARN] 当前活动窗口不是Photoshop: chrome.exe
[INFO] 需要激活Photoshop窗口

------------------------------------------------------------
正在激活窗口...
[OK] 窗口已激活

------------------------------------------------------------
开始执行快捷键序列...
  1. Alt + W
  2. K
  3. R

步骤 1: 发送 Alt+W
[OK] 按键已发送

步骤 2: 发送 K
[OK] 按键已发送

步骤 3: 发送 R
[OK] 按键已发送

[OK] 快捷键序列执行完成
============================================================
测试完成!
============================================================
```
