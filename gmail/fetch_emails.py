from googleapiclient.errors import HttpError
from gmail.auth import authenticate_gmail
from database.db import SessionLocal
from database.models import Email
from utils.logger import setup_logger
from utils.error_handler import handle_error

# Initialize logger
logger = setup_logger()

def fetch_and_store_emails():
    """
    Fetches emails from Gmail and stores them in PostgreSQL.
    """
    try:
        logger.info("📩 Starting email fetching process...")
        service = authenticate_gmail()
        if service is None:
            logger.error("❌ Authentication failed. Cannot fetch emails.")
            print("❌ Authentication failed. Cannot fetch emails.")
            return

        # Fetch the latest 10 emails
        results = service.users().messages().list(userId="me", maxResults=10).execute()
        messages = results.get("messages", [])

        if not messages:
            logger.info("📭 No new emails found.")
            print("📭 No new emails found.")
            return

        db = SessionLocal()  # Open a database session

        try:
            emails_added = 0
            for msg in messages:
                msg_id = msg["id"]  # ✅ Get Gmail's unique message ID
                msg_details = service.users().messages().get(userId="me", id=msg_id).execute()

                # Extract email details
                headers = msg_details["payload"]["headers"]
                from_email = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
                subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
                snippet = msg_details.get("snippet", "")

                # ✅ Check if email already exists in the database using message_id
                existing_email = db.query(Email).filter(Email.message_id == msg_id).first()
                if existing_email:
                    logger.info(f"⚠ Skipping duplicate email ID: {msg_id} from {from_email} with subject '{subject}'")
                    print(f"⚠ Email ID: {msg_id} from {from_email} already exists. Skipping...")
                    continue

                # ✅ Store email in the database with message_id
                email = Email(
                    id=msg_id,  # ✅ Store Gmail's actual message ID
                    from_email=from_email,
                    subject=subject,
                    snippet=snippet
                )
                db.add(email)
                emails_added += 1

            db.commit()  # Save all new emails to the database
            logger.info(f"✅ {emails_added} emails stored successfully.")
            print(f"✅ {emails_added} emails stored successfully.")

        finally:
            db.close()  # Ensure session is closed properly

    except HttpError as e:
        logger.error(f"❌ Gmail API Error: {str(e)}")
        print(handle_error(e, "Fetching Emails"))
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        print(handle_error(e, "Fetching Emails"))

if __name__ == "__main__":
    fetch_and_store_emails()
