# Main FastAPI application for Think41 E-commerce Chatbot
# This file handles all API endpoints, conversation management, and data persistence

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from app.models import User, Conversation, Message
from app.database import get_database
from app.config import settings
from app.chat_logic import chat_logic
from app.data_loader import load_sample_data
from typing import List, Optional
from datetime import datetime

# Initialize FastAPI application
app = FastAPI(title="Think41 E-commerce Chatbot API", version="1.0.0")

# Configure CORS for frontend-backend communication
# This allows the React frontend to make API calls to the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # List of allowed origins (frontend URLs)
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def fix_id(doc):
    """
    Convert MongoDB ObjectId to string for JSON serialization
    MongoDB uses ObjectId type which can't be directly serialized to JSON
    """
    doc["_id"] = str(doc["_id"])
    return doc

# Get database connection - this will be used throughout the application
db = get_database()

# Load sample data on application startup
# This ensures the database has realistic e-commerce data for testing
@app.on_event("startup")
async def startup_event():
    load_sample_data()

# ============================================================================
# CONVERSATION MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/conversations", response_model=Conversation)
def create_conversation(conv: Conversation):
    """
    Create a new conversation for chat history
    Each conversation represents a chat session between user and bot
    """
    conv_dict = conv.dict(by_alias=True)
    db.conversations.insert_one(conv_dict)
    return conv

@app.get("/conversations/{conv_id}", response_model=Conversation)
def get_conversation(conv_id: str):
    """
    Retrieve conversation details by conversation ID
    Used for loading chat history
    """
    conv = db.conversations.find_one({"_id": conv_id})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return fix_id(conv)

@app.get("/users/{user_id}/conversations", response_model=List[Conversation])
def get_user_conversations(user_id: str):
    """
    Get all conversations for a specific user
    Returns only the last 10 conversations (most recent first)
    This prevents database bloat and improves performance
    """
    # Get only the last 10 conversations, sorted by most recent first
    convs = list(db.conversations.find({"user_id": user_id}).sort("updated_at", -1).limit(10))
    
    # For each conversation, get the first user message to use as title
    # This makes the conversation history more readable
    conversations_with_titles = []
    for conv in convs:
        # Get the first user message in this conversation
        first_message = db.messages.find_one(
            {"conversation_id": conv["_id"], "sender": "user"},
            sort=[("timestamp", 1)]
        )
        
        # Create conversation object with title
        conv_with_title = fix_id(conv)
        if first_message:
            # Truncate the message if it's too long (like ChatGPT does)
            title = first_message["content"]
            if len(title) > 50:
                title = title[:47] + "..."
            conv_with_title["title"] = title
        else:
            conv_with_title["title"] = "New conversation"
        
        conversations_with_titles.append(conv_with_title)
    
    return conversations_with_titles

# ============================================================================
# MESSAGE MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/messages", response_model=Message)
def create_message(msg: Message):
    """
    Create a new message in the database
    Used for storing individual chat messages
    """
    msg_dict = msg.dict(by_alias=True)
    db.messages.insert_one(msg_dict)
    return msg

@app.get("/conversations/{conv_id}/messages", response_model=List[Message])
def get_conversation_messages(conv_id: str):
    """
    Get all messages for a specific conversation
    Used for loading chat history when user clicks on a conversation
    """
    msgs = list(db.messages.find({"conversation_id": conv_id}))
    return [fix_id(m) for m in msgs]

# ============================================================================
# MAIN CHAT API ENDPOINT
# ============================================================================

@app.post("/api/chat")
def chat(
    user_id: str = Body(...),      # Required: User ID for conversation tracking
    message: str = Body(...),      # Required: User's message
    conversation_id: Optional[str] = Body(None)  # Optional: Continue existing conversation
):
    """
    Main chat endpoint that handles all user queries
    This is the core of the RAG system - it processes user input, queries the database,
    and generates contextual responses using the LLM
    """
    now = datetime.utcnow()
    
    # ============================================================================
    # CONVERSATION MANAGEMENT
    # ============================================================================
    
    # If conversation_id is provided, use it; else, create new conversation
    if conversation_id:
        # Continue existing conversation
        conv = db.conversations.find_one({"_id": conversation_id})
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        # Update the conversation's last activity timestamp
        db.conversations.update_one({"_id": conversation_id}, {"$set": {"updated_at": now}})
    else:
        # Create new conversation
        conversation_id = str(ObjectId())
        conv_doc = {
            "_id": conversation_id,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now
        }
        db.conversations.insert_one(conv_doc)
        
        # ============================================================================
        # CONVERSATION CLEANUP - Keep only last 10 conversations per user
        # ============================================================================
        # This prevents database bloat and improves performance
        # Get all conversations for this user, sorted by updated_at descending
        all_convs = list(db.conversations.find({"user_id": user_id}).sort("updated_at", -1))
        if len(all_convs) > 10:
            # Delete conversations beyond the 10th one
            convs_to_delete = all_convs[10:]
            for conv in convs_to_delete:
                conv_id = conv["_id"]
                # Delete the conversation and all its messages
                db.conversations.delete_one({"_id": conv_id})
                db.messages.delete_many({"conversation_id": str(conv_id)})
    
    # ============================================================================
    # MESSAGE STORAGE
    # ============================================================================
    
    # Insert user's message into database
    user_msg_id = str(ObjectId())
    user_msg_doc = {
        "_id": user_msg_id,
        "conversation_id": conversation_id,
        "sender": "user",
        "content": message,
        "timestamp": now
    }
    db.messages.insert_one(user_msg_doc)

    # ============================================================================
    # RAG SYSTEM - RETRIEVAL AND GENERATION
    # ============================================================================
    
    # Get conversation history for context (last 10 messages)
    # This helps the LLM understand the conversation flow
    history = list(db.messages.find({"conversation_id": conversation_id}).sort("timestamp", -1).limit(10))
    history = list(reversed(history))  # Reverse to get chronological order
    
    # Use the enhanced chat logic with RAG
    # This is where the magic happens - database query + LLM generation
    ai_response = chat_logic.generate_contextual_response(message, history)
    
    # Insert AI response into database
    ai_msg_id = str(ObjectId())
    ai_msg_doc = {
        "_id": ai_msg_id,
        "conversation_id": conversation_id,
        "sender": "ai",
        "content": ai_response,
        "timestamp": datetime.utcnow()
    }
    db.messages.insert_one(ai_msg_doc)
    
    # Return the complete response with conversation tracking
    return {
        "conversation_id": conversation_id,
        "user_message": user_msg_doc,
        "ai_message": ai_msg_doc
    }
