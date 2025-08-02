from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.database import Base


class EtatSaga(Base):
    __tablename__ = "etat_saga"

    id = Column(Integer, primary_key=True, index=True)
    saga_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    etat = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
