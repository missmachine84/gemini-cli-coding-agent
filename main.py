import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv

    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    run_agent_loop(client, messages, verbose)


def run_agent_loop(client, messages, verbose):

    for _ in range(20):  # safety: max 20 iterations

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # Add model response candidates into conversation
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        # If the model gives a final natural-language response
        if not response.function_calls:
            if response.text:
                print("Final response:")
                print(response.text)
            return

        # Handle tool calls
        for function_call_part in response.function_calls:

            tool_result = call_function(function_call_part, verbose)

            if (
                not tool_result.parts
                or not tool_result.parts[0].function_response
            ):
                raise Exception("empty function call result")

            result_dict = tool_result.parts[0].function_response.response

            # Print tool result every time
            print(result_dict)

            # Feed tool result back to model
            messages.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=str(result_dict))]
                )
            )

    print("Max iterations reached without conclusion.")


if __name__ == "__main__":
    main()
