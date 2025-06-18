import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

verbose = False
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python3 main.py <prompt> [--verbose]")
    sys.exit(1)
elif len(sys.argv) == 3:
    if sys.argv[2] == "--verbose":
        verbose = True
    else:
        print("Usage: python3 main.py <prompt> [--verbose]")
        sys.exit(1)

system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
user_prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

res = client.models.generate_content(
    model=model,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)
print(res.text)

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
