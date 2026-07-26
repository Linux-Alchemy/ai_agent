# bootdev ai-agent project

import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolMessageParam,
)
from argparse import ArgumentParser, Namespace
from ai_agent.prompts import system_prompt
from ai_agent.call_functions import available_functions, call_function, console
from rich.panel import Panel

# TODO 3.1.2 (imports):
# - Add `console` to the import from `ai_agent.call_functions` above. This reuses
#   the one Console instance already created there; do not create another here.
# - Import `Panel` from `rich.panel` for the final response.


def main() -> None:
    """Run one turn of the agent: prompt in, tool call out, result printed.

    Reads the user prompt from the command line, sends it to the model with the
    available tool schemas, and executes whichever tool the model asks for. The
    tool's result is not yet fed back to the model.

    Raises:
        RuntimeError: If the API key is missing or the response carries no usage
            metadata.
        ValueError: If a tool call returns an empty result.
    """
    load_dotenv()
    api_key: str | None = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("The API key was not found")

    parser: ArgumentParser = ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--auto-approve", action="store_true", help="Enable YOLO mode. Use at your own risk")
    args: Namespace = parser.parse_args()

    if not isinstance(args.user_prompt, str):
        raise RuntimeError("The user prompt must be a string")

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]


    print(f"User prompt: {args.user_prompt}")

    client: OpenAI = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    for _ in range(20):
        with console.status(
            "[bold white]Thinking...[/]",
            spinner = "dots",
            spinner_style = "white",
            speed = 1.0,
        ):
            response: ChatCompletion = client.chat.completions.create(
                model="google/gemini-2.5-flash",
                messages=messages,
                tools=available_functions,
                temperature=0,
            )

        if response.usage is None:
            raise RuntimeError("No usage metadata returned")

        prompt_tokens: int = response.usage.prompt_tokens
        response_tokens: int = response.usage.completion_tokens
        
        if args.verbose:
            console.print(
                f"Prompt tokens: {prompt_tokens}",
                style = "dim"
            )
            console.print(
                f"Response tokens: {response_tokens}",
                style = "dim"
            )


        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            console.print(
                Panel(
                    message.content or "",
                    title = "[bold blue]Final Response",
                    border_style = "blue",
                )
            )
            return

        for tool_call in message.tool_calls:
            if tool_call.type == "function":
                result_message: ChatCompletionToolMessageParam = call_function(
                    tool_call, args.verbose, args.auto_approve
                )
                if not result_message["content"]:
                    raise ValueError("Content is empty")
                messages.append(result_message)

    else:
        print("Reached maximum turns")
        sys.exit(1)



if __name__ == "__main__":
    main()
