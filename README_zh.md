# 文件哈希校验工具

一个基于 Python 的文件哈希工具，支持 GUI/TUI 交互、磁盘类型分块建议与进度显示。  
支持 MD5、SHA1、SHA256、SHA512，适合大文件快速计算与校验。

## 功能特性

- GUI 模式（Tkinter，不可用时自动降级到 TUI）
- TUI 模式（questionary）
- CLI 参数模式（直接计算）
- 根据磁盘类型提供分块大小建议（仅 Windows）
- alive-progress 实时进度条
- 可选哈希值比对

## 性能比较

![性能比较](res/performance.gif)

文件越大，差距越明显
## 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包：
- `tkinter` - 图形界面（可用时为标准库）
- `questionary` - 终端交互
- `alive-progress` - 进度条

## 快速开始

GUI 模式（默认）：
```bash
python -m hash_calculation
```

TUI 模式：
```bash
python -m hash_calculation -t
```

CLI 模式：
```bash
python -m hash_calculation -f "C:\path\to\file.iso" -m SHA256
python -m hash_calculation -f "C:\path\to\file.iso" -m SHA256 -c "your_sha256_hash"
```

## 命令行参数

- `-t, --tui` 使用 TUI 模式
- `-f, --file` CLI 模式下的文件路径
- `-m, --mode` 哈希算法：MD5、SHA1、SHA256、SHA512
- `-c, --compare` 可选哈希值，用于校验

## 智能分块优化

Windows 下提供磁盘类型检测用于分块大小建议：
- SSD: 512KB
- HDD: 256KB
- 兜底: 1MB（无法识别时）

非 Windows 系统默认使用 1MB，除非手动传入分块大小。

## 作为模块使用

```python
from hash_calculation import calculate_hash_with_progress, get_chunk_size, hash_diff
from pathlib import Path

file_path = Path("path/to/your/file")
algorithm = "SHA256"
chunk_size = get_chunk_size(file_path)
hash_value = calculate_hash_with_progress(file_path, algorithm, chunk_size=chunk_size)
# 或不带进度条的计算
# from hash_calculation import calculate_hash
# hash_value = calculate_hash(file_path, algorithm, chunk_size=chunk_size)
print(f"{file_path}'s {algorithm} value is: {hash_value}")

compare_hash = "your_sha256_hash"
if hash_diff(hash_value, compare_hash):
    print("校验成功 ✅")
else:
    print("校验失败 ❌")
```

```python
from hash_calculation import get_ssd_or_hdd

disk_types = get_ssd_or_hdd()
for disk, media_type in disk_types.items():
    print(f"Disk {disk}: {media_type}")
```

## 注意事项

- 磁盘类型检测仅支持 Windows
- 在虚拟机环境可能无法准确识别硬盘类型
- 仅支持文件输入，不支持目录
