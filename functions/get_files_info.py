import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
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
