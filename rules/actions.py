from googleapiclient.errors import HttpError
import time
from utils.logger import setup_logger
from utils.error_handler import handle_error

logger = setup_logger()

def apply_action(service, email, rule):
    """
    Applies an action to an email based on a matched rule.
    """
    try:
        email_id = email.id
        actions = rule["actions"]

        for action in actions:
            if action == "mark_as_read":
                mark_email_as_read(service, email_id)
            elif action == "mark_as_unread":
                mark_email_as_unread(service, email_id)
            elif action == "move_to_folder":
                folder = rule.get("folder", "Default")
                move_email_to_folder(service, email_id, folder)
            else:
                logger.warning(f"⚠ Unknown action '{action}' for rule '{rule['rule_name']}'")

    except HttpError as e:
        logger.error(handle_error(e, f"Applying action: {rule['rule_name']}"))
    except Exception as e:
        logger.error(handle_error(e, "Executing Email Action"))

def gmail_api_retry(func, *args, **kwargs):
    """
    Retries Gmail API requests in case of rate limits or transient failures.
    Implements exponential backoff.
    """
    max_retries = 5
    delay = 2  # Start with 2 seconds

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            if e.resp.status in [403, 429, 500, 503]:
                logger.warning(f"⚠ Rate limit or temporary error. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise  # Re-raise other errors

def mark_email_as_read(service, email_id):
    """Marks an email as read in Gmail."""
    try:
        gmail_api_retry(
            service.users().messages().modify,
            userId="me",
            id=email_id,
            body={"removeLabelIds": ["UNREAD"]}
        )
        logger.info(f"Marked email {email_id} as read in Gmail.")
    except HttpError as e:
        logger.error(handle_error(e, "Mark as Read Error"))

def mark_email_as_unread(service, email_id):
    """Marks an email as unread in Gmail."""
    try:
        gmail_api_retry(
            service.users().messages().modify,
            userId="me",
            id=email_id,
            body={"addLabelIds": ["UNREAD"]}
        )
        logger.info(f"Marked email {email_id} as unread in Gmail.")
    except HttpError as e:
        logger.error(handle_error(e, "Mark as Unread Error"))

def move_email_to_folder(service, email_id, folder):
    """Moves an email to a specified folder in Gmail using labels."""
    try:
        labels = service.users().labels().list(userId="me").execute().get("labels", [])
        folder_id = next((label["id"] for label in labels if label["name"].lower() == folder.lower()), None)

        if not folder_id:
            logger.warning(f"⚠ Folder '{folder}' not found. Creating new label in Gmail...")
            folder_id = create_gmail_label(service, folder)

        gmail_api_retry(
            service.users().messages().modify,
            userId="me",
            id=email_id,
            body={"addLabelIds": [folder_id]}
        )
        logger.info(f"Moved email {email_id} to folder '{folder}' in Gmail.")
    except HttpError as e:
        logger.error(handle_error(e, "Move to Folder Error"))

def create_gmail_label(service, label_name):
    """Creates a new label in Gmail if it does not exist."""
    try:
        new_label = {
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
        label = gmail_api_retry(
            service.users().labels().create,
            userId="me",
            body=new_label
        )
        logger.info(f"Created new label '{label_name}' in Gmail.")
        return label["id"]
    except HttpError as e:
        logger.error(handle_error(e, f"Error creating label '{label_name}'"))
        return None
