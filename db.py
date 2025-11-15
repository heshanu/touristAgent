from bson import ObjectId
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
collection = db["customers"]

def insert_customer(data: dict):
    """Insert a customer document into MongoDB and return the document with string _id"""
    result = collection.insert_one(data)
    data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return data
