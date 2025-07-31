# Think41 E-commerce Chatbot

A full-stack customer support chatbot for e-commerce clothing websites with RAG (Retrieval-Augmented Generation) capabilities.

## 🚀 Features

- **Intelligent Chat Interface**: Natural language processing for customer queries
- **RAG System**: Combines MongoDB data retrieval with LLM responses
- **Multi-Collection Support**: Handles users, orders, products, inventory
- **Conversation Management**: Persistent chat history with cleanup
- **Real-time Responses**: Fast database queries with contextual LLM generation
- **Modern UI**: React-based chat interface with responsive design

## 🏗️ Architecture

```
Frontend (React) → Backend (FastAPI) → MongoDB → LLM (Groq)
```

### Tech Stack
- **Frontend**: React, CSS Modules
- **Backend**: FastAPI, Python 3.11
- **Database**: MongoDB (Docker)
- **LLM**: Groq API
- **Containerization**: Docker Compose

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- Groq API key

### Quick Start

1. **Clone the repository**
```bash
   git clone <repository-url>
cd think41
   ```

2. **Set up environment variables**
   ```bash
   # Create backend/.env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > backend/.env
   ```

3. **Build and run with Docker**
   ```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🗄️ Database Schema

### Collections
- **users**: Customer profiles and information
- **orders**: Order details and status
- **order_items**: Individual items in orders
- **products**: Product catalog and pricing
- **inventory_items**: Stock levels and availability
- **conversations**: Chat conversation history
- **messages**: Individual chat messages

### Sample Data
The system includes realistic e-commerce data:
- 1,000+ user profiles
- 490,705 inventory items
- 181,759 order items
- Complete product catalog

## 🔧 API Endpoints

### Chat API
- `POST /api/chat` - Send message and get AI response
  - Body: `{ user_id, message, conversation_id? }`
  - Response: `{ conversation_id, user_message, ai_message }`

### User Management
- `POST /users` - Create user
- `GET /users/{user_id}` - Get user details
- `GET /users/{user_id}/conversations` - Get user conversations

### Conversation Management
- `GET /conversations/{conv_id}` - Get conversation
- `GET /conversations/{conv_id}/messages` - Get conversation messages

## 💬 Supported Queries

### Order Status
```
"What is the status of order 1626?"
"Order #1626 status: Cancelled"
```

### User Information
```
"user 24731"
"User 24731: Jeremy Salazar, Email: jeremy@example.com, Age: 28, Location: Ostend, Flanders"
```

### Product Queries
```
"satin headband price"
"Found 5 products:
• (ONE) 1 Satin Headband: $6.99 (Out of stock)
• (ONE) 1 Satin Headband: $6.99 (Out of stock)"
```

### Category Queries
```
"what products you have under socks category?"
"Products in socks category:
• Cotton Socks Pack - $12.99
• Wool Socks - $15.99"
```

### Location-based Queries
```
"any user from Rio Branco"
"Users from Rio Branco:
• Elizabeth Martinez (ID: 6578)
• Timothy Bush (ID: 457)"
```

### Return Policy
```
"what is your return policy?"
"Return Policy:
• You can return items within 30 days of purchase for a full refund
• Items must be unworn, unwashed, and in original packaging with tags attached"
```

## 🔄 RAG System

### How it Works
1. **Query Analysis**: Extract intent from user message
2. **Database Retrieval**: Query relevant MongoDB collections
3. **Context Building**: Combine retrieved data into context
4. **LLM Generation**: Generate natural response using Groq API
5. **Response Delivery**: Return formatted response to user

### Benefits
- **Accuracy**: Uses real database data, not hallucinations
- **Performance**: Fast database queries with minimal LLM usage
- **Consistency**: Same query always returns same data
- **Cost-effective**: Optimized LLM usage

## 🐳 Docker Configuration

### Services
- **mongo**: MongoDB database (port 27017)
- **backend**: FastAPI application (port 8000)
- **frontend**: React development server (port 3000)

### Volumes
- MongoDB data persistence
- Frontend hot-reloading for development

## 🛠️ Development

### Local Development
```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm install
npm start
```

### Code Structure
```
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── chat_logic.py    # RAG system implementation
│   │   ├── database.py      # MongoDB connection
│   │   ├── config.py        # Configuration management
│   │   ├── data_loader.py   # CSV to MongoDB loader
│   │   └── models.py        # Pydantic models
│   ├── datasets/            # Sample CSV files
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── api.js          # API communication
│   │   └── App.js          # Main application
│   └── package.json        # Node.js dependencies
└── docker-compose.yml      # Service orchestration
```

## 📊 Performance

### Database Performance
- Indexed queries for fast response times
- Connection pooling for efficient database access
- Query optimization for large datasets

### LLM Integration
- Context-aware responses
- Fallback handling for API failures
- Optimized prompt engineering

### Frontend Performance
- React hooks for efficient state management
- CSS modules for optimized styling
- Responsive design for all devices

## 🔒 Security

- CORS configuration for frontend-backend communication
- Input validation with Pydantic models
- Environment variable management for API keys
- Docker containerization for isolation

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues, please open an issue on GitHub.
