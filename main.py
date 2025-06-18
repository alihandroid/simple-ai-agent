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

user_prompt = sys.argv[1]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        required=["directory"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

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
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if res.text:
    print(res.text)

if len(res.function_calls) > 0:
    for fc in res.function_calls:
        print(f"Calling function: {fc.name}({fc.args})")

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
