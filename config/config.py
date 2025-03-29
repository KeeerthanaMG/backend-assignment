import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Gmail API Configuration
GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH")
TOKEN_PATH = os.getenv("TOKEN_PATH")

# Ensure variables are loaded correctly
if not DATABASE_URL or not GMAIL_CREDENTIALS_PATH or not TOKEN_PATH:
    raise ValueError(" Missing environment variables. Check your .env file.")
