import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
from Utils import clean_hexadecimal, detrend_data, normalize_data

def plot_processed(df):
    # Selección de columna
    column = input("Enter the column name to process: ").strip()
    if column not in df.columns:
        print(f"❌ Column '{column}' not found in dataframe")
        return

    # Procesamiento de datos
    try:
        # Convertir hexadecimal si es necesario
        processed_df = df.copy()
        processed_df[column] = clean_hexadecimal(processed_df[column])
        
        # Aplicar transformaciones
        processed_df['Detrended'] = detrend_data(processed_df[column])
        processed_df['Normalized'] = normalize_data(processed_df[column])
        
    except Exception as e:
        print(f"❌ Processing error: {e}")
        return

    # Configuración del gráfico
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    
    # Gráfico original
    ax1.plot(processed_df['Date'], processed_df[column], color='blue')
    ax1.set_title(f"Original {column} Data")
    ax1.grid(True)
    
    # Gráfico sin tendencia
    ax2.plot(processed_df['Date'], processed_df['Detrended'], color='red')
    ax2.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax2.set_title("Detrended Data")
    ax2.grid(True)
    
    # Gráfico normalizado
    ax3.plot(processed_df['Date'], processed_df['Normalized'], color='green')
    ax3.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax3.set_title("Normalized Data (Z-score)")
    ax3.grid(True)
    
    # Formateo común
    date_format = DateFormatter("%m-%d %H:%M")
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(date_format)
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()