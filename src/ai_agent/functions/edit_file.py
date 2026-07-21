import difflib

from ai_agent.sandbox import resolve_in_workdir


def edit_file(
    working_directory: str, file_path: str, old_string: str, new_string: str
) -> str:
    """Replace one exact occurrence of old_string with new_string in a file.

    Reads the file, requires old_string to appear exactly once, writes back the
    result, and returns a unified diff of the change. The file is left untouched
    on any error.

    Args:
        working_directory: The sandbox root.
        file_path: Target file, relative to working_directory.
        old_string: Exact text to replace. Must occur exactly once.
        new_string: Replacement text.

    Returns:
        A unified diff of the change on success, or an ``Error:``-prefixed
        string if the path escapes the sandbox, the file is missing,
        old_string is absent, or old_string is ambiguous (>1 match).
    """
    ...  # TODO 2.2.1: resolve_in_workdir, count occurrences, replace one, difflib diff


# TODO 2.2.2: define schema_edit_file: ChatCompletionToolParam mirroring
# schema_write_file's shape, then register it in available_functions and
# function_map in call_functions.py, and add "edit_file" to DANGEROUS in approval.py.
