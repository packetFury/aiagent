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

def generate_response(client, message, verbose=False):
    # Set maximum iterations to prevent infinite loops
    MAX_ITERATIONS = config.MAX_ITERS

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

    iters = 0
    # Start the feedback loop
    while iters < MAX_ITERATIONS:
        iters =+ 1

        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=message,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt)
        )
    

        function_calls = []
        candidate = None
        final_text = ""
        # Check for whether the model called one of our functions, then get that metadata
        # Step 1: Get the parts from the first candidate.
        try:
            candidate = response.candidates[0]
        except (IndexError, AttributeError):
            print("Model response was empty or blocked")
            return

        # Step 2: Iterate content parts to find the function calls if they exist
        for part in candidate.content.parts:
            if part.function_call:
                function_calls.append(part.function_call)
            if part.text:
                final_text += part.text

        # Step 2.5: If no function calls were found by iterating parts, check for API mismatch with old/alternate attributes
        if not function_calls:
            if hasattr(candidate, 'function_calls') and candidate.function_calls:
                function_calls = candidate.function_calls
            elif hasattr(candidate, 'function_call') and candidate.function_call:
                function_calls = [candidate.function_call] # Wrap in a list for consistency

        # Step 3: Check for response.text to determine if this is the final output. If it is, return it.
        if final_text and not function_calls:
            print(final_text)
            return

        # Step 4: If there were function calls, prepare responses.
        if function_calls:
            tool_responses = []
            # Now iterate over the list and execute the functions.
        for call in function_calls:
            # Step 4: Second response that actually calls the function the agent identified.
            tool_response = call_function(call, verbose)
            tool_responses.append(tool_response)

        # Add the model's function call and the tool's output to conversation history.
        message.append(candidate.content)
        message.extend(tool_responses)

        # Call API again to get the final answer
        continue

        # Append API usage data if verbose flag is toggled.
        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def call_function(call, verbose=False):
    function_name = call.name
    function_args = call.args
    if verbose:
            print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")
    function_dict = {
        "get_files_info": get_files_info.get_files_info,
        "get_file_content": get_file_content.get_file_content,
        "run_python_file": run_python_file.run_python_file,
        "write_file": write_file.write_file,
    }
    
    if function_name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    args = dict(call.args)
    args["working_directory"] = config.WORKING_DIR
    function_result = function_dict[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )

if __name__ == "__main__":
    main()