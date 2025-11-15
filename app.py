from flask import Flask, request, jsonify
from flask_cors import CORS
from db import insert_customer
from bson import ObjectId
import uuid
from agents.registrationAgent import MESSAGE_FIELDS, MESSAGE_PROMPTS, save_message_answer, get_next_message_question
from agents.travelAgent import get_next_question, agentic_response, TRAVEL_FIELDS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory session storage
sessions = {}

# ---------- Helper: convert ObjectId ----------
def convert_objectid(doc):
    if isinstance(doc, dict):
        return {k: convert_objectid(v) for k, v in doc.items()}
    if isinstance(doc, list):
        return [convert_objectid(i) for i in doc]
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc
        

# --------------------------------------------------
# 1️⃣ USER INFO MESSAGE BOT
# --------------------------------------------------
@app.route("/message", methods=["POST"])
def message():
    data = request.json
    user_id = data.get("user_id")
    text = data.get("text", "").strip()

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    if user_id not in sessions:
        sessions[user_id] = {"step": 0, "data": {}}

    session = sessions[user_id]

    # Save previous response
    save_message_answer(session, text)

    # Ask next question
    next_question = get_next_message_question(session)
    if next_question:
        return jsonify({"message": next_question, "user_id": user_id})

    # All answered → Save to DB
    inserted = insert_customer(session["data"])
    inserted = convert_objectid(inserted)

    del sessions[user_id]
    return jsonify({"message": "All data collected!", "data": inserted})


# --------------------------------------------------
# 2️⃣ AGENTIC TRAVEL MODE BOT
# --------------------------------------------------
@app.route("/travel-agent", methods=["POST"])
def travel_agent():
    data = request.json
    text = data.get("text", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if user_id not in sessions:
        sessions[user_id] = {"step": 0, "data": {}}

    session = sessions[user_id]

    # Save previous answer
    if session["step"] > 0 and text:
        session["data"][TRAVEL_FIELDS[session["step"] - 1]] = text

    # Ask next question
    next_q = get_next_question(session)
    if next_q:
        session["step"] += 1
        return jsonify({"message": next_q, "user_id": user_id})

    # All done → Generate AI reply
    reply = agentic_response(session)

    del sessions[user_id]
    return jsonify({"message": reply, "user_id": user_id})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
