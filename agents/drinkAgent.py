import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fields and prompts for the travel agent
FIELDS = ["budget", "comfort_level","food_Style","food_type", "group_size"]
PROMPTS = {
    "budget": "What is your budget for this travel?",
    "comfort_level": "What comfort level do you prefer? (low/medium/high)",
    "food_Style": "What is your preferred food style? (vegan/vegetarian/non-vegetarian)",
    "food_type": "What type of food do you prefer? (SriLanka/Indian/Chinese/Italian/Mexican/etc.)",
    "group_size": "How many people are traveling?"
}

def get_next_question(session: dict) -> str:
    """Return the next question based on the current step."""
    step = session.get("step", 0)
    if step >= len(FIELDS):
        return None
    return PROMPTS[FIELDS[step]]

def send_to_qwen3(food_data: dict) -> str:
    """Send the collected data to Qwen3 and return the response."""
    print("Sending travel data to Qwen3:", travel_data)
    prompt = f"""
    You are a smart food recommendation assistant. A tourist provided this info: {food_data}.
    Recommend the best mode of travel (bus, taxi, train, rental car, cycling, walking)
    and give reasoning based on distance, budget, comfort, and group size.
    """
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_TOKEN"),
    )
    completion = client.chat.completions.create(
        model="Qwen/Qwen3-VL-235B-A22B-Thinking",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=0.95
    )
    return completion.choices[0].message.content


# Example usage
if __name__ == "__main__":
    session = {"step": 0}
    travel_data = {}
    while True:
        question = get_next_question(session)
        if not question:
            break
        answer = input(question + " ")
        travel_data[FIELDS[session["step"]]] = answer
        session["step"] += 1

    recommendation = send_to_qwen3(travel_data)
    print("Recommendation:", recommendation)
