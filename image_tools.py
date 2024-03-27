from PIL import Image
import os

def image_convert(paths_str, target_width, target_height, target_format):
    paths = [path.strip() for path in paths_str.split('\n')]  # 将输入的字符串分割成列表,并删除头尾空字符
    output_messages = []

    for path in paths:
        if os.path.isfile(path):
            try:
                img = Image.open(path)
                img_resized = img.resize((target_width, target_height), Image.ANTIALIAS)
                
                # 构建新的文件名
                base_name = os.path.splitext(path)[0]
                new_path = f"{base_name}_converted.{target_format}"
                
                img_resized.save(new_path)
                output_messages.append(f"Image converted: {path} -> {new_path}")
            except Exception as e:
                output_messages.append(f"Failed to convert image: {path}. Error: {str(e)}")
        else:
            output_messages.append(f"File not found or not a valid image: {path}")

    return '\n'.join(output_messages)