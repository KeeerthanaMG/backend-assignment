from database.db import SessionLocal
from sqlalchemy.sql import text  # ✅ Import `text()`

def test_database_connection():
    """
    Test if the database connection works correctly.
    """
    try:
        db = SessionLocal()  # Open a database session
        db.execute(text("SELECT 1"))  # ✅ Use `text()`
        assert True  # If no error, test passes
    except Exception as e:
        assert False, f"Database connection failed: {str(e)}"
    finally:
        db.close()
