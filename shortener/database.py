from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import string
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Atlas connection
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")

# Encode special characters in password (if needed)
MONGO_PASS_ENCODED = MONGO_PASS.replace("@", "%40").replace("#", "%23")

# Update your connection string
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS_ENCODED}@cluster0.i4mx3ca.mongodb.net/url_shortener_db?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["url_shortener_db"]
urls_collection = db["shortened_urls"]

BASE62_ALPHABET = string.ascii_letters + string.digits  # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Function to convert an integer ID to Base62 and ensure it's 7 characters long
def encode_base62(num, length=7):
    if num == 0:
        return BASE62_ALPHABET[0] * length
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    return ''.join(reversed(base62)).rjust(length, BASE62_ALPHABET[0])

# Function to create a short URL entry in MongoDB
def create_short_url(long_url):
    existing_url_entry = urls_collection.find_one({"long_url": long_url})
    if existing_url_entry:
        return existing_url_entry
    last_entry = urls_collection.find_one(sort=[("_id", -1)])
    next_id = last_entry["_id"] + 1 if last_entry else 1
    short_code = encode_base62(next_id)
    url_entry = {
        "_id": next_id,
        "short_code": short_code,
        "long_url": long_url,
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "clicks": 0
    }
    urls_collection.insert_one(url_entry)
    return url_entry