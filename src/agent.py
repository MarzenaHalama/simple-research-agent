from google.genai import types
from src.config import get_client, get_generation_config, MODEL_NAME, MAX_LOOPS


def run_agent(prompt: str) -> str:
    client = get_client()
    config = get_generation_config()

    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    ]

    finished = False
    final_text = ""

    print("Agent started working...")

    for i in range(MAX_LOOPS):
        print(f"\n--- Iteration {i+1} - Searching and analyzing ---")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config,
        )

        response_content = response.candidates[0].content
        contents.append(response_content)

        for part in response_content.parts:
            if part.text:
                final_text = part.text
                print(final_text)

                if "finished: true" in part.text.lower():
                    finished = True

        if finished:
            break

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="Verify this data against another source or find additional details. "
                        "If you are 100$\%$ confident, summarize the answer and finish by writing 'FINISHED: TRUE'."
                    )
                ],
            )
        )

    clean_final_response = (
        final_text.replace("FINISHED: TRUE", "")
        .replace("finished: true", "")
        .strip()
    )

    print("\n" + "=" * 50)
    print("                 FINAL RESPONSE")
    print("=" * 50 + "\n")
    print(clean_final_response)
    print("\n" + "=" * 50)

    return clean_final_response
