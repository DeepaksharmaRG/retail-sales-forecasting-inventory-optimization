def create_features(df):
    """
    Create time-based and lag features for forecasting
    """

    df = df.copy()

    # Time features
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.weekday

    # Lag features (grouped for realism)
    df['lag_1'] = df.groupby(['category', 'store'])['sales'].shift(1)
    df['lag_7'] = df.groupby(['category', 'store'])['sales'].shift(7)

    # Fill missing values
    df.fillna(0, inplace=True)

    return df