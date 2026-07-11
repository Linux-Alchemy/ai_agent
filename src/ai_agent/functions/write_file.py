import os
from openai.types.chat import ChatCompletionToolParam


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write content to a file, scoped to a working directory.

    Overwrites the file if it already exists and creates any missing parent
    directories along the way.

    Args:
        working_directory: The directory the write is confined to.
        file_path: Path to the target file, relative to working_directory.
        content: The text to write.

    Returns:
        A success message reporting the number of characters written, or an
        ``Error:``-prefixed string if the path escapes working_directory,
        points at an existing directory, or a standard-library call raises.
    """
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            _ = f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file: ChatCompletionToolParam = (
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file, relative to the working directory, creating it if needed and overwriting it if it already exists",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write, relative to the working directory",
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to write to the file",
                    },
                },
                "required": ["file_path", "content"],
            },
        },
    }
)

