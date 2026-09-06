from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base


class TransactionRecord(Base):
    __tablename__ = "scoring_history"

    id = Column(Integer, primary_key=True, index=True)
    # Входные данные
    amount = Column(Float, nullable=False)
    merchant_category = Column(String, nullable=False)
    transaction_time = Column(DateTime, nullable=False)

    # Результаты ML-скоринга
    score = Column(Float, nullable=False)
    verdict = Column(String, nullable=False)

    # Системное время записи
    created_at = Column(DateTime, default=datetime.utcnow)