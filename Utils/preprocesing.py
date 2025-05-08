from scipy.signal import savgol_filter
import pandas as pd
import numpy as np

def convert_columns_to_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Convierte columnas específicas a valores numéricos (reemplaza comas por puntos).
    """
    df = df.copy()
    for col in columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    return df

def apply_savgol_filter(df: pd.DataFrame, columns: list, window_length: int, polyorder: int) -> pd.DataFrame:
    """
    Aplica el filtro Savitzky-Golay a columnas específicas.
    """
    df = df.copy()
    for col in columns:
        try:
            df[col] = savgol_filter(df[col].values, window_length=window_length, polyorder=polyorder, mode='nearest')
        except Exception as e:
            print(f"Error aplicando Savitzky-Golay en columna {col}: {str(e)}")
    return df

def normalize_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normaliza columnas específicas (mínimo 0, máximo 1).
    """
    df = df.copy()
    for col in columns:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max != col_min:
            df[col] = (df[col] - col_min) / (col_max - col_min)
        else:
            df[col] = 0  # Evitar división por cero si todos los valores son iguales
    return df

def process_dataframe(df: pd.DataFrame, window_length: int = 15, polyorder: int = 2) -> pd.DataFrame:
    """
    Procesa un DataFrame aplicando:
    1. Conversión a numérico.
    2. Filtro Savitzky-Golay.
    3. Normalización de columnas.

    Parámetros:
    df (pd.DataFrame): DataFrame con columnas que incluyen 'Resistance' y '(y)'.
    window_length (int): Longitud de la ventana del filtro.
    polyorder (int): Orden del polinomio.

    Retorna:
    pd.DataFrame: DataFrame procesado.
    """
    processed_df = df.copy()
    resistance_columns = [col for col in df.columns if '(y)' in col]

    processed_df = convert_columns_to_numeric(processed_df, resistance_columns)
    processed_df = apply_savgol_filter(processed_df, resistance_columns, window_length, polyorder)
    processed_df = normalize_columns(processed_df, resistance_columns)

    return processed_df