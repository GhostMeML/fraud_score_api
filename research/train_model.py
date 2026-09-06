import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    # Защита от изменения исходного датафрейма
    df_processed = df.copy()

    # Извлечение времени
    df_processed['transaction_time'] = pd.to_datetime(df_processed['transaction_time'])
    df_processed['hour'] = df_processed['transaction_time'].dt.hour

    # Математическое преобразование суммы (защита от логарифма нуля/отрицательных значений)
    df_processed['amount_log'] = np.log1p(df_processed['amount'].clip(lower=0))

    # One-Hot Encoding категорий
    df_processed = pd.get_dummies(df_processed, columns=['merchant_category'], drop_first=True)

    # Удаление неинформативных для модели признаков
    df_processed.drop(columns=['user_id', 'transaction_time', 'amount'], inplace=True)

    return df_processed


def train():
    print("Загрузка данных...")
    df = pd.read_csv('transactions.csv')

    print("Генерация признаков...")
    df_processed = feature_engineering(df)

    X = df_processed.drop('is_fraud', axis=1)
    y = df_processed['is_fraud']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Обучение модели...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)

    print("Оценка качества:")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Сериализация модели
    joblib.dump(model, 'fraud_model.pkl')
    # Сериализация порядка колонок (важно для продакшена)
    joblib.dump(list(X.columns), 'model_columns.pkl')
    print("Модель и структура признаков сохранены.")


if __name__ == '__main__':
    train()