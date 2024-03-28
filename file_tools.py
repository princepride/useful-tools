import os
import fnmatch

def folder_scan(paths_str, ignore_patterns_str="", save_to_file=False, print_file_content=False):
    paths = [path.strip() for path in paths_str.split('\n')]  # 将输入的字符串分割成列表,并删除头尾空字符
    ignore_patterns = [pattern.strip() for pattern in ignore_patterns_str.split('\n')] if ignore_patterns_str else []
    all_output = []  # 用于收集所有文件夹的输出
    print(ignore_patterns)
    def is_ignored(path, ignore_patterns):
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
            if os.path.isdir(path) and fnmatch.fnmatch(path + '/', pattern):
                return True
        return False

    for path in paths:  # 处理每个路径
        output = []

        def scan_folder(folder, depth=0):
            entries = sorted(os.listdir(folder))
            for i, entry in enumerate(entries):
                full_path = os.path.join(folder, entry)
                if is_ignored(full_path, ignore_patterns):
                    continue

                # 使用不同的前缀表示层级关系
                prefix = "    " * depth + ("└── " if i == len(entries) - 1 else "├── ")
                if os.path.isdir(full_path):
                    output.append(f"{prefix}[Folder] {entry}")
                    scan_folder(full_path, depth + 1)
                else:
                    output.append(f"{prefix}[File] {entry}")
                    if print_file_content:
                        try:
                            with open(full_path, "r", encoding="utf-8") as file:
                                content = file.read()
                                output.append(f"{prefix}  <<File Content>>:\n{content}\n")
                        except:
                            output.append(f"{prefix}  Unable to read file content.\n")

        # 将根目录添加到输出
        root_dir_name = os.path.basename(os.path.normpath(path))
        output.append(f"[Folder] {root_dir_name}")
        scan_folder(path)
        all_output.extend(output + ["\n"])  # 添加空行作为文件夹之间的分隔符

    # 根据用户选择决定是返回字符串还是保存到文件
    if save_to_file:
        with open("folder_scan_output.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(all_output))
        return "Output saved to folder_scan_output.txt"
    else:
        return "\n".join(all_output)
    
def export_pdf_text(paths_str):
    from PyPDF2 import PdfReader

    def extract_text_from_pdf(pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    # 导出PDF文本内容
    text = extract_text_from_pdf(paths_str)
    return text