# bootdev ai-agent project

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key: str | None = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("The API key was not found")


client= genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    )

print(response.text)


