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
    ...  # TODO 1.3.1: join + realpath, then commonpath containment check
