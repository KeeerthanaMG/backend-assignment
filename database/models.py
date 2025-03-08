from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from database.db import engine  # ✅ Import engine

Base = declarative_base()

class Email(Base):
    """
    Represents an email record in the database.
    """
    __tablename__ = "emails"

    id = Column(String, primary_key=True)  # ✅ Use id as message_id
    from_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    received_date = Column(DateTime, default=datetime.datetime.utcnow)
    snippet = Column(String, nullable=False)
# ✅ Ensure tables are created
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully.")
