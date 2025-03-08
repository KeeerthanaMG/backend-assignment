from gmail.fetch_emails import fetch_and_store_emails

def test_email_fetching():
    """
    Test fetching emails from Gmail.
    """
    try:
        fetch_and_store_emails()
        assert True  # If no error, test passes
    except Exception as e:
        assert False, f"Email fetching failed: {str(e)}"
