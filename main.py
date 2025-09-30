import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    args = sys.argv[1:]
    if not args:
        raise ValueError("Usage example: main.py \"type your prompt here\"")
        sys.exit(1)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=args[0]
    )
    print(response.text)
    if "--verbose" in args:
        print(f"User prompt: {args[0]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
