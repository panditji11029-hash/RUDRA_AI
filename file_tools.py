import os


BASE_DIR = os.path.abspath(".")


def safe_path(path):
    path = os.path.abspath(path)

    try:
        if os.path.commonpath([BASE_DIR, path]) != BASE_DIR:
            return None
    except ValueError:
        return None

    return path


def read_file(path):
    target = safe_path(path)

    if not target:
        return "Access denied: file must be inside the RUDRA project folder."

    if not os.path.exists(target):
        return f"File not found: {path}"

    if not os.path.isfile(target):
        return f"Not a file: {path}"

    try:
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()

        if not content:
            return "File is empty."

        return content

    except UnicodeDecodeError:
        return "This file is not a readable UTF-8 text file."

    except Exception as e:
        return f"Error reading file: {e}"


def create_folder(name):
    target = safe_path(name)

    if not target:
        return "Access denied: folder must be inside the RUDRA project folder."

    if os.path.exists(target):
        return f"Already exists: {name}"

    try:
        os.makedirs(target)
        return f"Folder created successfully: {name}"

    except Exception as e:
        return f"Error creating folder: {e}"


def create_text_file(name, content):
    target = safe_path(name)

    if not target:
        return "Access denied: file must be inside the RUDRA project folder."

    if os.path.exists(target):
        return f"File already exists: {name}"

    try:
        parent = os.path.dirname(target)

        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File created successfully: {name}"

    except Exception as e:
        return f"Error creating file: {e}"


def file_exists(path):
    target = safe_path(path)

    if not target:
        return False

    return os.path.isfile(target)


def folder_exists(path):
    target = safe_path(path)

    if not target:
        return False

    return os.path.isdir(target)