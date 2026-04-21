import os
from src.pipeline import run_pipeline
from src.visualization import plot_sales_vs_forecast, plot_category_sales

os.makedirs("outputs", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("models", exist_ok=True)

df, test, mae, rmse = run_pipeline()

# Save outputs
test.to_csv("outputs/forecast.csv", index=False)

# Graphs
plot_sales_vs_forecast(test)
plot_category_sales(df)

print("✅ Pipeline completed")
print(f"MAE: {mae}")
print(f"RMSE: {rmse}")