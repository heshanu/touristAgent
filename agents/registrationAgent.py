# Message agent fields
MESSAGE_FIELDS = [
    "name", "age", "address", "foods", "beverages",
    "hotels", "mode_of_travel", "duration", "budget"
]

MESSAGE_PROMPTS = {
    "name": "What is your full name?",
    "age": "What is your age?",
    "address": "What is your home address?",
    "foods": "What is your favorite food?",
    "beverages": "What beverage do you like?",
    "hotels": "Which hotel will you stay at?",
    "mode_of_travel": "Your preferred travel method?",
    "duration": "How long is your trip?",
    "budget": "What is your budget?"
}

def save_message_answer(session, text):
    step = session["step"]
    if step > 0:
        field = MESSAGE_FIELDS[step - 1]
        session["data"][field] = text

def get_next_message_question(session):
    step = session["step"]

    if step >= len(MESSAGE_FIELDS):
        return None

    field = MESSAGE_FIELDS[step]
    session["step"] += 1
    return MESSAGE_PROMPTS[field]
