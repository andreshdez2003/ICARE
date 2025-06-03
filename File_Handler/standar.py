def get_users_to_add():
    """
    Prompts the user to enter how many users they want to add,
    and then collects their names via input.

    Returns:
    - A list of user names.
    """
    num_users = int(input("How many users would you like to add? "))
    return [input(f"Enter the name of user {i+1}: ").strip() for i in range(num_users)]

def add_event_columns(df, users):
    """
    Adds a new column for each user to store their events.

    Parameters:
    - df: The DataFrame to modify.
    - users: A list of user names.

    Returns:
    - The modified DataFrame with new "Events <user>" columns.
    """
    for user in users:
        col_name = f"Events {user}"
        df[col_name] = None  # Initialize column with None values
        print(f"New column '{col_name}' created.")
    return df

def add_events_columns(df):
    """
    Main function to interactively add event columns to a DataFrame.

    Returns:
    - The modified DataFrame.
    """
    users = get_users_to_add()
    return add_event_columns(df, users)

def remove_x_columns(df):
    """
    Removes all columns whose names contain '(x)'.

    Parameters:
    - df: The DataFrame to clean.

    Returns:
    - The cleaned DataFrame.
    """
    return df.loc[:, ~df.columns.str.contains(r'\(x\)', regex=True)]

def remove_highcharts_column(df):
    """
    Removes the 'Highcharts' column if it exists.

    Parameters:
    - df: The DataFrame to modify.

    Returns:
    - The DataFrame without the 'Highcharts' column.
    """
    if 'Highcharts' in df.columns:
        df = df.drop(columns=['Highcharts'])
        print("Column 'Highcharts' has been removed during standardization.")
    return df

def get_date_column(df):
    """
    Finds the first column in the DataFrame whose name contains 'date' (case insensitive).

    Parameters:
    - df: The DataFrame to inspect.

    Returns:
    - The name of the date column, or None if not found.
    """
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    return date_cols[0] if date_cols else None

def build_ordered_columns(df, main_measurements, date_col):
    """
    Builds a list of columns to reorder the DataFrame.

    Parameters:
    - df: The DataFrame to reorder.
    - main_measurements: A list of important measurement strings.
    - date_col: The name of the date column.

    Returns:
    - A list of columns in the desired order.
    """
    new_columns = [date_col]

    for measurement in main_measurements:
        for i, col in enumerate(df.columns):
            if measurement in col and col not in new_columns:
                new_columns.append(col)

                # Optionally add the next column (e.g. units) if not already included
                if i + 1 < len(df.columns):
                    next_col = df.columns[i + 1]
                    if next_col not in new_columns:
                        new_columns.append(next_col)
                break  # Move on to next measurement
    return new_columns

def reorder_dataframe_columns(df):
    """
    Reorders DataFrame columns to place date and main measurement columns first.

    Parameters:
    - df: The DataFrame to reorder.

    Returns:
    - The reordered DataFrame.
    """
    main_measurements = [
        "Temperature", "Humidity",
        "Resistance 1", "Resistance 2",
        "Resistance 3", "Resistance 4"
    ]

    date_col = get_date_column(df)
    if not date_col:
        raise ValueError("No date column found in the DataFrame")

    ordered_columns = build_ordered_columns(df, main_measurements, date_col)

    # Append any remaining columns
    remaining_cols = [col for col in df.columns if col not in ordered_columns]
    return df[ordered_columns + remaining_cols]

def standardize_dataframe(df):
    """
    Standardizes the DataFrame by:
    - Adding event columns (if they don't already exist),
    - Removing '(x)' columns,
    - Removing 'Highcharts' column,
    - Reordering columns.

    Parameters:
    - df: The DataFrame to standardize.

    Returns:
    - The standardized DataFrame.
    """
    # Check if any event columns already exist
    has_events_columns = any(col.startswith("Events ") for col in df.columns)

    if not has_events_columns:
        # Ask user for a valid name to create a default event column
        while True:
            user_name = input("Enter the name of the user to add: ").strip()
            if user_name:
                df = add_event_columns(df, [user_name])
                break
            else:
                print("No user name provided. Please enter a valid name.")

        # Apply cleanup and ordering
        df = remove_x_columns(df)
        df = remove_highcharts_column(df)
        df = reorder_dataframe_columns(df)
        print("DataFrame standardized (initial setup).")
    else:
        print("DataFrame already contains event columns. Skipping initial standardization.")

    return df