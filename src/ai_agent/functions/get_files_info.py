import os
from openai.types.chat import ChatCompletionToolParam

from ai_agent.sandbox import resolve_in_workdir


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """List the entries of a directory, scoped to a working directory.

    Args:
        working_directory: The directory the listing is confined to.
        directory: Path to the target directory, relative to working_directory.

    Returns:
        A newline-joined listing, one entry per line as
        ``- <name>: file_size=<bytes> bytes, is_dir=<bool>``, or an
        ``Error:``-prefixed string if the path escapes working_directory,
        is not a directory, or a standard-library call raises.
    """
    try:
        target_dir: str | None = resolve_in_workdir(working_directory, directory)
        if target_dir is None:
            return f'Error: Cannot resolve "{directory}" as it is outside the permitted directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        contents: list[str] = os.listdir(target_dir)
        result: list[str]= []
        for name in contents:
            full_path : str = os.path.join(target_dir, name)
            file_size: int = os.path.getsize(filename=full_path)
            is_directory: bool = os.path.isdir(s=full_path)
            result.append(f"- {name}: file_size={file_size} bytes, is_dir={is_directory}")
                
        return '\n'.join(result)

        
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info: ChatCompletionToolParam = { "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
