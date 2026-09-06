import joblib
import pandas as pd
import numpy as np
import os


class MLScorer:
    def __init__(self):
        # Предзагрузка модели в память (Singleton-подход)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model = joblib.load(os.path.join(base_dir, 'research', 'fraud_model.pkl'))
        self.columns = joblib.load(os.path.join(base_dir, 'research', 'model_columns.pkl'))

    def predict(self, amount: float, category: str, t_time) -> float:
        # Расчет производных метрик
        hour = t_time.hour
        # Защита от выбросов через логарифмирование
        amount_log = np.log1p(max(0, amount))

        # Создаем пустой вектор с правильными колонками
        df = pd.DataFrame(columns=self.columns)
        df.loc[0] = 0.0

        df.at[0, 'hour'] = hour
        df.at[0, 'amount_log'] = amount_log

        # One-Hot Encoding для категории
        cat_col = f'merchant_category_{category}'
        if cat_col in self.columns:
            df.at[0, cat_col] = 1.0

        # Возвращаем вероятность фрода
        proba = self.model.predict_proba(df)[0][1]
        return float(proba)