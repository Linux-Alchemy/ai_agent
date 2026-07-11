import os
from openai.types.chat import ChatCompletionToolParam

from ai_agent.config import MAX_CHARS


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
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content: ChatCompletionToolParam = (
    {
        "type": "function",
        "function": {
            "name": "get_file_content",
            "description": "Read and return the contents of a single file, relative to the working directory, truncated to a maximum character count",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read, relative to the working directory",
                    }
                },
                "required": ["file_path"],
            },
        },
    }
)
