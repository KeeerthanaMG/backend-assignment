from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

def get_db():
    """
    Provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
