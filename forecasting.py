from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

# -------------------------------
# TRAIN TEST SPLIT
# -------------------------------
def train_test_split_data(df):

    split = int(len(df) * 0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    return train, test


# -------------------------------
# TRAIN MODEL
# -------------------------------
def train_model(df):

    features = ['day', 'month', 'weekday', 'lag_1', 'lag_7']

    X = df[features]
    y = df['sales']

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    # Save model
    joblib.dump(model, "models/model.pkl")

    return model


# -------------------------------
# EVALUATE MODEL (🔥 THIS WAS MISSING)
# -------------------------------
def evaluate_model(model, df):

    features = ['day', 'month', 'weekday', 'lag_1', 'lag_7']

    X = df[features]
    y = df['sales']

    preds = model.predict(X)

    mae = mean_absolute_error(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))

    return mae, rmse


# -------------------------------
# PREDICT
# -------------------------------
def predict(model, df):

    features = ['day', 'month', 'weekday', 'lag_1', 'lag_7']

    df = df.copy()
    df['forecast'] = model.predict(df[features])

    return df