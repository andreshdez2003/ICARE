def get_users_to_add():
    """Obtiene la lista de usuarios a añadir desde la entrada del usuario"""
    num_users = int(input("How many users would you like to add? "))
    return [input(f"Enter the name of user {i+1}: ").strip() for i in range(num_users)]

def add_event_columns(df, users):
    """Añade columnas de eventos para cada usuario al DataFrame"""
    for user in users:
        col_name = f"Events {user}"
        df[col_name] = None
        print(f"✅ New column '{col_name}' created.")
    return df

def add_events_columns(df):
    """Función principal para añadir columnas de eventos"""
    users = get_users_to_add()
    return add_event_columns(df, users)

def remove_x_columns(df):
    """Elimina columnas que contienen '(x)' en su nombre"""
    return df.loc[:, ~df.columns.str.contains(r'\(x\)', regex=True)]

def remove_highcharts_column(df):
    """Elimina la columna Highcharts si existe"""
    if 'Highcharts' in df.columns:
        df = df.drop(columns=['Highcharts'])
        print("Column 'Highcharts' has been removed during standardization.")
    return df

def get_date_column(df):
    """Encuentra la columna de fecha (asume que es la primera que contiene 'date')"""
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    return date_cols[0] if date_cols else None

def build_ordered_columns(df, main_measurements, date_col):
    """Construye el orden principal de columnas basado en las mediciones principales"""
    new_columns = [date_col]
    
    for measurement in main_measurements:
        for i, col in enumerate(df.columns):
            if measurement in col and col not in new_columns:
                new_columns.append(col)
                # Añadir posible columna de unidad si existe
                if i + 1 < len(df.columns):
                    next_col = df.columns[i + 1]
                    if next_col not in new_columns:
                        new_columns.append(next_col)
                break  # Pasar a siguiente medición
    return new_columns

def reorder_dataframe_columns(df):
    """Reordena las columnas del DataFrame según el esquema especificado"""
    main_measurements = [
        "Temperature", "Humidity",
        "Resistance 1", "Resistance 2",
        "Resistance 3", "Resistance 4"
    ]
    
    date_col = get_date_column(df)
    if not date_col:
        raise ValueError("No se encontró columna de fecha en el DataFrame")
    
    ordered_columns = build_ordered_columns(df, main_measurements, date_col)
    
    # Añadir columnas restantes
    remaining_cols = [col for col in df.columns if col not in ordered_columns]
    return df[ordered_columns + remaining_cols]

def standardize_dataframe(df):
    """Función principal para estandarizar el DataFrame"""
    # Verificar si existen columnas de eventos
    has_events_columns = any(col.startswith("Events ") for col in df.columns)
    
    # Solo aplicar estandarización si no hay columnas de eventos
    if not has_events_columns:
        df = remove_x_columns(df)
        df = remove_highcharts_column(df)
        df = reorder_dataframe_columns(df)
        print("DataFrame estandarizado (primera configuración).")
    else:
        print("DataFrame ya contiene columnas de eventos. Saltando estandarización inicial.")
    
    return df