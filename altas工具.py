import os
import sys
import tkinter as tk
from tkinter import filedialog
import subprocess
import 拆分
import 合并
import 放大
import png处理
import configparser
import shutil
from tkinter import messagebox
import ctypes
from PIL import Image


# 定义拆分函数，用于将一个 Atlas 文件拆分成多个小图
def split():
    atlas_file = filedialog.askopenfilename(title="选择atlas文件", filetypes=[("Atlas文件", "*.atlas")])
    if atlas_file:
        拆分.backup_altas_file(atlas_file)
        拆分.create_altas_files(atlas_file)
        log_message(f"拆分完成: {atlas_file}")

# 定义放大函数，用于将一个 Atlas 文件放大一定的倍数
def enlarge():
    scale_factor = entry.get()
    if not scale_factor:
        messagebox.showinfo("提示", "请输入放大倍数")
        return
    atlas_file = filedialog.askopenfilename(title="选择atlas文件", filetypes=[("Atlas文件", "*.atlas")])
    if atlas_file:
        放大.scale_atlas_file(atlas_file, scale_factor)
        log_message(f"放大完成: {atlas_file} by {scale_factor}倍")

# 定义合并函数，用于将多个小图合并成一个 Atlas 文件
def merge():
    input_folder = filedialog.askdirectory(title="选择包含拆分文件的文件夹")
    if input_folder:
        result = 合并.merge_altas_files(input_folder)
        if result:
            new_file_name, new_file_path = result
            display_result(new_file_name, new_file_path)
            log_message(f"合并完成: {new_file_name}")

# 定义替换函数，用于替换 Atlas 文件中的某些小图
def replace():
    selected_indices = file_listbox.curselection()
    if not selected_indices:
        return

    selected_files = [file_listbox.get(idx) for idx in selected_indices]

    for selected_file in selected_files:
        new_file_name = selected_file
        ini_file_path = config[section_name][new_file_name]

        source_path = os.path.join(os.path.dirname(ini_file_path), selected_file)
        destination_path = os.path.join(os.path.dirname(os.path.dirname(ini_file_path)), new_file_name.replace("new.", ""))

        shutil.copy(source_path, destination_path)
        os.remove(source_path)
        config[section_name][new_file_name] = destination_path
        file_listbox.delete(selected_indices)
        log_message(f"替换完成: {new_file_name}")

# 定义显示结果函数，用于显示合并结果
def display_result(new_file_name, new_file_path):
    file_listbox.insert(tk.END, new_file_name)
    config[section_name][new_file_name] = new_file_path
    with open("merged_files.ini", "w") as configfile:
        config.write(configfile)

def pngtool(include_subfolders):
    input_folder = filedialog.askdirectory(title="选择包混淆png图片的文件夹")
    if input_folder:
        png处理.process_folder(input_folder, include_subfolders=include_subfolders)
        log_message(f"PNG处理完成: {input_folder} (包括子文件夹: {'是' if include_subfolders else '否'})")

def log_message(message):
    log_text.insert(tk.END, message + '\n')
    log_text.see(tk.END)

##png同步处理
def select_folder(include_subfolders):
    folder = filedialog.askdirectory()
    if folder:
        
        log_message("Selected folder: " + folder)
        process_folderpng(folder, include_subfolders=include_subfolders)
        
def process_folderpng(folder,include_subfolders):
    for root_dir, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.atlas'):
                process_atlas_file(os.path.join(root_dir, file))
        if not include_subfolders:
            break
            
def process_atlas_file(atlas_file_path):
        log_message(f"Processing atlas file: {atlas_file_path}")
        try:
            with open(atlas_file_path, 'r', encoding='utf-8') as atlas_file:
                lines = atlas_file.readlines()
        except UnicodeDecodeError:
            log_message(f"Failed to read {atlas_file_path} with utf-8 encoding.")
            return

        for i in range(len(lines)):
            if lines[i].strip().endswith('.png'):
                png_file_name = lines[i].strip()
                next_line = lines[i + 1].strip()
                
                if next_line.startswith('size:'):
                    dimensions = next_line.split(':')[1].strip()
                    width, height = map(int, dimensions.split(','))
                    resize_png(atlas_file_path, png_file_name, width, height)


def resize_png( atlas_file_path, png_file_name, width, height):
        atlas_dir = os.path.dirname(atlas_file_path)
        png_file_path = os.path.join(atlas_dir, png_file_name)
        if os.path.exists(png_file_path):
            log_message(f"Resizing {png_file_name} to {width}x{height}")
            with Image.open(png_file_path) as img:
                resized_img = img.resize((width, height))
                resized_img.save(png_file_path)
            log_message(f"Resized {png_file_name} successfully")
        else:
            log_message(f"PNG file not found: {png_file_name}")

def MergedFilestest():
    # 检查是否为打包的exe
    if getattr(sys, 'frozen', False):
        folder_path = os.path.dirname(sys.executable)
    else:
        folder_path = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(folder_path, 'merged_files.ini')

    # 检查文件是否存在
    if not os.path.exists(file_path):
        # 创建并写入内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('[MergedFiles]')
       

    
        

# 设置DPI感知
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# 创建主窗口
window = tk.Tk()
window.title("Atlas文件处理工具")
window.geometry("1200x600")
window_width = 1200
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 创建标签控件
label = tk.Label(window, text="请选择要执行的操作：")
label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='w')

# 创建文本输入框
entry = tk.Entry(window, fg='grey')
entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
entry.insert(0, "放大倍数")

def on_focus_in(event):
    if entry.get() == "放大倍数":
        entry.delete(0, tk.END)
        entry.config(fg='black')

def on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, "放大倍数")
        entry.config(fg='grey')

entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)

# 创建按钮控件
button1 = tk.Button(window, text="拆分", command=split)
button1.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

button2 = tk.Button(window, text="放大", command=enlarge)
button2.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

button3 = tk.Button(window, text="合并", command=merge)
button3.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

button4 = tk.Button(window, text="替换", command=replace)
button4.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

button5 = tk.Button(window, text="png去混淆", command=lambda: pngtool(include_subfolders=include_subfolders_var.get()))
button5.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# 调整png尺寸同步按钮的大小
button6 = tk.Button(window, text="png尺寸同步", command=lambda: select_folder(include_subfolders=include_subfolders_var.get()), width=15)
button6.grid(row=5, column=0, padx=10, pady=10, sticky='ew')

# 创建复选框用于选择是否包括子文件夹
include_subfolders_var = tk.BooleanVar(value=True)
include_subfolders_check = tk.Checkbutton(window, text="包括子文件夹", variable=include_subfolders_var)
include_subfolders_check.grid(row=5, column=1, padx=10, pady=10, sticky='w')

# 创建已处理文件显示控件
log_label = tk.Label(window, text="合并的历史文件：")
log_label.grid(row=0, column=4, padx=10, pady=10, sticky='w')
# 创建列表框控件
file_listbox = tk.Listbox(window)
file_listbox.grid(row=1, column=4, rowspan=5, padx=10, pady=10, sticky='nsew')

# 创建滚动条
scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.grid(row=1, column=5, rowspan=5, sticky='ns')
file_listbox.config(yscrollcommand=scrollbar.set)

# 创建日志显示控件
log_label = tk.Label(window, text="日志：")
log_label.grid(row=0, column=6, padx=10, pady=10, sticky='w')

log_text = tk.Text(window, wrap=tk.WORD, state=tk.NORMAL, height=30, width=50)
log_text.grid(row=1, column=6, rowspan=5, padx=10, pady=10, sticky='nsew')

log_scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=log_text.yview)
log_scrollbar.grid(row=1, column=7, rowspan=5, sticky='ns')
log_text.config(yscrollcommand=log_scrollbar.set)

MergedFilestest()
# 创建 configparser 对象
config = configparser.ConfigParser()
config.read("merged_files.ini")

section_name = "MergedFiles"
if config.has_section(section_name):
    merged_files = config[section_name]
    for file_name, file_path in merged_files.items():
        file_listbox.insert(tk.END, file_name)

# 设置控件的权重
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=0)
window.grid_rowconfigure(2, weight=0)
window.grid_rowconfigure(3, weight=0)
window.grid_rowconfigure(4, weight=0)
window.grid_rowconfigure(5, weight=0)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(4, weight=1)
window.grid_columnconfigure(5, weight=0)
window.grid_columnconfigure(6, weight=0)
window.grid_columnconfigure(7, weight=0)

# 运行主循环
window.mainloop()
