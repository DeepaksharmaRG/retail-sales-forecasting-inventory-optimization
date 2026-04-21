import pandas as pd
import numpy as np

def generate_sales_data(num_days=365):

    np.random.seed(42)

    dates = pd.date_range(start="2023-01-01", periods=num_days)

    categories = ["Electronics", "Clothing", "Beauty"]
    regions = ["East", "West", "North", "South"]
    stores = ["S001", "S002"]

    data = []

    for date in dates:
        for cat in categories:
            for store in stores:
                region = np.random.choice(regions)

                base = 100

                if cat == "Electronics":
                    base += 50
                elif cat == "Clothing":
                    base += 30

                if date.weekday() >= 5:
                    base += 40

                sales = base + np.random.normal(0, 10)

                data.append([
                    date, cat, store, region, int(max(0, sales))
                ])

    df = pd.DataFrame(data, columns=[
        "date", "category", "store", "region", "sales"
    ])

    return df