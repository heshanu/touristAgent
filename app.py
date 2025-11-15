from flask import Flask, request, jsonify
from flask_cors import CORS
from db import insert_customer  # make sure this returns JSON serializable dict
from bson import ObjectId  # if using MongoDB ObjectId

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

# Temporary in-memory storage for active sessions
sessions = {}

# Fields to collect in order
FIELDS = ["name", "age", "address", "foods", "beverages", "hotels", "mode_of_travel", "duration", "budget"]

# Questions for each field
PROMPTS = {
    "name": "What is your full name?",
    "age": "What is your age?",
    "address": "What is your home address?",
    "foods": "What is your favorite food?",
    "beverages": "What is your favorite beverage?",
    "hotels": "Which hotel will you stay at?",
    "mode_of_travel": "What mode of travel will you use?",
    "duration": "How long will your trip last?",
    "budget": "What is your budget for the trip?"
}

# Helper to convert ObjectId to string
def convert_objectid(doc):
    if isinstance(doc, dict):
        return {k: convert_objectid(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_objectid(i) for i in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

@app.route("/message", methods=["POST", "OPTIONS"])
def message():
    if request.method == "OPTIONS":
        # Handle preflight CORS
        return jsonify({}), 200

    data = request.json
    user_id = data.get("user_id")
    text = data.get("text", "").strip()

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    # Initialize session if new
    if user_id not in sessions:
        sessions[user_id] = {"step": 0, "data": {}}

    session = sessions[user_id]
    step = session["step"]

    # Save previous answer
    if step > 0:
        field = FIELDS[step - 1]
        session["data"][field] = text

    # Check if all fields collected
    if step >= len(FIELDS):
        # Insert into MongoDB
        inserted_doc = insert_customer(session["data"])
        inserted_doc = convert_objectid(inserted_doc)  # make JSON safe
        response = {
            "message": "All information collected successfully! Thank you",
            "data": inserted_doc
        }
        del sessions[user_id]  # Clear session
        return jsonify(response)

    # Ask next question
    next_field = FIELDS[step]
    session["step"] += 1
    return jsonify({"message": PROMPTS[next_field]})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
