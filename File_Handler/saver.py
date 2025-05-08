from pathlib import Path
import pandas as pd

def save_dataframe_to_csv(df, filename, output_dir): 
    """
    Guarda un DataFrame en un archivo CSV.

    Parámetros:
    - df: DataFrame a guardar.
    - filename: Nombre del archivo (ej. 'output.csv').
    - output_dir: Directorio de salida (objeto Path).
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)  # Crea el directorio si no existe
        file_path = output_dir / filename
        df.to_csv(file_path, index=False)
        print(f"✅ DataFrame guardado en '{file_path}'")
    except Exception as e:
        print(f"❌ Error al guardar CSV: {e}")

def save_dataframe_to_excel(df, filename, output_dir): 
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        df.to_excel(file_path, index=False)
        print(f"✅ DataFrame guardado en '{file_path}'")
    except Exception as e:
        print(f"❌ Error al guardar Excel: {e}")

