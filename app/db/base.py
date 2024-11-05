from pymongo import MongoClient
import os
from pymongo.errors import ConnectionFailure

# Initialize the MongoDB client and database variables
client = None
db = None

def connect_to_database():
    global client, db
    try:
        # Initialize the client using the MongoDB URI, including the database name
        client = MongoClient(os.getenv("MONGODB_URI"))
        # Get the database name directly from the URI
        db = client.get_default_database()  # Automatically gets the database from the URI
        # Check the connection by sending a ping command
        client.admin.command('ping')  # This sends a ping command to check the connection
        print("Database connected successfully.")
    except ConnectionFailure:
        print("Failed to connect to the database.")
        client = None  # Set client to None on failure
        db = None

def get_collection(collection_name: str):
    """Get a specific collection from the database."""
    return db[collection_name] if db else None

def close_connection():
    """Close the MongoDB client connection."""
    global client
    if client:
        client.close()
        print("Database connection closed.")