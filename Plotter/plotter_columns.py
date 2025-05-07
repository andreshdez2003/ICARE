import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
from Utils import plot_menu

def select_column(df, keyword):
    """Selecciona la columna basada en una palabra clave"""
    column_matches = [col for col in df.columns if keyword.lower() in col.lower()]
    return column_matches[0] if column_matches else None

def get_date_range():
    """Obtiene y valida el rango de fechas del usuario"""
    try:
        start_input = input("Enter the start date (YYYY-MM-DD HH:MM:SS): ")
        end_input = input("Enter the end date (YYYY-MM-DD HH:MM:SS): ")
        return pd.to_datetime(start_input), pd.to_datetime(end_input)
    except Exception as e:
        print(f"❌ Invalid date format. Error: {e}")
        return None, None

def filter_by_date(df, start_date, end_date):
    """Filtra el dataframe por el rango de fechas especificado"""
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask]

def setup_plot_style(ax, column_name, start_date, end_date):
    """Configura el estilo y formato del gráfico"""
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d %H:%M"))
    plt.xticks(rotation=45)
    ax.set_title(f"{column_name} from {start_date} to {end_date}")
    ax.set_xlabel("Date")
    ax.set_ylabel(column_name)
    ax.legend()
    ax.grid(True)

def plot_data(filtered_df, column_name, start_date, end_date):
    """Genera y muestra el gráfico"""
    fig, ax = plt.subplots(figsize=(16, 6), dpi=100)
    ax.plot(filtered_df['Date'], filtered_df[column_name], label=column_name, color='blue')
    setup_plot_style(ax, column_name, start_date, end_date)
    plt.tight_layout()
    plt.show()

def plot_column(df):
    """Función principal que coordina el flujo de trabajo completo"""
    # Paso 1: Selección de columna
    keyword = plot_menu()
    if not keyword:
        return
    
    # Paso 2: Búsqueda de columna
    column_name = select_column(df, keyword)
    if not column_name:
        print(f"❌ No column containing '{keyword}' found.")
        return
    
    # Paso 3: Obtención de fechas
    start_date, end_date = get_date_range()
    if None in [start_date, end_date]:
        return
    
    # Paso 4: Filtrado de datos
    filtered_df = filter_by_date(df, start_date, end_date)
    if filtered_df.empty:
        print("❌ No data found in the specified date range.")
        return
    
    # Paso 5: Visualización
    plot_data(filtered_df, column_name, start_date, end_date)