import matplotlib.pyplot as plt

def plot_sales_vs_forecast(df):

    plt.figure(figsize=(12,6))

    plt.plot(df['date'], df['sales'], label='Actual')
    plt.plot(df['date'], df['forecast'], label='Forecast', linestyle='--')

    plt.legend()
    plt.title("Sales vs Forecast")

    plt.savefig("images/sales_vs_forecast.png")
    plt.close()


def plot_category_sales(df):

    grouped = df.groupby('category')['sales'].sum()

    grouped.plot(kind='bar', title="Category Sales")

    plt.savefig("images/category_sales.png")
    plt.close()