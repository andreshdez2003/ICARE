from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def detrend_data(data: pd.Series) -> pd.Series:
    """Elimina la tendencia lineal de una serie temporal."""
    try:
        X = np.arange(len(data)).reshape(-1, 1)
        model = LinearRegression().fit(X, data)
        return data - model.predict(X)
    except Exception as e:
        raise ValueError(f"Error detrending data: {e}")

def normalize_data(data: pd.Series) -> pd.Series:
    """Estandariza los datos a media 0 y desviación estándar 1."""
    try:
        return (data - data.mean()) / data.std()
    except Exception as e:
        raise ValueError(f"Error normalizing data: {e}")

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa columnas de resistencia aplicando detrending y normalización.

    Parámetros:
    df (pd.DataFrame): DataFrame con columnas que incluyen 'Resistance' y '(y)'.

    Retorna:
    pd.DataFrame: DataFrame con las columnas procesadas.
    """
    processed_df = df.copy()
    resistance_columns = [col for col in df.columns if 'Resistance' in col and '(y)' in col]
    
    for column in resistance_columns:
        try:
            
            # Convertir comas a puntos y asegurar tipo float        
            processed_df[column] = detrend_data(processed_df[column])
            processed_df[column] = normalize_data(processed_df[column])
        except Exception as e:
            print(f"Error en columna {column}: {str(e)}")
    
    return processed_df