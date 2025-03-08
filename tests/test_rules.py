from rules.rule_processor import load_rules, process_emails

def test_load_rules():
    """
    Test if rules are loaded correctly.
    """
    rules = load_rules()
    assert len(rules) > 0, "Rules not loaded from rules.json"

def test_process_emails():
    """
    Test if emails are processed without errors.
    """
    try:
        process_emails()
        assert True
    except Exception as e:
        assert False, f"Processing emails failed: {str(e)}"
