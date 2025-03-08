import logging
from utils.logger import setup_logger

logger = setup_logger()

def handle_error(exception, context=""):
    """
    Logs and formats error messages.

    Args:
        exception (Exception): The error that occurred.
        context (str): Description of where the error happened.

    Returns:
        str: A formatted error message.
    """
    error_message = f"❌ Error in {context}: {str(exception)}"
    logger.error(error_message)
    return error_message
