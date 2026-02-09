from pathlib import Path

import questionary

from hash_calculation.core import Algorithm

def select_algorithm() -> Algorithm:
    """选择哈希算法(TUI模式)"""
    algorithm = questionary.select(
        message="Select Hash Algorithm: ",
        choices=["MD5", "SHA1", "SHA256", "SHA512"],
    ).ask()
    return algorithm

def select_file(algorithm: Algorithm) -> Path:
    """选择文件(TUI模式)"""
    file_path = questionary.path(
        message=f"Select the file to calculate {algorithm}: ",
        default=str(Path.cwd()),
        validate=lambda path: True if Path(path).is_file() else "Please select a file path",
        file_filter=lambda file: Path(file).is_file()
    ).ask()
    return Path(file_path).resolve()

def input_hash(algorithm: Algorithm) -> str:
    """输入要比对的哈希值(TUI模式)"""
    compare_hash = questionary.text(
        message=(
            f"Input {algorithm} Value"
            f"Please input the {algorithm} value to compare against, or leave blank to skip: "
        ),
        default=""
    ).ask()
    return compare_hash.strip()