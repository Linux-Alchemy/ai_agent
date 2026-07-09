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
    # TODO 1: Build absolute paths and validate file_path is inside
    #         working_directory (abspath + normpath(join) + commonpath check).
    #         If it escapes, return:
    #         f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # TODO 2: If the target is not an existing regular file (os.path.isfile),
    #         return:
    #         f'Error: "{file_path}" does not exist or is not a regular file'

    # TODO 3: If the target does not end with ".py", return:
    #         f'Error: "{file_path}" is not a Python file'

    # TODO 4: Build the command list, e.g. ["python", absolute_file_path].

    # TODO 5: If args were provided, .extend() the command list with them.

    # TODO 6: subprocess.run the command — set cwd to working_directory,
    #         capture_output=True, text=True, timeout=30. Assign the result.

    # TODO 7: Build the output string from the CompletedProcess:
    #         - non-zero returncode -> include "Process exited with code X"
    #         - empty stdout AND empty stderr -> "No output produced"
    #         - otherwise -> stdout prefixed "STDOUT:", stderr prefixed "STDERR:"

    # TODO 8: Return the output string.

    # TODO 9: Wrap the above in try/except; on any exception return:
    #         f"Error: executing Python file: {e}"
    ...
