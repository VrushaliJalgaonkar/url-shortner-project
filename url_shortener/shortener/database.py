from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import string

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/url_shortener_db"
client = MongoClient(MONGO_URI)
db = client["url_shortener_db"]
urls_collection = db["shortened_urls"]

BASE62_ALPHABET = string.ascii_letters + string.digits  # "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Function to convert an integer ID to Base62 and ensure it's 7 characters long
def encode_base62(num, length=7):
    if num == 0:
        return BASE62_ALPHABET[0] * length  # Return a string of the first character repeated 'length' times
    
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    
    # Ensure that the encoded string is exactly 'length' characters long
    short_code = ''.join(reversed(base62))
    return short_code.rjust(length, BASE62_ALPHABET[0])  # Pad with the first character if it's shorter

# Function to create a short URL entry in MongoDB
def create_short_url(long_url):
    # Check if the long_url already exists in the database
    existing_url_entry = urls_collection.find_one({"long_url": long_url})
    if existing_url_entry:
        # If it exists, return the existing entry
        return existing_url_entry
    # Get the next sequence number manually (Auto-increment-like behavior)
    last_entry = urls_collection.find_one(sort=[("_id", -1)])
    next_id = last_entry["_id"] + 1 if last_entry else 1  # Increment the last _id

    short_code = encode_base62(next_id)  # Generate a 7-character Base62 short code

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
