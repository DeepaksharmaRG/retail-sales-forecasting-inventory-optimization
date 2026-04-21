from src.data_generator import generate_sales_data
from src.data_preprocessing import load_data
from src.feature_engineering import create_features
from src.forecasting import train_model, predict, train_test_split_data, evaluate_model

def run_pipeline(num_days=365):

    # Generate
    df = generate_sales_data(num_days)

    # Preprocess
    df = load_data(df)

    # Features
    df = create_features(df)

    # Split
    train, test = train_test_split_data(df)

    # Train
    model = train_model(train)

    # Predict
    test = predict(model, test)

    # Evaluate
    mae, rmse = evaluate_model(model, test)

    return df, test, mae, rmse