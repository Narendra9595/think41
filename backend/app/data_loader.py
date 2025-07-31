import pandas as pd
from app.database import get_database
import os
import time

def load_sample_data():
    """Load sample e-commerce data into MongoDB"""
    # Retry connection to MongoDB
    max_retries = 5
    for attempt in range(max_retries):
        try:
            db = get_database()
            # Test connection
            db.command('ping')
            print("✅ Connected to MongoDB successfully!")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  MongoDB connection attempt {attempt + 1} failed: {e}")
                print("🔄 Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"❌ Failed to connect to MongoDB after {max_retries} attempts")
                print("Continuing without sample data...")
                return
    
    # Check if data already exists
    try:
        if db.products.count_documents({}) > 0:
            print("Sample data already loaded. Skipping...")
            return
    except Exception as e:
        print(f"❌ Error checking existing data: {e}")
        return
    
    datasets_path = os.path.join(os.path.dirname(__file__), "..", "datasets")
    
    try:
        # Load products
        if os.path.exists(os.path.join(datasets_path, "products.csv")):
            products_df = pd.read_csv(os.path.join(datasets_path, "products.csv"))
            products_records = products_df.to_dict(orient='records')
            db.products.insert_many(products_records)
            print(f"Loaded {len(products_records)} products")
        
        # Load users
        if os.path.exists(os.path.join(datasets_path, "users.csv")):
            users_df = pd.read_csv(os.path.join(datasets_path, "users.csv"))
            users_records = users_df.to_dict(orient='records')
            db.users.insert_many(users_records)
            print(f"Loaded {len(users_records)} users")
        
        # Load orders
        if os.path.exists(os.path.join(datasets_path, "orders.csv")):
            orders_df = pd.read_csv(os.path.join(datasets_path, "orders.csv"))
            orders_records = orders_df.to_dict(orient='records')
            db.orders.insert_many(orders_records)
            print(f"Loaded {len(orders_records)} orders")
        
        # Load order items
        if os.path.exists(os.path.join(datasets_path, "order_items.csv")):
            order_items_df = pd.read_csv(os.path.join(datasets_path, "order_items.csv"))
            order_items_records = order_items_df.to_dict(orient='records')
            db.order_items.insert_many(order_items_records)
            print(f"Loaded {len(order_items_records)} order items")
        
        # Load inventory items
        if os.path.exists(os.path.join(datasets_path, "inventory_items.csv")):
            inventory_df = pd.read_csv(os.path.join(datasets_path, "inventory_items.csv"))
            inventory_records = inventory_df.to_dict(orient='records')
            db.inventory_items.insert_many(inventory_records)
            print(f"Loaded {len(inventory_records)} inventory items")
        
        # Load distribution centers
        if os.path.exists(os.path.join(datasets_path, "distribution_centers.csv")):
            dc_df = pd.read_csv(os.path.join(datasets_path, "distribution_centers.csv"))
            dc_records = dc_df.to_dict(orient='records')
            db.distribution_centers.insert_many(dc_records)
            print(f"Loaded {len(dc_records)} distribution centers")
        
        print("✅ Sample data loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        print("Continuing without sample data...")

if __name__ == "__main__":
    load_sample_data() 