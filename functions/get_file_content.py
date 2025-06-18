import os

MAX_CHARS = 10_000


def get_file_content(working_directory, file_path):
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(abs_work_dir, file_path))
        if not abs_path.startswith(abs_work_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        res = ""
        with open(abs_path, "r") as f:
            res = f.read(MAX_CHARS)
        if os.path.getsize(abs_path) > MAX_CHARS:
            res += f'[...File "{abs_path}" truncated at 10000 characters]'
        return res
    except Exception as e:
        return f"Error: {e}"
