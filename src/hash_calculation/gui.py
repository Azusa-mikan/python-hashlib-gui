from typing import cast
import tkinter as tk
from tkinter import filedialog, simpledialog
import sys
from pathlib import Path

from hash_calculation.core import Algorithm
from hash_calculation.tui import select_algorithm as tui_select_algorithm
from hash_calculation.tui import select_file as tui_select_file
from hash_calculation.tui import input_hash as tui_input_hash

def select_algorithm() -> Algorithm:
    """选择哈希算法(GUI模式)"""
    try:
        root = tk.Tk()
        root.title("Select Hash Algorithm")
        root.resizable(False, False)
        root.attributes("-topmost", True)
        algorithm = tk.StringVar()

        def on_click(choice):
            algorithm.set(choice)
            root.destroy()

        # 窗口关闭事件
        def on_close():
            sys.exit(0)

        root.protocol("WM_DELETE_WINDOW", on_close)

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
    except tk.TclError:
        return tui_select_algorithm()
    return cast(Algorithm, algorithm.get())

def select_file(algorithm: Algorithm) -> Path:
    """选择文件(GUI模式)"""
    try:
        file_path = filedialog.askopenfilename(
            title=f"Select the file to calculate {algorithm}", 
            initialdir=Path.cwd(),
            filetypes=[("All files", "*.*")]
        )
        return Path(file_path).resolve()
    except tk.TclError:
        return tui_select_file(algorithm)

def input_hash(algorithm: Algorithm) -> str:
    """输入要比对的哈希值(GUI模式)"""
    try:
        custom_hash = simpledialog.askstring(
            f"Input {algorithm} Value",
            f"Please input the {algorithm} value to compare against, or leave blank to skip: " 
        )
        return custom_hash or ""
    except tk.TclError:
        return tui_input_hash(algorithm)
