import sys
import tkinter as tk
from tkinter import filedialog, simpledialog
from alive_progress import alive_bar
import hashlib
import os
import subprocess
import platform

def get_platform() -> bool:
    if platform.system() != "Windows":
        return False
    else:
        return True

def get_ssd_or_hdd() -> dict:
    if not get_platform():
        return {}
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
        return {}
    output = result.stdout.strip()
    # 解析输出，将其转换为字典
    """
    示例输出:
    F SSD
    E SSD
    C SSD
    D SSD
    """
    result_dict = {}
    for line in output.split('\n'):
        if line.strip():
            key, value = line.split()
            result_dict[key] = value
    """
    转换后:
    {'F': 'SSD', 'E': 'SSD', 'C': 'SSD', 'D': 'SSD'}
    """
    return result_dict

def select_algorithm() -> str:
    """选择哈希算法"""
    try:
        root = tk.Tk()
        root.title("Select Hash Algorithm") #翻译成英文
        root.resizable(False, False)
        root.attributes("-topmost", True)
        algorithm = tk.StringVar()

        def on_click(choice):
            algorithm.set(choice)
            root.destroy()

        tk.Label(root, text="Please select a hash algorithm:").pack(pady=10)
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="MD5", width=10, command=lambda: on_click("MD5")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="SHA1", width=10, command=lambda: on_click("SHA1")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="SHA256", width=10, command=lambda: on_click("SHA256")).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="SHA512", width=10, command=lambda: on_click("SHA512")).grid(row=0, column=3, padx=5)

        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_width()) // 2
        y = (root.winfo_screenheight() - root.winfo_height()) // 2
        root.geometry(f"+{x}+{y}")

        root.mainloop()
        return algorithm.get()
    except tk.TclError:
        # 无桌面环境，回退到命令行输入
        while True:
            print(
                f"Select the algorithm to calculate:\n"
                "1. MD5\n"
                "2. SHA1\n"
                "3. SHA256\n"
                "4. SHA512\n"
            )
            msg = input("Please input the number of the selected algorithm (1-4): ")
            match msg:
                case "1":
                    return "MD5"
                case "2":
                    return "SHA1"
                case "3":
                    return "SHA256"
                case "4":
                    return "SHA512"
                case _:
                    print("Invalid input. Please select a number between 1 and 4.")
                    continue


def select_file(algorithm: str):
    """打开文件选择对话框，无桌面环境时回退到input"""
    try:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        file_path = filedialog.askopenfilename(
            title=f"Select the file to calculate {algorithm}", 
            filetypes=[("All files", "*.*")]
        )
        return file_path
    except tk.TclError:
        # 无桌面环境，回退到命令行输入
        return input(f"Please input the file path to calculate {algorithm}: ") 

def input_hash(algorithm: str):
    """输入要比对的哈希值"""
    try:
        custom_hash = simpledialog.askstring(
            f"Input {algorithm} Value",
            f"Please input the {algorithm} value to compare against, or leave blank to skip: " 
        )
        return custom_hash
    except tk.TclError:
        # 无桌面环境，回退到命令行输入
        return input(f"Please input the {algorithm} value to compare against, or leave blank to skip: ") 

def get_file_name(file_path):
    """获取文件名称"""
    name = os.path.basename(file_path)
    max_length = 20
    if len(name) > max_length:
        name = "..." + name[-max_length:]
    return name

def _chunk_size(file_path):
    """根据文件路径判断分块大小"""
    DEFAULT_CHUNK = 1024 * 1024  # 1MB
    SSD_CHUNK = 512 * 1024       # 512KB
    HDD_CHUNK = 256 * 1024       # 256KB
    ssd_or_hdd = get_ssd_or_hdd()
    if ssd_or_hdd is None:
        if not get_platform():
            print("The current system is not Windows, unable to retrieve SSD or HDD information. Default chunk size set to 1MB.")
            return DEFAULT_CHUNK  # 默认分块大小为1MB
        print("Unable to retrieve SSD or HDD information. Default chunk size set to 1MB.") 
        return DEFAULT_CHUNK  # 默认分块大小为1MB
    # 获取文件所在磁盘
    file_drive = file_path[0].upper()
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


def calculate_hash_with_progress(file_path, algorithm):
    """计算文件的哈希值并显示进度条"""
    # 获取文件大小
    file_size = os.path.getsize(file_path)
    # 根据文件所在磁盘判断分块大小
    chunk_size = _chunk_size(file_path)
    
    match algorithm:
        case "MD5":
            hash = hashlib.md5()
        case "SHA1":
            hash = hashlib.sha1()
        case "SHA256":
            hash = hashlib.sha256()
        case "SHA512":
            hash = hashlib.sha512()
        case _:
            print(f"You must select an algorithm: MD5, SHA1, SHA256, SHA512.")
            sys.exit(0)
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
                hash.update(chunk)
                bar(len(chunk))  # 更新进度条
    
    return hash.hexdigest()

def hash_diff(hash1: str, hash2: str) -> bool:
    """比较两个哈希值是否相同"""
    if str(hash1).lower() == str(hash2).lower():
        return True
    else:
        return False

def main():
    try:
        algorithm = select_algorithm()
        file_path_original = select_file(algorithm)
        if not get_platform():
            file_path = os.path.realpath(file_path_original)
        else:
            file_path = os.path.abspath(file_path_original)
        if file_path == "":
            print("No file selected.") 
            sys.exit(0)
        custom_hash = input_hash(algorithm)
        hash = calculate_hash_with_progress(file_path, algorithm)
        print(f"{algorithm} value for {get_file_name(file_path)}: {hash}") 
        if custom_hash is None or custom_hash.strip() == "":
            pass
        elif hash_diff(custom_hash, hash):
            print(f"{get_file_name(file_path)} {algorithm} value matches the input.") 
        else:
            print(f"{get_file_name(file_path)} {algorithm} value differs from the input.") 
        input("Press any key to continue...") 
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nProgram exited.") 
        sys.exit(0)

if __name__ == "__main__":
    main()