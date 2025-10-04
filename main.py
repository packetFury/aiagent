import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions import tool_info, config, get_file_content, get_files_info, run_python_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    # Handle extra flags and arguments apart from the prompt.
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print("AI Code Assistant")
        print("Usage: python main.py \"type your prompt here\" [--verbose]")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    message = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_response(client, message, verbose)

def generate_response(client, message, verbose):
    # Tell the agent what local tools it has access to.
    available_functions = types.Tool(
        function_declarations=[
            tool_info.schema_get_files_info,
            tool_info.schema_write_file,
            tool_info.schema_get_file_content,
            tool_info.schema_run_python_file
        ]
    )

    # Obtain our system prompt from config.
    system_prompt = config.SYSTEM_PROMPT

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=message,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

    function_calls = []
    candidate = response.candidates[0]
    # Check for whether the model called one of our functions, then get that metadata
    # Step 1: Get the parts from the first candidate.
    try:
        candidate_parts = response.candidates[0].content.parts
    except (IndexError, AttributeError):
        print("Model response was empty or blocked")
        return

    # Step 2: Iterate content parts to find the function calls if they exist
    if candidate.content and candidate.content.parts:
        for part in candidate.content.parts:
            if part.function_call:
                function_calls.append(part.function_call)

    # Step 2.5: If no function calls were found by iterating parts, check for API mismatch with old/alternate attributes
    if not function_calls:
        if hasattr(candidate, 'function_calls') and candidate.function_calls:
            function_calls = candidate.function_calls
        elif hasattr(candidate, 'function_call') and candidate.function_call:
            function_calls = [candidate.function_call] # Wrap in a list for consistency
        elif response.text:
            # If there were no function calls, simply print the text response.
            print(response.text)

    # Step 3: If there were function calls, iterate over the list and split them out, then announce each call.
    for call in function_calls:
        function_name = call.name
        function_args = {k: v for k, v in call.args.items()}
        print(f"Calling function: {function_name}({function_args})")

    # Step 4: Second response that actually calls the function the agent identified.

    # Append API usage data if verbose flag is toggled.
    if verbose:
        print(f"User prompt: {message}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
