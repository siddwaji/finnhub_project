import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

if not FINNHUB_API_KEY:
    raise ValueError("Please set FINNHUB_API_KEY in .env file")

print("API Key loaded successfully")