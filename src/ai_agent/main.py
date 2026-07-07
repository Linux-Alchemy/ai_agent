# bootdev ai-agent project

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from argparse import ArgumentParser, Namespace

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
    {"role": "user", "content": args.user_prompt}
]

client: OpenAI = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
response: ChatCompletion = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

if response.usage is None:
    raise RuntimeError("No usage metadata returned")

prompt_tokens: int = response.usage.prompt_tokens
response_tokens: int = response.usage.completion_tokens

content: str | None = response.choices[0].message.content

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens:{prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(content)
else:
    print(content)
