# 导入需要的模块
import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import 拆分
import 合并
import 放大
import png处理
import configparser
import shutil # 用于复制和重命名文件
from tkinter import messagebox

# 定义拆分函数，用于将一个 Atlas 文件拆分成多个小图
def split():
    # 弹出一个文件选择对话框，让用户选择一个后缀为 .atlas 的文件
    atlas_file = filedialog.askopenfilename(title="选择atlas文件", filetypes=[("Atlas文件", "*.atlas")])
    # 如果用户选择了一个有效的文件，执行拆分操作
    if atlas_file:
    # 在拆分之前调用备份函数，传入选中的文件路径作为参数
        拆分.backup_altas_file(atlas_file)
        拆分.create_altas_files(atlas_file)
        


# 定义放大函数，用于将一个 Atlas 文件放大一定的倍数
def enlarge():
    # 获取用户输入的放大倍数
    scale_factor = entry.get()
    if not scale_factor:
        messagebox.showinfo("提示", "请输入放大倍数")
       # print("1111")
        return
    # 弹出一个文件选择对话框，让用户选择一个后缀为 .atlas 的文件
    atlas_file = filedialog.askopenfilename(title="选择atlas文件", filetypes=[("Atlas文件", "*.atlas")])
    # 如果用户选择了一个有效的文件，执行放大操作
    if atlas_file:
        # 执行一个外部命令，调用放大.py 脚本，传入要放大的 Atlas 文件路径和倍数
        放大.scale_atlas_file( atlas_file, scale_factor)

# 定义合并函数，用于将多个小图合并成一个 Atlas 文件
def merge():
    # 弹出一个目录选择对话框，让用户选择一个包含拆分文件的目录
    input_folder = filedialog.askdirectory(title="选择包含拆分文件的文件夹")
    # 如果用户选择了一个有效的目录，执行合并操作
    if input_folder:
        # 调用合并模块的函数，传入要合并的目录路径，获取合并结果
        result = 合并.merge_altas_files(input_folder)
        # 如果合并结果不为空，说明合并成功，显示合并结果
        if result:
            new_file_name, new_file_path = result
            display_result(new_file_name, new_file_path)

# 定义替换函数，用于替换 Atlas 文件中的某些小图
def replace():
    selected_indices = file_listbox.curselection()
    if not selected_indices:
        return

    selected_files = [file_listbox.get(idx) for idx in selected_indices]

    for selected_file in selected_files:
        # 不要替换文件名中的 "new."，保持和配置文件中的键一致
        new_file_name = selected_file
        ini_file_path = config[section_name][new_file_name]

        source_path = os.path.join(os.path.dirname(ini_file_path), selected_file)
        # 替换目标路径中的 "new."，得到原始 Atlas 文件名
        destination_path = os.path.join(os.path.dirname(os.path.dirname(ini_file_path)), new_file_name.replace("new.", ""))

        # Copy and rename the file
        shutil.copy(source_path, destination_path)

        # Delete the original file
        os.remove(source_path)

        # Update the config file
        config[section_name][new_file_name] = destination_path

        # Delete the item from the listbox
        file_listbox.delete(selected_indices)


# 定义显示结果函数，用于显示合并结果
def display_result(new_file_name, new_file_path):
    # 在列表框末尾插入新生成的 Atlas 文件名
    file_listbox.insert(tk.END, new_file_name)
    # 保存文件信息到配置文件中
    config[section_name][new_file_name] = new_file_path

    # 打开一个名为 "merged_files.ini" 的文件，以写入模式打开
    with open("merged_files.ini", "w") as configfile:
        # 将配置信息写入到文件中
        config.write(configfile)



def pngtool():
    # 弹出一个目录选择对话框，让用户选择一个包含拆分文件的目录
    input_folder = filedialog.askdirectory(title="选择包混淆png图片的件夹")
    print(input_folder)
    # 如果用户选择了一个有效的目录，执行合并操作
    if input_folder:
        # 调用合并模块的函数，传入要合并的目录路径，获取合并结果
        png处理.process_folder(input_folder,include_subfolders=True)
        # 如果合并结果不为空，说明合并成功，显示合并结果


# 进入主窗口的主循环，等待用户的操作

# 创建一个主窗口对象，并赋值给 window 变量
window = tk.Tk()
# 设置主窗口的标题为 "Atlas文件处理工具"
window.title("Atlas文件处理工具")
# 设置主窗口的大小为 600x200 像素
window.geometry("620x200")
window_width = 600
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 创建一个标签控件，显示文本 "请选择要执行的操作："，并放置在主窗口的第一行第一列，占两列，设置边距为 10 像素
label = tk.Label(window, text="请选择要执行的操作：")
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# 创建一个文本输入框控件，并赋值给 entry 变量，用于输入放大倍数，并放置在主窗口的第二行第一列，占两列，设置边距为 10 像素
entry = tk.Entry(window, fg='grey')  # 设置文本颜色为灰色
entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
# 在文本输入框中插入占位文本
entry.insert(0, "")



# 创建一个按钮控件，显示文本 "拆分"，并绑定拆分函数到点击事件上，放置在主窗口的第三行第一列，设置边距为 10 像素
button1 = tk.Button(window, text="拆分", command=split)
button1.grid(row=2, column=0, padx=10, pady=10)

# 创建一个按钮控件，显示文本 "放大"，并绑定放大函数到点击事件上，放置在主窗口的第三行第二列，设置边距为 10 像素
button2 = tk.Button(window, text="放大", command=enlarge)
button2.grid(row=2, column=1, padx=10, pady=10)

# 创建一个按钮控件，显示文本 "合并"，并绑定合并函数到点击事件上，放置在主窗口的第四行第一列，设置边距为 10 像素
button3 = tk.Button(window, text="合并", command=merge)
button3.grid(row=3, column=0, padx=10, pady=10)

# 创建一个按钮控件，显示文本 "替换"，并绑定替换函数到点击事件上，放置在主窗口的第四行第二列，设置边距为 10 像素
button4 = tk.Button(window, text="替换", command=replace)
button4.grid(row=3, column=1, padx=10, pady=10)

# 创建一个按钮控件，显示文本 "png去混淆"，并绑定替换函数到点击事件上，放置在主窗口的第5行第1列，设置边距为 10 像素
button5 = tk.Button(window, text="png去混淆", command=pngtool)
button5.grid(row=2, column=2, padx=10, pady=10)



# 创建一个列表框控件，并赋值给 file_listbox 变量，用于显示合并后的 Atlas 文件名，并放置在主窗口的第一行第三列，占四行，设置边距为 10 像素
file_listbox = tk.Listbox(window)
file_listbox.grid(row=0, column=4, rowspan=4, padx=10, pady=10)

# 创建一个 configparser 对象，并赋值给 config 变量，用于读写配置文件
config = configparser.ConfigParser()
# 从 "merged_files.ini" 文件中读取配置信息，并保存到 config 对象中
config.read("merged_files.ini")

# 定义一个常量 section_name，表示配置文件中的一个分节名
section_name = "MergedFiles"
# 如果 config 对象中有 section_name 对应的分节
if config.has_section(section_name):
    # 获取该分节下的所有键值对，并赋值给 merged_files 变量
    merged_files = config[section_name]
    # 遍历 merged_files 中的每个键值对
    for file_name, file_path in merged_files.items():
        # 在列表框中# 在列表框中插入文件名
        file_listbox.insert(tk.END, file_name)

window.mainloop()
