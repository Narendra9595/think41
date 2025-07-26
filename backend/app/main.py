from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from app.models import User, Conversation, Message
from typing import List
import os

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://grandhinarendrakumar:Geyjrq77USksXqap@cluster41.p2i211j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster41")
client = MongoClient(MONGO_URI)
db = client['ecommerce_bot']

app = FastAPI()

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility to convert MongoDB documents to dicts with string IDs
def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# --- User Endpoints ---
@app.post("/users", response_model=User)
def create_user(user: User):
    user_dict = user.dict(by_alias=True)
    db.users.insert_one(user_dict)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return fix_id(user)

# --- Conversation Endpoints ---
@app.post("/conversations", response_model=Conversation)
def create_conversation(conv: Conversation):
    conv_dict = conv.dict(by_alias=True)
    db.conversations.insert_one(conv_dict)
    return conv

@app.get("/conversations/{conv_id}", response_model=Conversation)
def get_conversation(conv_id: str):
    conv = db.conversations.find_one({"_id": conv_id})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return fix_id(conv)

@app.get("/users/{user_id}/conversations", response_model=List[Conversation])
def get_user_conversations(user_id: str):
    convs = list(db.conversations.find({"user_id": user_id}))
    return [fix_id(c) for c in convs]

# --- Message Endpoints ---
@app.post("/messages", response_model=Message)
def create_message(msg: Message):
    msg_dict = msg.dict(by_alias=True)
    db.messages.insert_one(msg_dict)
    return msg

@app.get("/conversations/{conv_id}/messages", response_model=List[Message])
def get_conversation_messages(conv_id: str):
    msgs = list(db.messages.find({"conversation_id": conv_id}))
    return [fix_id(m) for m in msgs]
