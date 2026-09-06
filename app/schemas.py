from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# Создаем жесткий список доступных категорий
class MerchantCategory(str, Enum):
    SUPERMARKET = "Supermarket"
    ELECTRONICS = "Electronics"
    ONLINE_SERVICES = "OnlineServices"
    TRANSFER = "Transfer"
    RESTAURANT = "Restaurant"

class TransactionRequest(BaseModel):
    amount: float = Field(
        ...,
        gt=0,
        description="Сумма перевода в рублях. Ожидается значение больше 0.",
        json_schema_extra={"example": 1500.50}
    )
    merchant_category: MerchantCategory = Field(
        ...,
        description="Категория продавца. Выберите значение из выпадающего списка."
    )
    transaction_time: datetime = Field(
        ...,
        description="Локальное время транзакции (гггг-мм-ддTчч:мм:сс).",
        json_schema_extra={"example": "2026-09-06T14:30:00"}
    )

class TransactionResponse(BaseModel):
    score: float = Field(
        ...,
        description="Вероятность мошенничества от 0.0 (безопасно) до 1.0 (100% фрод)."
    )
    verdict: str = Field(
        ...,
        description="Вердикт системы: APPROVE (одобрено), REVIEW (ручная проверка) или DECLINE (отклонено)."
    )