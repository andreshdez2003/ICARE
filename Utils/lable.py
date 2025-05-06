import pandas as pd
from datetime import datetime



def find_closest_date_row(df, user_input):
    # Check if 'Date' column exists
    if 'Date' not in df.columns:
        print("No 'Date' column found in the DataFrame.")
        return None

    # Ensure 'Date' column is in datetime format
    dates = pd.to_datetime(df['Date'], errors='coerce')

    try:
        target_date = pd.to_datetime(user_input)
    except Exception as e:
        print(f"Invalid date format. Error: {e}")
        return None

    # Calculate absolute differences without modifying df
    time_diffs = (dates - target_date).abs()

    # Find the rows with minimum difference
    min_diff = time_diffs.min()
    candidates = df[time_diffs == min_diff]

    # If multiple (equidistant), pick the earlier one
    closest_row_index = candidates.sort_values('Date').index[0]

    return closest_row_index

def select_event_column_name(df):

    # Find columns containing 'event' (case insensitive)
    event_columns = [col for col in df.columns if 'event' in col.lower()]
    
    if not event_columns:
        print(" No 'event' columns found.")
        return None
    
    elif len(event_columns) == 1:
        print(f"Only one event column found: {event_columns[0]}")
        return event_columns[0]
    
    else:
        print("Multiple event columns found:")
        for i, col in enumerate(event_columns, 1):
            print(f"{i}. {col}")
        
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
    """Custom exception for invalid date range."""
    pass

def annotate_event_in_dataframe(df, event_column):
    while True:
        try:
            # Step 1: Ask the user for the start date
            start_date_input = input("Enter the start date of the event (format YYYY-MM-DD HH:MM:SS): ")
            start_index = find_closest_date_row(df, start_date_input)
            print(f"Start index found: {start_index}")

            # Step 2: Ask the user for the end date
            end_date_input = input("Enter the end date of the event (format YYYY-MM-DD HH:MM:SS): ")
            end_index = find_closest_date_row(df, end_date_input)
            print(f"End index found: {end_index}")

            # Step 3: Check if start_index <= end_index
            if start_index > end_index:
                raise InvalidDateRangeError(f"Start date index ({start_index}) is after end date index ({end_index}). Please enter a valid date range.")

            # Step 4: Ask for event name once dates are valid
            event_name = input("Enter the name of the event: ")

            # Step 5: Fill the event name into the specified column for the selected range
            df.loc[start_index:end_index, event_column] = event_name
            print(f"✅ Event '{event_name}' added to column '{event_column}' from index {start_index} to {end_index}.")

            break  # Exit loop if successful

        except InvalidDateRangeError as e:
            print(f"❌ {e}")
            print("Please re-enter the dates.\n")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("Please try again.\n")

    return df