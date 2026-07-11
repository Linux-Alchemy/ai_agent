# bootdev ai-agent project

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from argparse import ArgumentParser, Namespace
from ai_agent.prompts import system_prompt
from ai_agent.call_functions import available_functions
import json

load_dotenv()
api_key: str | None = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("The API key was not found")

parser: ArgumentParser = ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args: Namespace = parser.parse_args()

if not isinstance(args.user_prompt, str):
    raise RuntimeError("The user prompt must be a string")

messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

client: OpenAI = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
response: ChatCompletion = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    
)

if response.usage is None:
    raise RuntimeError("No usage metadata returned")

prompt_tokens: int = response.usage.prompt_tokens
response_tokens: int = response.usage.completion_tokens

message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")

else:
    print(message.content)

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens:{prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    

