from langchain_huggingface import HuggingFaceEndpoint
from langchain.output_parsers.pydantic import PydanticOutputParser
from models.travel_info import TravelInfo
import os

TRAVEL_FIELDS = ["distance_km", "budget", "comfort_level", "group_size"]

PROMPTS = {
    "distance_km": "How many kilometers will you travel?",
    "budget": "What is your budget?",
    "comfort_level": "Preferred comfort? (low/medium/high)",
    "group_size": "How many people?"
}

# Parser
parser = PydanticOutputParser(pydantic_object=TravelInfo)

# Free HF model
model = HuggingFaceEndpoint(
    repo_id="google/gemma-2b",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
    max_new_tokens=200,
    temperature=0.3
)

def get_next_question(session):
    step = session["step"]
    if step >= len(TRAVEL_FIELDS):
        return None
    return PROMPTS[TRAVEL_FIELDS[step]]

def agentic_response(session):
    travel_data = session["data"]
    prompt = f"""
You are a smart travel assistant. Tourist info: {travel_data}
Recommend the best travel mode (bus, train, taxi, car, walking).
Return ONLY JSON like:
{parser.get_format_instructions()}
"""

    try:
        raw = model.invoke(prompt)
        parsed = parser.parse(raw)
        return parsed.json()
    except Exception as e:
        print("ERROR:", e)
        return "Unable to generate travel recommendation."
