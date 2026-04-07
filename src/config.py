import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in .env file")
    return genai.Client(api_key=api_key)


def get_grounding_tool():
    return types.Tool(google_search=types.GoogleSearch())

# Content generation config for the agent
# Defines the agent's role, system instructions, and tools available during operation.
def get_generation_config():
    return types.GenerateContentConfig(
        tools=[get_grounding_tool()],
        temperature=0.2, # controls response creativity, lower value = more precise answers
        system_instruction=(
            "You are an agent that helps find and verify information on a given topic. "
            "You work methodically — every answer must be backed by concrete sources.\n\n"

            "Always cite your sources (website name, article, or organization).\n"
            "Distinguish confirmed facts from speculation and opinions.\n"
            "If sources contradict each other, clearly indicate this and present both versions.\n"
            "Be concise and factual, avoid unnecessary filler.\n\n"

            "Perform your work in 5 stages:\n\n"

            "Stage 1: RECONNAISSANCE\n"
            "Find basic information on the given topic from at least 2 sources."
            "Present preliminary findings as bullet points. "
            "Stage 2: CROSS-VERIFICATION\n"
            "Check previous findings against other, independent sources. "
            "Correct any errors or inaccuracies. "
            "Add missing details, dates, numbers, context. "
            "Stage 3: CONTRASTING SOURCE ANALYSIS\n"
            "If you encounter conflicting information, analyze it thoroughly. "
            "Indicate which sources are more credible and why. "
            "Stage 4: PRELIMINARY SUMMARY\n"
            "Based on gathered and verified information, write an organized summary. "
            "Stage 5: FINALIZATION\n"
            "Review all information once more, ensure the summary is complete and accurate. "
            "At the very end write exactly: 'FINISHED: TRUE'."
        ),
    )


MODEL_NAME = "gemini-3-flash-preview"
MAX_LOOPS = 5
