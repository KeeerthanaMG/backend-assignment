import logging
import os

LOG_FILE = "logs/app.log"

def setup_logger():
    """
    Sets up logging to write logs to logs/app.log with proper formatting.
    """
    # Ensure the logs/ directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()
