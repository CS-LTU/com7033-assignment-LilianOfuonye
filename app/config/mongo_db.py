import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URL from environment
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "HealthcareDB")
COLLECTION_NAME = os.getenv("PATIENT_COLLECTION", "StrokeData")

# Initialize MongoDB client
client = None
db = None

def mongo_init_db():
    """Initialize MongoDB connection"""
    global client, db
    
    try:
        if not MONGO_URL:
            raise ValueError("MONGO_URL not found in environment variables")
        
        # Create MongoDB client
        client = MongoClient(MONGO_URL)
        
        # Test the connection
        client.admin.command('ping')
        
        # Get database
        db = client[DB_NAME]
        
        print(f"Successfully connected to MongoDB: {DB_NAME}")
        return db
        
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        raise

def get_db():
    """Get database instance"""
    if db is None:
        return mongo_init_db()
    return db

def get_collection():
    """Get the patients collection"""
    database = get_db()
    return database[COLLECTION_NAME]

def close_db():
    """Close MongoDB connection"""
    global client, db
    if client:
        try:
            client.close()
            print("MongoDB connection closed")
        except Exception as e:
            print(f"Error closing MongoDB connection: {e}")
        finally:
            client = None
            db = None
