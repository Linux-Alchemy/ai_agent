import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """Execute a Python file, scoped to a working directory.

    Runs ``file_path`` with the system ``python`` interpreter as a subprocess,
    confined to ``working_directory``, capturing its output. Execution is
    aborted after a 30-second timeout.

    Args:
        working_directory: The directory execution is confined to.
        file_path: Path to the target ``.py`` file, relative to
            working_directory.
        args: Optional command-line arguments passed through to the script.

    Returns:
        A string containing the captured STDOUT/STDERR (and a non-zero exit
        code notice, if any), or an ``Error:``-prefixed string if the path
        escapes working_directory, is missing, is not a regular file, is not a
        ``.py`` file, or the subprocess raises.
    """

    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command: list[str] = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(command,
                                cwd=working_dir_abs,
                                capture_output=True,
                                text=True,
                                timeout=30)

        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")

        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")

        return "\n".join(output)



    except Exception as e:
        return f"Error: executing Python file: {e}"


