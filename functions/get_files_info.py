import os


def get_files_info(working_directory, directory=None):
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_dir = os.path.abspath(os.path.join(abs_work_dir, directory))
        if not abs_dir.startswith(abs_work_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_dir):
            return f'Error: "{directory}" is not a directory'
        res = ""
        for entry in os.listdir(abs_dir):
            path = os.path.join(abs_dir, entry)
            res += f"{entry}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n"
        return res
    except Exception as e:
        return f"Error: {e}"
