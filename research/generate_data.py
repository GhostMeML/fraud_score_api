import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Фиксация seed для строгого воспроизведения результатов
np.random.seed(42)
random.seed(42)


def generate_transactions(n_samples: int = 10000) -> pd.DataFrame:
    data = []
    start_date = datetime(2023, 1, 1)

    for _ in range(n_samples):
        user_id = random.randint(1000, 5000)
        # Базовая сумма от 100 до 50 000 руб
        amount = round(np.random.lognormal(mean=7.0, sigma=1.5), 2)

        # Случайное время в течение 30 дней
        time_offset = timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1440))
        transaction_time = start_date + time_offset

        merchant_category = random.choice(['Supermarket', 'Electronics', 'OnlineServices', 'Transfer', 'Restaurant'])

        # Логика фрода: крупные переводы, ночное время (с 0 до 5 утра)
        is_fraud = 0
        hour = transaction_time.hour

        if (amount > 150000) or (hour < 5 and amount > 30000 and merchant_category in ['Transfer', 'OnlineServices']):
            # Вероятность фрода в таких условиях 80%
            is_fraud = np.random.choice([0, 1], p=[0.2, 0.8])
        else:
            # Случайный шум
            is_fraud = np.random.choice([0, 1], p=[0.99, 0.01])

        data.append([user_id, amount, transaction_time, merchant_category, is_fraud])

    df = pd.DataFrame(data, columns=['user_id', 'amount', 'transaction_time', 'merchant_category', 'is_fraud'])
    return df


if __name__ == '__main__':
    df = generate_transactions(15000)
    df.to_csv('transactions.csv', index=False)
    print("Данные успешно сгенерированы: transactions.csv")