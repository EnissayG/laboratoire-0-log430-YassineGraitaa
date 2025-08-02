from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from app.db.database import Base


class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    aggregate_id = Column(String, index=True)
    data = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
