import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    """Return the text contents of a file, scoped to a working directory.

    Reads at most ``MAX_CHARS`` characters. If the file is longer than that,
    the returned string is truncated and a truncation notice is appended.

    Args:
        working_directory: The directory the read is confined to.
        file_path: Path to the target file, relative to working_directory.

    Returns:
        The file's contents (possibly truncated), or an ``Error:``-prefixed
        string if the path escapes working_directory, is not a regular file,
        or a standard-library call raises.
    """
    try:
        # TODO 1: resolve both paths to absolutes
        #   working_dir_abs = abspath(working_directory)
        #   target_file     = normpath(join(working_dir_abs, file_path))

        # TODO 2: guard — is target_file inside working_dir_abs?
        #   reuse the commonpath check from get_files_info.
        #   if it fails, return:
        #     f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # TODO 3: guard — is target_file actually a regular file? (os.path.isfile)
        #   if not, return:
        #     f'Error: File not found or is not a regular file: "{file_path}"'

        # TODO 4: open target_file for reading (use a `with` block),
        #   read MAX_CHARS characters into `content`

        # TODO 5: peek one more char — if `f.read(1)` is truthy, the file was
        #   longer than MAX_CHARS, so append this to content:
        #     f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        # TODO 6: return content
        ...

    except Exception as e:
        return f"Error: {e}"
