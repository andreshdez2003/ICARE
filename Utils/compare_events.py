import pandas as pd

def compare_event_detection(df: pd.DataFrame, event_col: str = "Events", detected_col: str = "detected_events") -> float:
    """
    Compara las columnas de eventos reales y detectados. 
    Devuelve el % de coincidencias.
    """
    # 1) Detectar automáticamente la columna de verdad
    possible_columns = [col for col in df.columns if "events" in col.lower() and col != detected_col]
    if not possible_columns:
        raise KeyError("No se encontró ninguna columna relacionada a eventos en el DataFrame.")
    event_col = possible_columns[0]
    
    # 2) Verificar columna de detección
    if detected_col not in df.columns:
        raise KeyError(f"Columna detectada '{detected_col}' no encontrada.")

    positives = 0
    total = len(df)

    # 3) Recorre fila a fila sin convertir a string
    for i in range(total):
        true_val     = df.iloc[i][event_col]
        detected_val = df.iloc[i][detected_col]
        
        # Comprueba nulos con pd.isna()
        if (pd.isna(true_val)     and pd.isna(detected_val)) or \
           (not pd.isna(true_val) and not pd.isna(detected_val)):
            positives += 1

    # 4) Informes de conteos usando la columna dinámica
    print(f"Eventos reales ({event_col}) – conteo:")
    print(df[event_col].value_counts(dropna=False))
    print("Eventos detectados (detected_events) – conteo:")
    print(df[detected_col].value_counts(dropna=False))

    return positives / total if total > 0 else 0.0
