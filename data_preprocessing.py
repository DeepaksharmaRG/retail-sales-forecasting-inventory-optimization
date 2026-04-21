import pandas as pd

def load_data(df):
    df = df.copy()

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    df.ffill(inplace=True)

    return df