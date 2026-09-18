import os
import platform
from datetime import datetime


def system_info():
    return {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Python": platform.python_version(),
        "Computer": platform.node()
    }


def current_time():
    return datetime.now().strftime("%I:%M:%S %p")


def current_date():
    return datetime.now().strftime("%d %B %Y")


def list_folder(path="."):
    try:
        path = os.path.abspath(path)

        if not os.path.exists(path):
            return f"Folder not found: {path}"

        if not os.path.isdir(path):
            return f"Not a folder: {path}"

        items = os.listdir(path)

        if not items:
            return "Folder is empty."

        result = []

        for item in items:
            full_path = os.path.join(path, item)

            if os.path.isdir(full_path):
                result.append(f"[FOLDER] {item}")
            else:
                result.append(f"[FILE]   {item}")

        return "\n".join(result)

    except Exception as e:
        return f"Error reading folder: {e}"


def file_exists(path):
    return os.path.exists(os.path.abspath(path))


def folder_exists(path):
    return os.path.isdir(os.path.abspath(path))