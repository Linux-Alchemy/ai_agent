import os


def resolve_in_workdir(working_directory: str, file_path: str) -> str | None:
    """Resolve file_path under working_directory, or None if it escapes.

    Joins file_path onto working_directory and fully resolves the result —
    following symlinks and collapsing ``..`` — then confirms it still sits
    inside working_directory. Returns the resolved absolute path on success,
    or None if the path escapes the sandbox (including via symlink).

    Args:
        working_directory: The sandbox root. Assumed already realpath-resolved.
        file_path: Untrusted path, relative to working_directory.

    Returns:
        The resolved absolute path if contained, otherwise None.
    """
    working_dir_abs: str = os.path.abspath(working_directory)
    target_file: str = os.path.realpath(os.path.join(working_dir_abs, file_path))

    valid_target_file: bool = (
        os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    )

    if valid_target_file:
        return target_file
    return None

