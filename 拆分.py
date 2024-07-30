# 导入需要的模块
import os
import tkinter as tk
from tkinter import filedialog
import shutil # 用于复制文件
import chardet


def create_folder(folder_path):
    # 创建文件夹
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        pass
        
#判断文件编码格式        
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']
    
def backup_altas_file(atlas_file):
    # 复制一份atlas文件到同一个目录中，命名为xxx.atlas.bak
    backup_file_name = atlas_file + ".bak"
    shutil.copy(atlas_file, backup_file_name) # 复制文件
    print("Altas文件已创建完成。")

def create_altas_files(atlas_file):
    encoding = detect_encoding(atlas_file)
    # 读取atlas文件内容
    with open(atlas_file, 'r',encoding=encoding) as f:
        lines = f.readlines()

    # 获取文件夹路径
    folder_path = os.path.splitext(atlas_file)[0]  # 使用atlas文件的名称作为文件夹名称
    create_folder(folder_path)  # 创建文件夹

    # 初始化变量
    current_image_name = None
    current_image_data = []
    image_count = 0

    # 遍历atlas文件内容
    for line in lines:
        line = line.strip()
        if line.endswith(".png"):  # 如果是以.png结尾的行
            if current_image_name is not None:
                # 添加xxx.png行并创建xxx.png.altas文件并写入内容
                image_count += 1
                image_number = str(image_count).zfill(3)  # 格式化成3位数字，例如001, 002, ...
                current_image_data.insert(0, current_image_name + '.png\n')
                altas_file_name = os.path.join(folder_path, image_number + "_" + current_image_name + ".atlas")
                with open(altas_file_name, 'w') as altas_file:
                    altas_file.writelines(current_image_data)
            current_image_name = os.path.splitext(line)[0]  # 获取xxx.png
            current_image_data = []  # 重置当前图片的数据
        else:
            current_image_data.append(line + '\n')

    # 处理最后一个图片
    if current_image_name is not None:
        # 添加xxx.png行并创建xxx.png.altas文件并写入内容
        image_count += 1
        image_number = str(image_count).zfill(3)  # 格式化成3位数字，例如001, 002, ...
        current_image_data.insert(0, current_image_name + '.png\n')
        altas_file_name = os.path.join(folder_path, image_number + "_" + current_image_name + ".atlas")
        with open(altas_file_name, 'w',encoding=encoding) as altas_file:
            altas_file.writelines(current_image_data)
    print("Altas文件已完成拆分。")

def main():
    # 使用文件选择对话框让用户选择atlas文件
    root = tk.Tk()
    root.withdraw()  # 隐藏Tk窗口
    atlas_file = filedialog.askopenfilename(title="选择atlas文件", filetypes=[("Atlas文件", "*.atlas")])
    
    if atlas_file:
        backup_altas_file(atlas_file) # 在选中之后调用备份函数，传入选中的文件路径作为参数
        create_altas_files(atlas_file)
        print("Altas文件已创建完成。")

if __name__ == "__main__":
    main()
