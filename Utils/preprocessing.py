from scipy.signal import savgol_filter
import pandas as pd
import numpy as np

def convert_columns_to_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Convert specified columns to numeric values by replacing commas with periods.
    
    This function handles European number formatting where commas are used as
    decimal separators instead of periods. It's essential for processing data
    exported from European systems or Excel files with regional formatting.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        columns (list): List of column names to convert
    
    Returns:
        pd.DataFrame: DataFrame with specified columns converted to numeric format
    """
    df = df.copy()  # Create copy to avoid modifying original DataFrame
    
    for col in columns:
        # Convert to string, replace commas with periods, then convert to numeric
        # errors='coerce' converts invalid values to NaN instead of raising errors
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
    
    return df

def apply_savgol_filter(df: pd.DataFrame, columns: list, window_length: int, polyorder: int) -> pd.DataFrame:
    """
    Apply Savitzky-Golay filter to specified columns for signal smoothing.
    
    The Savitzky-Golay filter is excellent for smoothing noisy sensor data while
    preserving important signal features like peaks and trends. It fits local
    polynomials to data points, providing better edge handling than simple moving averages.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        columns (list): List of column names to filter
        window_length (int): Length of the filter window (must be odd)
        polyorder (int): Order of polynomial used to fit samples
    
    Returns:
        pd.DataFrame: DataFrame with filtered columns
    """
    df = df.copy()  # Preserve original data
    
    for col in columns:
        try:
            # Apply Savitzky-Golay filter with 'nearest' mode for edge handling
            # This mode extends the data at boundaries using the nearest values
            df[col] = savgol_filter(df[col].values, 
                                  window_length=window_length, 
                                  polyorder=polyorder, 
                                  mode='nearest')
        except Exception as e:
            print(f"Error applying Savitzky-Golay filter to column {col}: {str(e)}")
    
    return df

def normalize_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalize specified columns to range [0, 1] using min-max scaling.
    
    Min-max normalization scales data to a fixed range, making it easier to
    compare different sensors with varying measurement ranges and units.
    This is particularly useful for multi-sensor analysis and machine learning.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        columns (list): List of column names to normalize
    
    Returns:
        pd.DataFrame: DataFrame with normalized columns
    """
    df = df.copy()  # Avoid modifying original data
    
    for col in columns:
        col_min = df[col].min()
        col_max = df[col].max()
        
        # Check for constant values to avoid division by zero
        if col_max != col_min:
            # Standard min-max normalization formula: (x - min) / (max - min)
            df[col] = (df[col] - col_min) / (col_max - col_min)
        else:
            # Set constant values to 0 when all values are identical
            df[col] = 0
            print(f"Warning: Column {col} contains constant values, set to 0 after normalization")
    
    return df

def process_dataframe(df: pd.DataFrame, window_length: int = 15, polyorder: int = 2) -> pd.DataFrame:
    """
    Complete preprocessing pipeline for sensor data analysis.
    
    This function implements a comprehensive data processing workflow specifically
    designed for resistance-based sensor data, applying numeric conversion,
    signal filtering, normalization, and data cleaning in sequence.
    
    Processing Steps:
    1. Convert columns with European decimal formatting to numeric
    2. Apply Savitzky-Golay filtering for noise reduction
    3. Normalize data to [0,1] range for consistent scaling
    4. Remove rows containing NaN values for clean analysis
    
    Args:
        df (pd.DataFrame): Input DataFrame containing sensor data with '(y)' columns
        window_length (int, optional): Filter window size. Defaults to 15.
                                     Should be odd and smaller than data length
        polyorder (int, optional): Polynomial order for filtering. Defaults to 2.
                                 Must be less than window_length
    
    Returns:
        pd.DataFrame: Fully processed DataFrame ready for analysis
    """
    processed_df = df.copy()
    
    # Identify resistance columns by looking for '(y)' pattern in column names
    # This assumes resistance measurements are labeled with this suffix
    resistance_columns = [col for col in df.columns if '(y)' in col]
    
    if not resistance_columns:
        print("Warning: No columns containing '(y)' found. Check column naming convention.")
        return processed_df

    # Step 1: Convert European decimal format to standard numeric format
    print(f"Converting {len(resistance_columns)} columns to numeric format...")
    processed_df = convert_columns_to_numeric(processed_df, resistance_columns)

    # Step 2: Apply Savitzky-Golay filtering for signal smoothing
    print(f"Applying Savitzky-Golay filter (window={window_length}, polyorder={polyorder})...")
    processed_df = apply_savgol_filter(processed_df, resistance_columns, window_length, polyorder)

    # Step 3: Normalize data to [0,1] range for consistent scaling
    print("Normalizing columns to [0,1] range...")
    processed_df = normalize_columns(processed_df, resistance_columns)

    # Step 4: Clean data by removing rows with NaN values
    print("Removing rows with NaN values...")
    nan_rows = processed_df[resistance_columns].isnull().any(axis=1)
    
    if nan_rows.any():
        # Report which rows are being removed for transparency
        removed_indices = processed_df[nan_rows].index.tolist()
        print(f"⚠️ Removed {len(removed_indices)} rows containing NaN values: {removed_indices}")
        processed_df = processed_df.drop(index=removed_indices)
    else:
        print("✅ No NaN values found, all data retained")

    print(f"✅ Processing complete. Final DataFrame shape: {processed_df.shape}")
    return processed_df