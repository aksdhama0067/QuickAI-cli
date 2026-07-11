import os
import argparse
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(prompt: str, model_name: str = "gemini-2.5-flash"):
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f" Error connecting to API: {e}\nMake sure GEMINI_API_KEY is set in your environment."


def main():
    parser = argparse.ArgumentParser(
        description=" QuickAI CLI: A zero-friction AI assistant directly in your terminal."
    )

    # Arguments
    parser.add_argument("query", type=str, nargs="?", help="Your quick question or prompt for the AI")
    parser.add_argument("-f", "--file", type=str,
                        help="Path to a text or code file you want the AI to review/summarize")
    parser.add_argument("-r", "--review", action="store_true",
                        help="Ask the AI to specifically bug-hunt and review code")

    args = parser.parse_args()

    # Step 1: handle file input
    file_content = ""
    if args.file:
        if not os.path.exists(args.file):
            print(f" Error: File '{args.file}' not found.")
            return
        with open(args.file, "r", encoding="utf-8") as f:
            file_content = f.read()

    # Step 2: dynamic prompt based on user flags
    final_prompt = ""
    if args.review and file_content:
        final_prompt = f"Please review this code for bugs, performance issues, and optimization possibilities:\n\n```python\n{file_content}\n```"
    elif file_content:
        user_instruction = args.query if args.query else "Summarize the key points of this file clearly."
        final_prompt = f"{user_instruction}\n\nFile Content:\n{file_content}"
    elif args.query:
        final_prompt = args.query
    else:
        parser.print_help()
        return

    # Step 3: run the query
    print(" Thinking...")
    ai_output = get_ai_response(final_prompt)

    print("\n AI Response:")
    print(ai_output)


if __name__ == "__main__":
    main()
