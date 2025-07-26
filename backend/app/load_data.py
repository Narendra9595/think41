import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client['ecommerce_bot']

def load_csv_to_mongo(csv_file_path, collection_name):
    data = pd.read_csv(csv_file_path)
    records = data.to_dict(orient='records')
    db[collection_name].delete_many({})  # Clear existing data
    db[collection_name].insert_many(records)
    print(f"Inserted {len(records)} records into the '{collection_name}' collection.")


load_csv_to_mongo("../datasets/users.csv", "users")
load_csv_to_mongo("../datasets/products.csv", "products")
load_csv_to_mongo("../datasets/orders.csv", "orders")
load_csv_to_mongo("../datasets/order_items.csv", "order_items")
load_csv_to_mongo("../datasets/inventory_items.csv", "inventory_items")
load_csv_to_mongo("../datasets/distribution_centers.csv", "distribution_centers")