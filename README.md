# File Hash Verification Tool

A Python-based file hashing tool with GUI and TUI modes, disk-aware chunk sizing utilities, and progress display.  
Supports MD5, SHA1, SHA256, SHA512 for large files with noticeable speed improvements.

[中文文档](./README_zh.md)

## Features

- GUI mode with Tkinter dialogs (falls back to TUI if Tk is unavailable)
- TUI mode with questionary prompts
- CLI arguments for direct calculation
- Disk-type detection helper for recommended chunk size (Windows only)
- Real-time progress bar with alive-progress
- Optional hash verification

## Performance Comparison

![Performance Comparison](res/performance.gif)

The larger the file, the more pronounced the difference becomes.
## Installation

```bash
pip install -r requirements.txt
```

Main dependencies:
- `tkinter` - GUI dialogs (standard library when available)
- `questionary` - TUI prompts
- `alive-progress` - Progress bar

## Quick Start

GUI mode (default):
```bash
python -m hash_calculation
```

TUI mode:
```bash
python -m hash_calculation -t
```

CLI mode:
```bash
python -m hash_calculation -f "C:\path\to\file.iso" -m SHA256
python -m hash_calculation -f "C:\path\to\file.iso" -m SHA256 -c "your_sha256_hash"
```

## Command Line Arguments

- `-t, --tui` Use TUI mode (interactive prompts)
- `-f, --file` File path for CLI mode
- `-m, --mode` Hash algorithm: MD5, SHA1, SHA256, SHA512
- `-c, --compare` Optional hash value to verify

## Intelligent Chunking

On Windows, helper functions detect disk type to recommend chunk sizes:
- SSD: 512KB
- HDD: 256KB
- Fallback: 1MB when disk type is unknown

Non-Windows systems always use the default chunk size unless you pass a custom one.

## Use as a Module

```python
from hash_calculation import calculate_hash_with_progress, get_chunk_size, hash_diff
from pathlib import Path

file_path = Path("path/to/your/file")
algorithm = "SHA256"
chunk_size = get_chunk_size(file_path)
hash_value = calculate_hash_with_progress(file_path, algorithm, chunk_size=chunk_size)
# Optional: Calculate hash without progress bar
# from hash_calculation import calculate_hash
# hash_value = calculate_hash(file_path, algorithm, chunk_size=chunk_size)
print(f"{file_path}'s {algorithm} value is: {hash_value}")

compare_hash = "your_sha256_hash"
if hash_diff(hash_value, compare_hash):
    print("verification successful ✅")
else:
    print("verification failed ❌")
```

```python
from hash_calculation import get_ssd_or_hdd

disk_types = get_ssd_or_hdd()
for disk, media_type in disk_types.items():
    print(f"Disk {disk}: {media_type}")
```

## Notes

- Disk type detection only works on Windows
- Some environments may not return accurate disk media type
- Large directories are not supported as input; select files only
