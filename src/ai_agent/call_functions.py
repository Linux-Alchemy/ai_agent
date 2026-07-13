# function schemas

from collections.abc import Callable
import json
from typing import Any

from openai.types.chat import (
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)

from ai_agent.functions.get_files_info import schema_get_files_info, get_files_info
from ai_agent.functions.get_file_content import schema_get_file_content, get_file_content
from ai_agent.functions.write_file import schema_write_file, write_file
from ai_agent.functions.run_python_file import schema_run_python_file, run_python_file



available_functions: list[ChatCompletionToolParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


def call_function(
    tool_call: ChatCompletionMessageFunctionToolCall, verbose: bool = False
) -> ChatCompletionToolMessageParam:
    """Execute the tool call the model requested and wrap the result for the model.

    Dispatches on the tool call's function name, injects the `working_directory`
    argument (which the model never sees), and calls the matching function.

    Args:
        tool_call: A function tool call taken from `message.tool_calls`. Its
            `function.arguments` field is a JSON string of keyword arguments.
        verbose: If True, also print the parsed arguments alongside the name.

    Returns:
        A tool message (`role`, `tool_call_id`, `content`) carrying either the
        function's string result or an error string if the name is unknown. The
        `tool_call_id` is what lets the model match this result to its request.
    """
    function_name: str = tool_call.function.name
    function_args: dict[str, Any] = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
    
    function_args["working_directory"] = "./calculator"

    result: str = function_map[function_name](**function_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }


