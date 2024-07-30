import os
import tkinter as tk
from tkinter import filedialog
import chardet


#判断文件编码格式
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def merge_altas_files(input_folder):
    

    # 获取文件夹名称
    folder_name = os.path.basename(input_folder)

    # 获取文件夹中的所有文件，仅选择以 "xxx(数字).xxxx" 格式开头的文件
    altas_files = [f for f in os.listdir(input_folder) if f.endswith(".atlas") and f.startswith(tuple(str(i) for i in range(10)))]

    if not altas_files:
        print(f"在文件夹 {input_folder} 中没有符合条件的文件。")
        return None  # 返回空值表示没有新文件

    altas_files.sort()  # 根据文件名排序
    #print(f"{input_folder}\{altas_files[0]}")
    encoding = detect_encoding(f'{input_folder}\{altas_files[0]}')
    # 创建新的合并后的文件
    output_file_name = f"new.{folder_name}.atlas"
    output_file_path = os.path.join(input_folder, output_file_name)

    with open(output_file_path, 'w',encoding=encoding) as output_file:
        for altas_file in altas_files:
            altas_file_path = os.path.join(input_folder, altas_file)
            with open(altas_file_path, 'r',encoding=encoding) as atlas:
                atlas_content = atlas.read()
                output_file.write(atlas_content)
                output_file.write('\n\n')  # 添加两个空行

    print(f"合并后的文件 {output_file_name} 已创建在文件夹 {input_folder} 中。")
    
    # 返回新文件的名称和路径
    return output_file_name, output_file_path

def main():
    # 使用文件夹选择对话框让用户选择包含拆分文件的文件夹
    root = tk.Tk()
    root.withdraw()  # 隐藏Tk窗口
    input_folder = filedialog.askdirectory(title="选择包含拆分文件的文件夹")
    
    if input_folder:
        result = merge_altas_files(input_folder)
        if result:
            return result

if __name__ == "__main__":
    main()
