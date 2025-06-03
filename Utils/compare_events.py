import pandas as pd

def compare_event_detection(df: pd.DataFrame, event_col: str = "Events", detected_col: str = "detected_events") -> float:
    """
    Compare real events column with detected events column.
    Returns the percentage of matches between the two columns.
    
    Args:
        df: DataFrame containing event data
        event_col: Name of the ground truth events column (default: "Events")
        detected_col: Name of the detected events column (default: "detected_events")
    
    Returns:
        float: Percentage of matching rows (0.0 to 1.0)
    
    Raises:
        KeyError: If required columns are not found in the DataFrame
    """
    
    # 1) Automatically detect the ground truth column
    # Search for columns containing "events" in their name, excluding the detected column
    possible_columns = [col for col in df.columns if "events" in col.lower() and col != detected_col]
    if not possible_columns:
        raise KeyError("No event-related column found in the DataFrame.")
    event_col = possible_columns[0]  # Use the first matching column
    
    # 2) Verify that the detection column exists
    if detected_col not in df.columns:
        raise KeyError(f"Detected column '{detected_col}' not found in DataFrame.")

    positives = 0  # Counter for matching rows
    total = len(df)  # Total number of rows to compare

    # 3) Iterate through each row without converting values to strings
    # This preserves the original data types for accurate comparison
    for i in range(total):
        true_val = df.iloc[i][event_col]        # Ground truth value
        detected_val = df.iloc[i][detected_col] # Detected value
        
        # Check for matches using pandas null-aware comparison
        # Two cases count as matches:
        # - Both values are null/NaN
        # - Both values are non-null (regardless of their actual values)
        if (pd.isna(true_val) and pd.isna(detected_val)) or \
           (not pd.isna(true_val) and not pd.isna(detected_val)):
            positives += 1

    # 4) Print diagnostic information showing value distributions
    # Uses the dynamically detected column name for clarity
    print(f"Real events ({event_col}) - count distribution:")
    print(df[event_col].value_counts(dropna=False))
    print("Detected events (detected_events) - count distribution:")
    print(df[detected_col].value_counts(dropna=False))

    # Return the match percentage as a float between 0.0 and 1.0
    return positives / total if total > 0 else 0.0