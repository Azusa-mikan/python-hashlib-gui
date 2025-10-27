# File Hash Verification Tool

A Python-based multi-algorithm file hash calculation tool with GUI and intelligent chunking optimization.
Supports multiple hash algorithms including MD5, SHA1, SHA256, SHA512. When calculating large files, the efficiency far exceeds system-built tools.

[中文文档](./README_zh.md)

## Features

- **Multi-algorithm Support**: Supports MD5, SHA1, SHA256, SHA512 and other hash algorithms
- **GUI Support**: Uses Tkinter to provide file selection dialog and hash value input dialog
- **Command Line Fallback**: Automatically falls back to command line input in non-GUI environments
- **Intelligent Chunking Optimization**: Automatically adjusts read chunk size based on disk type (SSD/HDD)
- **Real-time Progress Display**: Uses `alive-progress` library to show calculation progress bar
- **Hash Value Verification**: Supports input of custom hash values for file verification and comparison
- **Cross-platform Compatibility**: Supports Windows systems, non-Windows systems use default chunk size

## Performance Comparison

![Performance Comparison Demo](src/performance.gif)

The larger the file, the more pronounced the difference becomes.

## Installation Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:
- `tkinter` - GUI support
- `alive-progress` - Progress bar display
- `hashlib` - Hash algorithm calculation

## Usage

1. Run the program:
   ```bash
   python main.py
   # On Windows, you can double-click to open directly
   ```

2. Select hash algorithm
   - Choose MD5, SHA1, SHA256 or SHA512 algorithm in GUI
   - Select algorithm by number in non-GUI environments

3. Select the file to calculate hash value
   - Select file through file selection dialog in GUI
   - Input file path through command line in non-GUI environments

4. Input hash value to compare (optional)
   - Input corresponding hash value in dialog for verification
   - Leave blank to only display calculated hash value

5. View results
   - Program will display calculation progress bar
   - Output file's hash value
   - If verification value was input, comparison result will be shown

## Intelligent Chunking Optimization

The program automatically optimizes read chunk size based on the disk type where the file is located:

- **SSD**: 512KB chunk size
- **HDD**: 256KB chunk size  
- **Default**: 1MB chunk size (when disk type cannot be detected)

This optimization can improve calculation efficiency for large files, especially on different storage media.

## Program Structure

- `get_ssd_or_hdd()`: Detects system disk type (Windows only)
- `select_algorithm()`: Selects hash algorithm
- `select_file()`: File selection functionality
- `input_hash()`: Hash value input functionality
- `_chunk_size()`: Intelligent chunk size determination
- `calculate_hash_with_progress()`: Hash calculation with progress bar
- `hash_diff()`: Hash value comparison
- `main()`: Main program logic

## Notes

- Program is mainly optimized for Windows systems
- Non-Windows systems will use default chunk size
- Appropriate permissions are required to access files and disk information
- Supports all types of file formats
- When running in virtual machines, accurate hard disk type may not be obtained

## Project Origin

The built-in system tools are painfully slow at calculating hashes—fine for small files, but what about a 100 GB one?

I might be old and gray before it finishes, so I wrote this tool hoping it helps everyone.

Plus, there’s no visual progress bar, leaving you clueless about where things stand.
