from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Test if your deployment is successful


# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)



# Set up MongoDB URI
uri = MONGO_URI + "?retryWrites=true&w=majority&appName=Booking-Platform"

# Create a new client with SSL/TLS configurations
client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection error:", e)
