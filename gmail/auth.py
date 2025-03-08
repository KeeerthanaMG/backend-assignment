import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config.config import GMAIL_CREDENTIALS_PATH, TOKEN_PATH
from utils.logger import setup_logger
from utils.error_handler import handle_error

# Set up logging
logger = setup_logger()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """
    Authenticates with Gmail API using OAuth 2.0.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service instance.
    """
    try:
        logger.info("Starting Gmail authentication...")
        creds = None

        # Check if token.json exists for saved credentials
        if os.path.exists(TOKEN_PATH):
            logger.info("Loading existing token.json...")
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        # If credentials are not valid, request new authentication
        if not creds or not creds.valid:
            if not os.path.exists(GMAIL_CREDENTIALS_PATH):
                raise FileNotFoundError(f"Gmail API credentials not found at {GMAIL_CREDENTIALS_PATH}")

            logger.info("No valid credentials found. Starting OAuth authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)  # Opens a browser for authentication

            # Save the new token for future use
            with open(TOKEN_PATH, "w") as token_file:
                token_file.write(creds.to_json())
                logger.info(f"New access token saved to {TOKEN_PATH}")

        logger.info("✅ Gmail authentication successful.")
        return build("gmail", "v1", credentials=creds)

    except Exception as e:
        logger.error(f"❌ Gmail Authentication Failed: {str(e)}")
        print(handle_error(e, "Gmail Authentication"))
        return None

# Run authentication manually if this script is executed directly
if __name__ == "__main__":
    service = authenticate_gmail()
    if service:
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed!")
