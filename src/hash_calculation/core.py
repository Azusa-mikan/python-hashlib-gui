from typing import Literal, cast
from pathlib import Path
import platform
import subprocess
import hashlib
import argparse

from alive_progress import alive_bar

Algorithm = Literal["MD5", "SHA1", "SHA256", "SHA512"]

_disk_media_cache: dict | None = None

def get_platform() -> bool:
    return platform.system() == "Windows"

def get_ssd_or_hdd() -> dict:
    """获取所有硬盘的类型（SSD或HDD，仅支持Windows）"""
    global _disk_media_cache
    if _disk_media_cache is not None:
        return _disk_media_cache
    if not get_platform():
        _disk_media_cache = {}
        return _disk_media_cache
    command = """
    Get-PhysicalDisk | % { $pd = $_; Get-Partition | ? DriveLetter | ? { (Get-Disk -Number $_.DiskNumber).UniqueId -eq $pd.UniqueId } | % { "$($_.DriveLetter) $($pd.MediaType)" } }
    """
    print("Detecting SSD and HDD...")
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )
    if result.stdout is None or result.stdout.strip() == "":
        _disk_media_cache = {}
        return _disk_media_cache
    output = result.stdout.strip()
    result_dict = {}
    for line in output.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        key, value = parts
        result_dict[key] = value
    _disk_media_cache = result_dict
    # {'F': 'SSD', 'E': 'SSD', 'C': 'SSD', 'D': 'SSD'}
    return result_dict

def get_chunk_size(file_path: Path) -> int:
    """根据文件路径判断分块大小"""
    DEFAULT_CHUNK = 1024 * 1024  # 1MB
    SSD_CHUNK = 512 * 1024       # 512KB
    HDD_CHUNK = 256 * 1024       # 256KB
    ssd_or_hdd = get_ssd_or_hdd()
    if not ssd_or_hdd:
        if not get_platform():
            print("The current system is not Windows, unable to retrieve SSD or HDD information. Default chunk size set to 1MB.")
            return DEFAULT_CHUNK  # 默认分块大小为1MB
        print("Unable to retrieve SSD or HDD information. Default chunk size set to 1MB.") 
        return DEFAULT_CHUNK  # 默认分块大小为1MB
    # 获取文件所在磁盘
    file_drive = file_path.drive.upper().replace(":", "")
    file_name = get_file_name(file_path)
    if file_drive not in ssd_or_hdd:
        print(f"Unknown disk type for file {file_name} Default chunk size set to 1MB.") 
        return DEFAULT_CHUNK # 默认分块大小为1MB
    match ssd_or_hdd[file_drive]:
        case "SSD":
            print(f"SSD detected for file {file_name} Chunk size set to 512KB for improved performance.") 
            return SSD_CHUNK  # 如果是SSD，分块大小为512KB
        case "HDD":
            print(f"HDD detected for file {file_name} Chunk size set to 256KB for improved performance.") 
            return HDD_CHUNK  # 如果是HDD，分块大小为256KB
        case _:
            print(f"Unknown disk type for file {file_name} Default chunk size set to 1MB.") 
            return DEFAULT_CHUNK  # 默认分块大小为1MB

def get_file_name(file_path: Path, max_length: int = 20) -> str:
    """获取文件名称"""
    name = file_path.name
    if len(name) > max_length:
        name = "..." + name[-max_length:]
    return name

def calculate_hash_with_progress(file_path: Path, algorithm: Algorithm) -> str:
    """计算文件的哈希值"""
    # 获取文件大小
    file_size = file_path.stat().st_size
    # 根据文件所在磁盘判断分块大小
    chunk_size = get_chunk_size(file_path)
    
    match algorithm:
        case "MD5":
            hasher = hashlib.md5()
        case "SHA1":
            hasher = hashlib.sha1()
        case "SHA256":
            hasher = hashlib.sha256()
        case "SHA512":
            hasher = hashlib.sha512()
        case _:
            raise ValueError("You must select an algorithm: MD5, SHA1, SHA256, SHA512.")
    with alive_bar(
        file_size, title=f"Calculating {algorithm} for {get_file_name(file_path)}",
        theme='classic',scale=True,
        spinner=None,dual_line=True,
        precision=2,max_cols=20
        ) as bar:
        with open(file_path, 'rb') as f:
            # 分块读取文件
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
                bar(len(chunk))  # 更新进度条
    
    return hasher.hexdigest().upper()

def hash_diff(hash1: str, hash2: str) -> bool:
    """比较两个哈希值是否相同"""
    if str(hash1).strip().casefold() == str(hash2).strip().casefold():
        return True
    else:
        return False

def run_calculate(
        file_path: Path,
        algorithm: Algorithm,
        compare_hash: str | None = None
    ) -> str:
    """运行计算哈希值"""
    digest = calculate_hash_with_progress(file_path, algorithm)
    if compare_hash and compare_hash.strip():
        if hash_diff(digest, compare_hash):
            print(f"{get_file_name(file_path)}'s {algorithm} value verification successful ✅")
        else:
            print(f"{get_file_name(file_path)}'s {algorithm} value verification failed ❌") 
    return digest

def args() -> tuple[bool, Path | None, Algorithm | None, str | None]:
    """处理命令行参数"""
    parser = argparse.ArgumentParser(description="Calculate file hash")
    parser.add_argument("-t", "--tui", help="Use TUI mode", action="store_true")
    parser.add_argument("-f", "--file", help="Path to the file to calculate hash for.")
    parser.add_argument("-m", "--mode", choices=["MD5", "SHA1", "SHA256", "SHA512"], help="Hash algorithm to use.")
    parser.add_argument("-c", "--compare", dest="compare_hash", help="Optional hash value to compare against the calculated one.", nargs='?')
    args = parser.parse_args()

    tui_mode = bool(args.tui)
    if not tui_mode and (args.file is None or args.mode is None):
        parser.error("--file and --mode are required unless --tui is used")
    file_path = Path(args.file).resolve() if args.file else None
    algorithm = cast(Algorithm, args.mode) if args.mode else None
    compare_hash = args.compare_hash
    return tui_mode, file_path, algorithm, compare_hash