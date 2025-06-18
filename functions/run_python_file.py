import os
import subprocess


def run_python_file(working_directory, file_path, arguments=""):
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_path = os.path.abspath(os.path.join(abs_work_dir, file_path))
        if not abs_path.startswith(abs_work_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        res = subprocess.run(
            ["python3", abs_path, arguments],
            timeout=30,
            capture_output=True,
            cwd=abs_work_dir,
        )

        if res.stdout == "" and res.stderr == "":
            return "No output produced."

        formatted_res = f"STDOUT:{res.stdout.decode("utf-8")}\n"
        formatted_res += f"STDERR:{res.stderr.decode("utf-8")}\n"
        if res.returncode != 0:
            formatted_res += f"Process exited with code {res.returncode}"
        return formatted_res
    except Exception as e:
        f"Error: executing Python file: {e}"
