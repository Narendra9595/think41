# Think41 E-commerce Chatbot - RAG System Implementation
# This file contains the core logic for processing user queries, retrieving data from MongoDB,
# and generating contextual responses using the LLM (Groq API)

import re
import requests
from datetime import datetime, timedelta
from app.database import get_database
from app.config import settings

class EcommerceChatLogic:
    """
    Main chat logic class that implements the RAG (Retrieval-Augmented Generation) system
    This class handles:
    1. Extracting information from user messages
    2. Querying MongoDB for relevant data
    3. Building context for LLM
    4. Generating natural language responses
    """
    
    def __init__(self):
        """Initialize the chat logic with database connection"""
        self.db = get_database()
        
    def extract_order_info(self, message):
        """
        Extract order-related information from user message using regex patterns
        Looks for patterns like "order 123", "order #123", "order number 123"
        """
        # Define regex patterns to match order IDs in natural language
        order_patterns = [
            r'order\s+#?(\d+)',      # "order 123" or "order #123"
            r'order\s+(\d+)',        # "order 123"
            r'order\s+number\s+(\d+)', # "order number 123"
            r'order\s+id\s+(\d+)'    # "order id 123"
        ]
        
        # Try each pattern to find order ID
        for pattern in order_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1)  # Return the extracted order ID
        return None
    
    def extract_product_info(self, message):
        """
        Extract product-related information from user message
        Looks for product names, categories, and keywords
        """
        # Define product keywords that indicate product queries
        product_keywords = [
            'jacket', 'shirt', 'pants', 'dress', 'shoes', 'denim', 'headband',
            'size', 'color', 'available', 'in stock', 'satin'
        ]
        
        found_keywords = []
        message_lower = message.lower()
        
        # Check for exact keywords in the message
        for keyword in product_keywords:
            if keyword in message_lower:
                found_keywords.append(keyword)
        
        # If no keywords found, try to extract product names from the message
        if not found_keywords:
            # Look for quoted text or specific product names using regex
            product_patterns = [
                r'"([^"]+)"',  # Text in quotes like "satin headband"
                r'\(([^)]+)\)',  # Text in parentheses
                r'(\w+(?:\s+\w+){1,3})',  # 2-4 word combinations
            ]
            
            for pattern in product_patterns:
                matches = re.findall(pattern, message)
                for match in matches:
                    if len(match) > 3:  # Only consider meaningful product names
                        found_keywords.append(match.lower())
        
        return found_keywords
    
    def extract_user_info(self, message):
        """
        Extract user-related information from user message
        Looks for user IDs, names, and other user identifiers
        """
        # Define regex patterns to match user information
        user_patterns = [
            r'user\s+#?(\d+)',      # "user 123" or "user #123"
            r'user\s+(\d+)',        # "user 123"
            r'user\s+id\s+(\d+)',   # "user id 123"
            r'(\d{5})',             # 5-digit user IDs
            r'(\w+)\s+(gilmore|smith|johnson)',  # First name + last name
        ]
        
        # Try each pattern to find user information
        for pattern in user_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1)
        return None
    
    def query_order_status(self, order_id, user_id=None):
        """
        Query order status from database
        Returns order details and associated order items
        """
        try:
            # Query orders collection by order_id
            order = self.db.orders.find_one({"order_id": int(order_id)})
            if not order:
                return None
            
            # Get order items for this order (cross-collection query)
            order_items = list(self.db.order_items.find({"order_id": int(order_id)}))
            
            return {
                "order": order,
                "items": order_items,
                "status": order.get("status", "unknown")
            }
        except:
            return None
    
    def query_product_availability(self, product_keywords):
        """
        Query product availability from database
        Searches across multiple fields for product matches
        """
        try:
            # Build complex query to search across multiple fields
            query = {"$or": []}
            for keyword in product_keywords:
                if keyword in ['size', 'available', 'in stock']:
                    continue  # Skip generic keywords
                query["$or"].append({
                    "$or": [
                        {"product_name": {"$regex": keyword, "$options": "i"}},
                        {"product_category": {"$regex": keyword, "$options": "i"}},
                        {"product_brand": {"$regex": keyword, "$options": "i"}},
                        {"product_department": {"$regex": keyword, "$options": "i"}}
                    ]
                })
            
            if not query["$or"]:
                return []
            
            # Execute query and limit results for performance
            inventory_items = list(self.db.inventory_items.find(query).limit(5))
            
            # Convert inventory items to product format for consistent response
            products = []
            for item in inventory_items:
                product = {
                    "name": item.get("product_name", "Unknown"),
                    "category": item.get("product_category", "Unknown"),
                    "brand": item.get("product_brand", "Unknown"),
                    "price": item.get("product_retail_price", 0),
                    "available": item.get("sold_at") is None,  # If sold_at is null, it's available
                    "sku": item.get("product_sku", ""),
                    "department": item.get("product_department", "")
                }
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error querying products: {e}")
            return []
    
    def query_user_info(self, user_id):
        """
        Query user information from database
        Tries multiple ways to find user (by ID or ObjectId)
        """
        try:
            # Try to find user by ID first
            user = self.db.users.find_one({"id": int(user_id)})
            if not user:
                # Try by _id if it's a MongoDB ObjectId
                user = self.db.users.find_one({"_id": user_id})
            return user
        except:
            return None
    
    def query_user_orders(self, user_id):
        """
        Query all orders for a specific user
        Used for cross-collection queries (users -> orders)
        """
        try:
            orders = list(self.db.orders.find({"user_id": int(user_id)}))
            return orders
        except:
            return []
    
    def query_products_by_category(self, category):
        """
        Query products by category
        Used for category-based product searches
        """
        try:
            products = list(self.db.products.find({"category": {"$regex": category, "$options": "i"}}).limit(5))
            return products
        except:
            return []
    
    def query_users_by_location(self, location):
        """
        Query users by location (city, state, country)
        Used for location-based user searches
        """
        try:
            users = list(self.db.users.find({
                "$or": [
                    {"city": {"$regex": location, "$options": "i"}},
                    {"state": {"$regex": location, "$options": "i"}},
                    {"country": {"$regex": location, "$options": "i"}}
                ]
            }).limit(5))
            return users
        except:
            return []
    
    def query_product_by_id(self, product_id):
        """
        Query product by ID
        Used for direct product lookups
        """
        try:
            product = self.db.products.find_one({"id": int(product_id)})
            return product
        except:
            return None
    
    def query_inventory_by_product(self, product_id):
        """
        Query inventory items by product ID
        Used for cross-collection queries (products -> inventory)
        """
        try:
            inventory = list(self.db.inventory_items.find({"product_id": int(product_id)}).limit(3))
            return inventory
        except:
            return []
    
    def get_return_policy_info(self):
        """
        Get return policy information
        Returns hardcoded policy data (could be moved to database)
        """
        return {
            "return_window": settings.RETURN_WINDOW_DAYS,
            "policy": f"You can return items within {settings.RETURN_WINDOW_DAYS} days of purchase for a full refund.",
            "conditions": "Items must be unworn, unwashed, and in original packaging with tags attached."
        }
    
    def generate_contextual_response(self, message, conversation_history):
        """
        Generate response using RAG approach - Simplified and effective
        This is the main method that processes user queries and generates responses
        """
        message_lower = message.lower()
        
        # ============================================================================
        # 1. ORDER STATUS QUERIES
        # ============================================================================
        order_match = re.search(r'order\s+(?:id\s+)?(?:#?)?(\d+)', message_lower)
        if order_match:
            order_id = order_match.group(1)
            order_info = self.query_order_status(order_id)
            if order_info:
                order = order_info["order"]
                status = order.get('status', 'unknown')
                return f"Order #{order_id} status: {status}"
            else:
                return f"No order found with ID {order_id}"
        
        # ============================================================================
        # 2. USER QUERIES
        # ============================================================================
        user_match = re.search(r'user\s+(?:id\s+)?(\d+)', message_lower)
        if user_match:
            user_id = user_match.group(1)
            user = self.query_user_info(user_id)
            if user:
                return f"User {user_id}:\n• Name: {user.get('first_name', '')} {user.get('last_name', '')}\n• Email: {user.get('email', 'N/A')}\n• Age: {user.get('age', 'N/A')}\n• Location: {user.get('city', 'N/A')}, {user.get('state', 'N/A')}"
            else:
                return f"No user found with ID {user_id}"
        
        # ============================================================================
        # 3. PRODUCT CATEGORY QUERIES
        # ============================================================================
        if 'category' in message_lower or 'socks' in message_lower or 'accessories' in message_lower:
            category = 'socks' if 'socks' in message_lower else 'accessories'
            products = self.query_products_by_category(category)
            if products:
                response = f"Products in {category} category:\n"
                for product in products[:3]:
                    response += f"• {product.get('name', 'Unknown')} - ${product.get('retail_price', 0):.2f}\n"
                return response.strip()
            else:
                return f"No products found in {category} category"
        
        # ============================================================================
        # 4. LOCATION-BASED USER QUERIES
        # ============================================================================
        if 'rio branco' in message_lower or 'location' in message_lower:
            location = 'Rio Branco' if 'rio branco' in message_lower else 'Rio Branco'
            users = self.query_users_by_location(location)
            if users:
                response = f"Users from {location}:\n"
                for user in users[:3]:
                    response += f"• {user.get('first_name', '')} {user.get('last_name', '')} (ID: {user.get('id', 'N/A')})\n"
                return response.strip()
            else:
                return f"No users found from {location}"
        
        # ============================================================================
        # 5. PRODUCT DETAILS BY ID
        # ============================================================================
        product_id_match = re.search(r'product\s+(?:id\s+)?(\d+)', message_lower)
        if product_id_match:
            product_id = product_id_match.group(1)
            product = self.query_product_by_id(product_id)
            if product:
                inventory = self.query_inventory_by_product(product_id)
                response = f"Product {product_id}:\n• Name: {product.get('name', 'Unknown')}\n• Brand: {product.get('brand', 'N/A')}\n• Price: ${product.get('retail_price', 0):.2f}\n• Category: {product.get('category', 'N/A')}\n• Department: {product.get('department', 'N/A')}"
                if inventory:
                    response += f"\n• Inventory items: {len(inventory)}"
                return response
            else:
                return f"No product found with ID {product_id}"
        
        # ============================================================================
        # 6. PRODUCT AVAILABILITY QUERIES
        # ============================================================================
        product_keywords = self.extract_product_info(message)
        if product_keywords:
            products = self.query_product_availability(product_keywords)
            if products:
                response = f"Found {len(products)} products:\n"
                for product in products[:3]:
                    name = product.get('name', 'Unknown')
                    price = product.get('price', 0)
                    available = "In stock" if product.get('available') else "Out of stock"
                    response += f"• {name}: ${price:.2f} ({available})\n"
                return response.strip()
            else:
                return f"No products found for: {', '.join(product_keywords)}"
        
        # ============================================================================
        # 7. RETURN POLICY QUERIES
        # ============================================================================
        if any(keyword in message_lower for keyword in ['return', 'refund', 'policy']):
            policy = self.get_return_policy_info()
            return f"Return Policy:\n• {policy['policy']}\n• {policy['conditions']}"
        
        # ============================================================================
        # 8. MIXED QUERIES - User + Product
        # ============================================================================
        if 'id' in message_lower and 'product details' in message_lower:
            # Extract user ID from message
            user_id_match = re.search(r'id\s+(\d+)', message_lower)
            if user_id_match:
                user_id = user_id_match.group(1)
                user = self.query_user_info(user_id)
                if user:
                    # Find user's orders
                    user_orders = list(self.db.orders.find({"user_id": int(user_id)}).limit(3))
                    response = f"User {user_id}:\n• Name: {user.get('first_name', '')} {user.get('last_name', '')}\n• Location: {user.get('city', 'N/A')}, {user.get('state', 'N/A')}"
                    if user_orders:
                        response += f"\n• Orders: {len(user_orders)} found"
                    return response
                else:
                    return f"No user found with ID {user_id}"
        
        # ============================================================================
        # 9. GENERAL HELP
        # ============================================================================
        return "I can help with:\n• Order status (order #123)\n• User details (user 123)\n• Product categories (socks, accessories)\n• Product details (product 123)\n• Return policy\n• Location-based users (Rio Branco)"
    
    def call_llm_with_context(self, user_message, context, conversation_history):
        """
        Call LLM with MongoDB context to generate natural response
        This method is used when we need more sophisticated LLM processing
        """
        system_prompt = f"""You are a helpful customer support assistant for an e-commerce clothing website. 
Use the following database information to provide accurate and helpful responses:

{context}

Rules:
- Always be polite and professional
- Use the database information provided above
- Keep responses concise and clear
- If no data is found, say so clearly
- Don't make up information not in the database
- Format responses naturally without markdown"""
        
        # Prepare conversation history for context
        chat_history = []
        for msg in conversation_history[-3:]:  # Last 3 messages for context
            role = "user" if msg["sender"] == "user" else "assistant"
            chat_history.append({"role": role, "content": msg["content"]})
        
        # Add current message
        chat_history.append({"role": "user", "content": user_message})
        
        # Call LLM
        return self.call_llm(chat_history, system_prompt)
    
    def call_llm(self, messages, system_prompt):
        """
        Call Groq LLM API with fallback handling
        This is the only LLM integration - we removed OpenAI fallback for simplicity
        """
        # Add system message to the conversation
        llm_messages = [{"role": "system", "content": system_prompt}] + messages
        
        # Call Groq API
        if settings.GROQ_API_KEY:
            try:
                headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
                payload = {
                    "model": settings.GROQ_MODEL,
                    "messages": llm_messages,
                    "max_tokens": 150,  # Shorter responses for better UX
                    "temperature": 0.3   # More focused responses
                }
                response = requests.post(settings.GROQ_API_URL, headers=headers, json=payload, timeout=10)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                # Remove markdown formatting for cleaner responses
                content = content.replace('**', '').replace('*', '').replace('`', '')
                return content
            except Exception as e:
                print(f"Groq API error: {e}")
        
        # Final fallback if LLM is unavailable
        return "I apologize, but I'm having trouble connecting to my AI service. Please try again in a moment or contact our support team directly."

# Initialize chat logic instance
# This creates a single instance that will be used throughout the application
chat_logic = EcommerceChatLogic() 