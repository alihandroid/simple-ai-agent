import os


def write_file(working_directory, file_path, content):
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(abs_work_dir, file_path))
        if not abs_path.startswith(abs_work_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(abs_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
