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