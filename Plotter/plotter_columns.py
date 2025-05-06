import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
from Utils import plot_menu  # Tu diccionario de señales


def plot_column(df):
    keyword = plot_menu()
    if keyword is None:
        return

    # Buscar la primera columna cuyo nombre contenga la palabra clave
    column_matches = [col for col in df.columns if keyword.lower() in col.lower()]
    if not column_matches:
        print(f"❌ No column containing '{keyword}' found.")
        return

    column_name = column_matches[0]

    # Preguntar al usuario por el rango de fechas
    try:
        start_input = input("Enter the start date (YYYY-MM-DD HH:MM:SS): ")
        end_input = input("Enter the end date (YYYY-MM-DD HH:MM:SS): ")
        start_date = pd.to_datetime(start_input)
        end_date = pd.to_datetime(end_input)
    except Exception as e:
        print(f"❌ Invalid date format. Error: {e}")
        return

    # Filtrar el dataframe por rango
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
        print("❌ No data found in the specified date range.")
        return

    # Plotear
    fig, ax = plt.subplots(figsize=(16, 6), dpi=100)
    ax.plot(filtered_df['Date'], filtered_df[column_name], label=column_name, color='blue')

    ax.xaxis.set_major_formatter(DateFormatter("%m-%d %H:%M"))
    plt.xticks(rotation=45)

    ax.set_title(f"{column_name} from {start_date} to {end_date}")
    ax.set_xlabel("Date")
    ax.set_ylabel(column_name)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()