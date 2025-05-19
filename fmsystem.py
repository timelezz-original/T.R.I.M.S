import os
import os.path
from pathlib import Path
import win32security
import win32file
import win32con


PC_USERS = ["timelezz", "Administrator"]
UNACCESSIBLE_DIRS = ["$Recycle.Bin"]


def hidden_attributes(path):
    try:
        attrs = win32file.GetFileAttributes(str(path))
        return bool(attrs & win32con.FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        return False
    

def file_ownership(path):
    try:
        sd = win32security.GetFileSecurity(str(path), win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return name
    except Exception as e:
        return f"Error: {type(e).__name__}"


def readable_content(content, threshold=0.9):
    try:
        printable_chars = sum(c.isprintable() for c in content)
        return printable_chars / len(content) >= threshold
    except ZeroDivisionError:
        return False


def folder_scan(file_directory):
    for path in file_directory.iterdir():
        try:
            if path.is_dir():
                folder_scan(path)
            elif path.is_file():
                owner = file_ownership(path)
                if owner not in PC_USERS:
                    continue
                elif path.name not in UNACCESSIBLE_DIRS:
                    continue
                elif not hidden_attributes(path):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if readable_content(content):
                            print(f"{path} is user based and readable.")
                        else:
                            continue       
        except (UnicodeDecodeError, PermissionError, OSError) as e:
            continue


folder_scan(Path("C:/"))
input("All Done")

#total_files = sum(len(paths) for paths in file_paths_by_type.values())
#print(len(file_paths_by_type), "file types found.")
#print(total_files, "files found.", total_files)

def find_specified_files(filename, search_path):
    result = []

    for root, dir, files in os.walk(search_path):
        if filename in files: 
            result.append(os.path.join(root, filename))
        return result


def write_files(file_paths_by_type, output_file):
    with open(output_file, 'w') as f:
        for file_extension, paths in file_paths_by_type.items():
            f.write(f"File Type: {file_extension}\n")
            f.write("---------------\n")
            for path in paths:
                f.write(path + '\n')
            f.write("\n")


if __name__ == "__main__":
    file_ownership()