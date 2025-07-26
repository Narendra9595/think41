from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# User schema
class User(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str

# Conversation schema
class Conversation(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Message schema
class Message(BaseModel):
    id: str = Field(..., alias="_id")
    conversation_id: str
    sender: str  # 'user' or 'ai'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Helper schemas for nested responses (optional)
class ConversationWithMessages(BaseModel):
    conversation: Conversation
    messages: List[Message]

class UserWithConversations(BaseModel):
    user: User
    conversations: List[ConversationWithMessages]