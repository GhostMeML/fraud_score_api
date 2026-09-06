from fastapi import FastAPI, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import TransactionResponse, MerchantCategory
from app.ml_service import MLScorer
from app.database import engine, Base, get_db
from app.models import TransactionRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FraudScore API")
scorer = MLScorer()


@app.post(
    "/api/v1/score_transaction",
    response_model=TransactionResponse,
    summary="Оценка транзакции на мошенничество",
    description="""
    Добро пожаловать в систему антифрод-скоринга FraudScore API!

    ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ:
    1. Нажмите кнопку "Try it out" в правой части панели, чтобы поля ввода стали активными.
    2. Заполните параметры транзакции или оставьте тестовые значения по умолчанию.
    3. Нажмите кнопку "Execute", чтобы запустить ML-модель и получить результат.

    СЦЕНАРИИ ДЛЯПРОВЕРКИ:
    - Легальная транзакция: Сумма 1500, категория Supermarket, дневное время. Ожидаемый вердикт: APPROVE.
    - Подозрительная транзакция: Сумма 350000, категория Transfer, ночное время. Ожидаемый вердикт: DECLINE.
    """
)
async def score_transaction(
        # Используем alias и description, чтобы скрыть технические имена и оставить только чистый текст
        amount: float = Form(
            1500.5,
            gt=0,
            alias="Сумма перевода (в рублях)",
            description="Введите размер денежной операции"
        ),
        merchant_category: MerchantCategory = Form(
            MerchantCategory.SUPERMARKET,
            alias="Категория торговой точки",
            description="Выберите тип бизнеса из выпадающего списка"
        ),
        transaction_time: datetime = Form(
            "2026-09-06T14:30:00",
            alias="Дата и время транзакции",
            description="Укажите момент совершения операции"
        ),
        db: Session = Depends(get_db)
):
    try:
        # 1. Инференс ML-модели
        score = scorer.predict(
            amount=amount,
            category=merchant_category.value,
            t_time=transaction_time
        )

        # 2. Бизнес-логика принятия решений
        if score > 0.8:
            verdict = "DECLINE"
        elif score > 0.5:
            verdict = "REVIEW"
        else:
            verdict = "APPROVE"

        # 3. Атомарное сохранение в БД
        db_record = TransactionRecord(
            amount=amount,
            merchant_category=merchant_category.value,
            transaction_time=transaction_time,
            score=score,
            verdict=verdict
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return TransactionResponse(score=score, verdict=verdict)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal processing error")