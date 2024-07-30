# 放大.py
import os
import sys
import chardet


#判断文件编码格式
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def scale_coordinates(coords, scale):
    # 将坐标列表中的所有坐标乘以放大倍数
    scaled_coords = [int(coord) * scale for coord in coords]
    return scaled_coords

def scale_atlas_file(file_path, scale):
    scale = int(scale)
    print(f"放大倍数为：{scale}倍")
    encoding = detect_encoding(file_path)
    with open(file_path, 'r',encoding=encoding) as f:
        content = f.read()

    if 'bounds:' in content or 'offsets:' in content:
        scale_atlas_file_4(file_path, scale)
    else:
        scale_atlas_file_3(file_path, scale)
    
def scale_atlas_file_3(file_path, scale):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r',encoding=encoding) as f:
        lines = f.readlines()

    processed_lines = []
    current_texture_info = None

    for line in lines:
        line = line.strip()
        if line.endswith('.png'):
            # 发现图片文件名
            current_texture_info = {'name': line, 'scale': scale}
        elif line.startswith('size:'):
            # 更新图片尺寸
            size_parts = line.split(': ')[1].split(',')
            new_size = [int(part) * scale for part in size_parts]
            line = f'size: {new_size[0]},{new_size[1]}'
        elif line.startswith(('xy:', 'orig:', 'offset:')):
            # 更新坐标信息
            coords_parts = line.split(': ')[1].split(',')
            new_coords = scale_coordinates(coords_parts, scale)
            line = f'{line.split(":")[0]}: {new_coords[0]},{new_coords[1]}'

        if current_texture_info:
            # 如果当前处理的是图片信息块，更新块中的所有相关信息
            processed_lines.append(line)
            if line.startswith('index:'):
                current_texture_info = None
        else:
            processed_lines.append(line)
    print("Atlas 文件已更新。")
    # 将处理后的内容写回 .atlas 文件
    with open(file_path, 'w',encoding=encoding) as f:
        f.write('\n'.join(processed_lines))

        

def scale_atlas_file_4(file_path, scale):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r',encoding=encoding) as f:
        lines = f.readlines()

    processed_lines = []
    current_texture_info = None

    for line in lines:
        line = line.strip()
        if line.endswith('.png'):
            # 发现图片文件名
            current_texture_info = {'name': line, 'scale': scale}     
        elif line.startswith('size:'):
            # 更新图片尺寸
            size_parts = line.split(':')[1].split(',')
            new_size = [int(part) * scale for part in size_parts]
            line = f'size: {new_size[0]},{new_size[1]}'
        elif line.startswith(('bounds:', 'offsets:')):
            # 更新坐标信息
            coords_parts = line.split(':')[1].split(',')
            new_coords = scale_coordinates(coords_parts, scale)
            line = f'{line.split(":")[0]}: {new_coords[0]},{new_coords[1]},{new_coords[2]},{new_coords[3]}'
        elif line.startswith('rotate:'):
         
            pass

        if current_texture_info:
            # 如果当前处理的是图片信息块，更新块中的所有相关信息
            processed_lines.append(line)
            if line.startswith('index:'):
                current_texture_info = None
        else:
            processed_lines.append(line)
    print("Atlas 文件已更新。")
    # 将处理后的内容写回 .atlas 文件
    with open(file_path, 'w',encoding=encoding) as f:
        f.write('\n'.join(processed_lines))

        
      
if __name__ == "__main__":
    # 从命令行参数获取文件路径和放大倍数
    atlas_file_path = sys.argv[1]
    scale_factor = int(sys.argv[2])
    scale_atlas_file(atlas_file_path, scale_factor)
    print("Atlas 文件已更新。")
