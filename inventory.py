def calculate_inventory(df):

    df['safety_stock'] = df['forecast'] * 0.2
    df['reorder_point'] = df['forecast'] + df['safety_stock']

    df['status'] = df.apply(
        lambda x: "Critical Low" if x['sales'] < x['reorder_point'] else "OK",
        axis=1
    )

    return df