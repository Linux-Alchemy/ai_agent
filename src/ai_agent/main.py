# bootdev ai-agent project

import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse, Content, Part
from argparse import ArgumentParser, Namespace

load_dotenv()
api_key: str | None = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("The API key was not found")

parser: ArgumentParser = ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Rnable verbose output")
args: Namespace = parser.parse_args()

if not isinstance(args.user_prompt, str):
    raise RuntimeError("The user prompt must be a string")

messages: list[Content] = [Content(role="user", parts=[Part(text=args.user_prompt)])]

client: genai.Client = genai.Client(api_key=api_key)
response: GenerateContentResponse = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
    )

if response.usage_metadata is None:
    raise RuntimeError("No usage metadata returned")

prompt_tokens: int | None =  response.usage_metadata.prompt_token_count
response_tokens: int | None = response.usage_metadata.candidates_token_count


if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens:{prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(response.text)
else:
    print(response.text)

#print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
#print(response.text)


