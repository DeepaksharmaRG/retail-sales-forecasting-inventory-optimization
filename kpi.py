def calculate_kpis(df):

    total_revenue = df['sales'].sum()
    units_sold = df['sales'].count()
    avg_sales = df['sales'].mean()

    return {
        "revenue": total_revenue,
        "units": units_sold,
        "avg": avg_sales
    }