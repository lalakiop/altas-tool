#去除PNG头文件之前的字节信息
import os
import binascii

def process_folder(folder_path, include_subfolders):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            processed = process_file(file_path)

            if processed:
                print(f"文件 {file_path} 处理完成，生成副本: {processed}")

            if not include_subfolders:
                break

def process_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()

        target_sequence = binascii.unhexlify(b'89504e470d')

        index = content.find(target_sequence)

        if index == -1:
            print(f"文件 {file_path} 无需处理")
            return None
        elif index != 0:
            new_content = content[index:]
            new_file_path = file_path.replace('.', '-副本.')
            with open(new_file_path, 'wb') as new_file:
                new_file.write(new_content)
            return new_file_path
        else:
            print(f"文件 {file_path} 无需处理")
            return None


def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_process():
    folder_path = folder_entry.get()
    include_subfolders = subfolders_var.get()
    process_folder(folder_path, include_subfolders)
    result_label.config(text="处理完成")
