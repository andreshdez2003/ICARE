

def add_events_columns(df):
    num_users = int(input("How many users would you like to add? "))

    for i in range(num_users):
        user_name = input(f"Enter the name of user {i+1}: ").strip()

        event_col_name = f"Events {user_name}"

        # Directamente crea una nueva columna vacía
        df[event_col_name] = None
        print(f"✅ New column '{event_col_name}' created.")

    return df

def standardize_dataframe(df):
    # 1. Remove columns that contain '(x)' in their name
    df = df.loc[:, ~df.columns.str.contains(r'\(x\)', regex=True)]

    # 2. Remove 'Highcharts' column if it exists
    if 'Highcharts' in df.columns:
        df = df.drop(columns=['Highcharts'])
        print("🗑️ Column 'Highcharts' has been removed during standardization.")

    # 3. Identify base columns to reorder (after 'date')
    main_measurements = ["Temperature", "Humidity", 
                         "Resistance 1", "Resistance 2", 
                         "Resistance 3", "Resistance 4"]

    # 4. Find the 'date' column (assuming it's the first and called 'date')
    date_col = [col for col in df.columns if 'date' in col.lower()][0]

    # 5. Build the new column order
    new_columns = [date_col]  # Start with the date column

    for measurement in main_measurements:
        for i, col in enumerate(df.columns):
            if measurement in col and col not in new_columns:
                new_columns.append(col)
                # Try to add the next column (unit), unless it's already included
                if i + 1 < len(df.columns):
                    next_col = df.columns[i + 1]
                    if next_col not in new_columns:
                        new_columns.append(next_col)
                break  # Go to next measurement once found

    # 6. Add any remaining columns (if any)
    remaining_cols = [col for col in df.columns if col not in new_columns]
    new_columns.extend(remaining_cols)

    # 7. Reorder and return the dataframe
    df = df[new_columns]
    return df

    # 5. Add any remaining columns (if any)
    remaining_cols = [col for col in df.columns if col not in new_columns]
    new_columns.extend(remaining_cols)

    # 6. Reorder and return the dataframe
    df = df[new_columns]
    return df