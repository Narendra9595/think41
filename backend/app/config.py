import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB Configuration - Force Docker environment URI
    MONGO_URI = "mongodb://mongo:27017/ecommerce_bot"
    DATABASE_NAME = "ecommerce_bot"
    
    # LLM Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    GROQ_MODEL = "llama3-8b-8192"
    
    # OpenAI fallback (optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # CORS Configuration
    ALLOWED_ORIGINS = ["*"]  # For development
    
    # E-commerce specific settings
    RETURN_WINDOW_DAYS = 30
    SHIPPING_TIME_DAYS = 3-7

settings = Settings()
