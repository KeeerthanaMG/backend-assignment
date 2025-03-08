from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from database.db import engine  # ✅ Import engine here

Base = declarative_base()

class Email(Base):
    """
    Represents an email record in the database.
    """
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    received_date = Column(DateTime, default=datetime.datetime.utcnow)
    snippet = Column(String, nullable=False)

# ✅ Ensure tables are created
Base.metadata.create_all(engine)
