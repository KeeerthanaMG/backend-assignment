from googleapiclient.errors import HttpError
from utils.logger import setup_logger
from utils.error_handler import handle_error

logger = setup_logger()

def apply_action(service, email, rule):
    """
    Applies an action to an email based on a matched rule.

    Args:
        service: Gmail API service instance.
        email (Email): The email object from the database.
        rule (dict): The matched rule.
    """
    try:
        action = rule["action"]
        email_id = email.id  

        if action == "mark_as_read":
            mark_email_as_read(service, email_id, email.subject)

        elif action == "move_to_folder":
            folder = rule.get("folder", "Default")
            move_email_to_folder(service, email_id, email.subject, folder)

        elif action == "flag_important":
            flag_email_as_important(service, email_id, email.subject)

        elif action == "delete_email":
            delete_email(service, email_id, email.subject)

        elif action == "forward_email":
            forward_to = rule.get("forward_to", "")
            forward_email(service, email_id, email.subject, forward_to)

        else:
            logger.warning(f"Unknown action '{action}' for rule '{rule['rule_name']}'. Skipping.")

    except HttpError as e:
        logger.error(handle_error(e, f"Applying action: {rule['action']}"))
    except Exception as e:
        logger.error(handle_error(e, "Executing Email Action"))

def mark_email_as_read(service, email_id, subject):
    """Marks an email as read."""
    service.users().messages().modify(userId="me", id=email_id, body={"removeLabelIds": ["UNREAD"]}).execute()
    logger.info(f"Marked email '{subject}' as read.")

def move_email_to_folder(service, email_id, subject, folder):
    """Moves an email to a specified folder."""
    logger.info(f"Simulating moving email '{subject}' to folder '{folder}'. (Folder movement via API requires label setup).")

def flag_email_as_important(service, email_id, subject):
    """Flags an email as important."""
    service.users().messages().modify(userId="me", id=email_id, body={"addLabelIds": ["IMPORTANT"]}).execute()
    logger.info(f"Flagged email '{subject}' as important.")

def delete_email(service, email_id, subject):
    """Deletes an email."""
    service.users().messages().delete(userId="me", id=email_id).execute()
    logger.info(f"Deleted email '{subject}'.")

def forward_email(service, email_id, subject, forward_to):
    """Simulates forwarding an email to another address."""
    logger.info(f"Simulating forwarding email '{subject}' to '{forward_to}'. (Forwarding via API requires SMTP setup).")
