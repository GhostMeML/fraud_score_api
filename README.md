# FraudScore API 

Асинхронный ML-микросервис для потокового антифрод-скоринга банковских транзакций в реальном времени.

Проект объединяет в себе разработку классического машинного обучения (предиктивная аналитика) и создание надежного бэкенда с использованием современных подходов к типизации, валидации данных и архитектуре.

## Стек технологий
* **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic
* **ML & Data:** scikit-learn, Pandas, NumPy, joblib
* **База данных:** SQLite + SQLAlchemy (ORM)
* **Инфраструктура:** Docker

##  Ключевые архитектурные решения
1. **Предзагрузка ML-модели:** Веса модели (`.pkl`) загружаются в оперативную память при старте сервера (Singleton), что минимизирует latency при инференсе.
2. **Строгая валидация:** Использование Pydantic и Enum для нормализации входящих данных (защита от неверных типов, отрицательных сумм и некорректного регистра).
3. **Audit Trail (Аудит-след):** Все транзакции и вердикты модели атомарно сохраняются в реляционную базу данных через SQLAlchemy с механизмом rollback при сбоях.

## Установка и запуск

### Вариант 1: Через Docker (Рекомендуемый)
```bash
git clone <ссылка_на_ваш_репозиторий>
cd fraud_score_api
docker build -t fraud_score_api .
docker run -d -p 8000:8000 fraud_score_api
```

### Вариант 2: Локальный запуск
```bash
python -m venv venv
# Активация окружения (Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
После запуска перейдите по адресу: http://127.0.0.1:8000/docs


<img width="1227" height="859" alt="Fraud" src="https://github.com/user-attachments/assets/7872be04-c0b5-4ced-858d-acd1cbbb2de7" />

<img width="1280" height="253" alt="fraud2" src="https://github.com/user-attachments/assets/f8099f4b-6d55-4d32-ab00-9393f4a63548" />

