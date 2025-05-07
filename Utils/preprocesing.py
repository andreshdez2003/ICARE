from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def clean_hexadecimal(data: pd.Series) -> pd.Series:
    """Convierte valores hexadecimales con formato '0xXXX.XXX' a float."""
    try:
        # Eliminar el prefijo 0x y convertir a float
        return data.astype(str).str.replace("0x", "", regex=False).astype(float)
    except Exception as e:
        raise ValueError(f"Error cleaning hexadecimal values: {e}")

def detrend_data(data: pd.Series) -> pd.Series:
    """Elimina la tendencia lineal de una serie temporal."""
    try:
        X = np.arange(len(data)).reshape(-1, 1)
        model = LinearRegression().fit(X, data)
        trend = model.predict(X)
        return data - trend
    except Exception as e:
        raise ValueError(f"Error detrending data: {e}")

def normalize_data(data: pd.Series) -> pd.Series:
    """Estandariza los datos a media 0 y desviación estándar 1."""
    try:
        return (data - data.mean()) / data.std()
    except Exception as e:
        raise ValueError(f"Error normalizing data: {e}")
    

def process_dataframe(df: pd.DataFrame,) -> pd.DataFrame:
    """
    Procesa todas las columnas de un DataFrame que contienen la palabra 'Resistance'.

    Parámetros:
    df (pd.DataFrame): DataFrame de entrada.
    clean_hexadecimal (Callable): Función para limpiar datos hexadecimales.
    detrend_data (Callable): Función para eliminar la tendencia de los datos.
    normalize_data (Callable): Función para normalizar los datos.

    Retorna:
    pd.DataFrame: Nuevo DataFrame con las columnas 'Resistance' procesadas.
    """
    processed_df = df.copy()
    # Selecciona columnas que contienen 'Resistance' en su nombre
    resistance_columns = [col for col in df.columns if 'Resistance' in col]
    
    for column in resistance_columns:
        try:
            # Aplica cada paso de procesamiento
            processed_df[column] = clean_hexadecimal(processed_df[column])
            processed_df[column] = detrend_data(processed_df[column])
            processed_df[column] = normalize_data(processed_df[column])
        except ValueError as e:
            print(f"Advertencia: No se pudo procesar la columna '{column}'. Error: {e}")
    
    return processed_df