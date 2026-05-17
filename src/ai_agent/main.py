# bootdev ai-agent project

import os
from dotenv import load_dotenv
from google import genai
import argparse

load_dotenv()
api_key: str | None = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("The API key was not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()



client= genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.user_prompt
    )

if response.usage_metadata is None:
    raise RuntimeError("No usage metadata returned")

print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)


