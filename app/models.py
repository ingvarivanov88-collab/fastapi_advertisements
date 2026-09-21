from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from datetime import datetime
from .database import Base


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    author_id = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)