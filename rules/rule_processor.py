import json
from datetime import datetime, timedelta
from database.db import SessionLocal
from database.models import Email
from gmail.auth import authenticate_gmail
from rules.actions import apply_action
from utils.logger import setup_logger
from utils.error_handler import handle_error

logger = setup_logger()

def load_rules():
    """Loads email processing rules from rules.json."""
    try:
        with open("data/rules.json", "r") as file:
            rules = json.load(file)
            if not rules:
                logger.warning("⚠ No rules found in rules.json.")
            else:
                logger.info(f"✅ Loaded {len(rules)} rules from rules.json.")
            return rules
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(handle_error(e, "Loading rules.json"))
        return []
    
def evaluate_condition(email, condition):
    """Evaluates whether an email meets a single condition."""
    field, predicate, value = condition["field"], condition["predicate"], condition["value"]

    if field == "from":
        email_value = email.from_email.lower()
    elif field == "subject":
        email_value = email.subject.lower()
    elif field == "message":
        email_value = email.snippet.lower()
    elif field == "received_date":
        email_value = email.received_date
    else:
        return False  # Unsupported field

    if predicate == "equals":
        return email_value == value.lower()
    elif predicate == "does_not_equal":
        return email_value != value.lower()
    elif predicate == "contains":
        return value.lower() in email_value
    elif predicate == "does_not_contain":
        return value.lower() not in email_value
    elif field == "received_date":
        days_ago = datetime.utcnow() - timedelta(days=int(value))
        return (predicate == "less_than_days" and email_value > days_ago) or \
               (predicate == "greater_than_days" and email_value < days_ago)

    return False

def process_emails():
    """Processes emails based on rules."""
    rules = load_rules()
    if not rules:
        logger.info("No rules to process.")
        return

    service = authenticate_gmail()
    if not service:
        logger.error("Failed to authenticate Gmail API.")
        return

    db = SessionLocal()
    try:
        emails = db.query(Email).all()
        if not emails:
            logger.info("No emails in the database.")
            return

        for email in emails:
            for rule in rules:
                conditions_met = [evaluate_condition(email, cond) for cond in rule["conditions"]]
                rule_matches = all(conditions_met) if rule["predicate"] == "ALL" else any(conditions_met)

                if rule_matches:
                    logger.info(f"Applying rule: {rule['rule_name']} to email: {email.subject}")
                    apply_action(service, email, rule)

    except Exception as e:
        logger.error(handle_error(e, "Processing Emails"))
    finally:
        db.close()

if __name__ == "__main__":
    process_emails()
