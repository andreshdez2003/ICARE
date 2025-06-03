import pandas as pd

def find_closest_date_row(df, user_input):
    """
    Find the row index with the date closest to the user-specified target date.
    
    This function handles date parsing and finds the chronologically nearest match
    in the DataFrame, which is useful when exact timestamp matches aren't available.
    
    Args:
        df (pd.DataFrame): DataFrame containing a 'Date' column
        user_input (str): Date string in various formats (e.g., 'YYYY-MM-DD HH:MM:SS')
    
    Returns:
        int or None: Index of the row with the closest date, or None if error occurs
    """
    # Validate that the required 'Date' column exists
    if 'Date' not in df.columns:
        print("No 'Date' column found in the DataFrame.")
        return None

    # Convert 'Date' column to datetime format with error handling
    # errors='coerce' converts invalid dates to NaT (Not a Time)
    dates = pd.to_datetime(df['Date'], errors='coerce')

    # Parse the user's target date input
    try:
        target_date = pd.to_datetime(user_input)
    except Exception as e:
        print(f"Invalid date format. Error: {e}")
        return None

    # Calculate absolute time differences between target and all dates
    # This creates a Series of time deltas showing distance from target
    time_diffs = (dates - target_date).abs()

    # Find all rows that have the minimum time difference
    min_diff = time_diffs.min()
    candidates = df[time_diffs == min_diff]

    # Handle ties by selecting the chronologically earliest candidate
    # This provides consistent behavior when multiple dates are equidistant
    closest_row_index = candidates.sort_values('Date').index[0]

    return closest_row_index

def select_event_column_name(df):
    """
    Automatically detect or let user select an event-related column from the DataFrame.
    
    This function provides intelligent column detection for event annotation,
    handling cases with single, multiple, or no event columns gracefully.
    
    Args:
        df (pd.DataFrame): DataFrame to search for event columns
    
    Returns:
        str or None: Selected column name, or None if no event columns found
    """
    # Search for columns containing 'event' (case-insensitive)
    # This catches variations like 'Event', 'events', 'EVENT_TYPE', etc.
    event_columns = [col for col in df.columns if 'event' in col.lower()]
    
    if not event_columns:
        print(" No 'event' columns found.")
        return None
    
    elif len(event_columns) == 1:
        # Automatic selection when only one option exists
        print(f"Only one event column found: {event_columns[0]}")
        return event_columns[0]
    
    else:
        # Interactive selection when multiple event columns exist
        print("Multiple event columns found:")
        for i, col in enumerate(event_columns, 1):
            print(f"{i}. {col}")
        
        # Input validation loop ensures valid selection
        while True:
            try:
                choice = int(input(f"Choose an event column (1-{len(event_columns)}): "))
                if 1 <= choice <= len(event_columns):
                    return event_columns[choice - 1]
                else:
                    print("Invalid option. Please choose a valid number.")
            except ValueError:
                print("Please enter a number.")


class InvalidDateRangeError(Exception):
    """
    Custom exception for handling invalid date range scenarios.
    
    Raised when the start date occurs chronologically after the end date,
    which would create an invalid time interval for event annotation.
    """
    pass

def annotate_event_in_dataframe(df, event_column):
    """
    Interactive function to annotate events in a DataFrame within a specified date range.
    
    This function guides users through the process of defining event boundaries
    and applying event labels to the corresponding rows in the DataFrame.
    It includes comprehensive error handling and validation.
    
    Args:
        df (pd.DataFrame): DataFrame to annotate with events
        event_column (str): Name of the column where event labels will be stored
    
    Returns:
        pd.DataFrame: Modified DataFrame with new event annotations
    """
    while True:
        try:
            # Step 1: Get and validate start date from user
            start_date_input = input("Enter the start date of the event (format YYYY-MM-DD HH:MM:SS): ")
            start_index = find_closest_date_row(df, start_date_input)
            print(f"Start index found: {start_index}")

            # Step 2: Get and validate end date from user
            end_date_input = input("Enter the end date of the event (format YYYY-MM-DD HH:MM:SS): ")
            end_index = find_closest_date_row(df, end_date_input)
            print(f"End index found: {end_index}")

            # Step 3: Validate chronological order of dates
            # Ensures that the event duration makes logical sense
            if start_index > end_index:
                raise InvalidDateRangeError(f"Start date index ({start_index}) is after end date index ({end_index}). Please enter a valid date range.")

            # Step 4: Get event name after validating date range
            # This prevents unnecessary input when dates are invalid
            event_name = input("Enter the name of the event: ")

            # Step 5: Apply event annotation to the specified range
            # Uses inclusive range (start_index:end_index) to mark all rows in the event period
            df.loc[start_index:end_index, event_column] = event_name
            print(f" Event '{event_name}' added to column '{event_column}' from index {start_index} to {end_index}.")

            break  # Exit the retry loop when annotation succeeds

        except InvalidDateRangeError as e:
            # Handle specific case of chronologically invalid date ranges
            print(f"X {e}")
            print("Please re-enter the dates.\n")

        except Exception as e:
            # Catch-all for any unexpected errors during the annotation process
            print(f"X Unexpected error: {e}")
            print("Please try again.\n")

    return df