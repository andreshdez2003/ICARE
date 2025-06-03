from pathlib import Path
import pandas as pd

def save_dataframe_to_csv(df, filename, output_dir): 
    """
    Saves a pandas DataFrame to a CSV file.

    Parameters:
    - df: The DataFrame to be saved.
    - filename: The name of the file (e.g., 'output.csv').
    - output_dir: The output directory (Path object) where the file will be saved.
    """
    try:
        # Create the output directory if it does not exist (including any necessary parent directories)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Construct the full path to the output file
        file_path = output_dir / filename
        
        # Save the DataFrame to a CSV file without the index column
        df.to_csv(file_path, index=False)
        
        print(f"DataFrame successfully saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

def save_dataframe_to_excel(df, filename, output_dir): 
    """
    Saves a pandas DataFrame to an Excel file.

    Parameters:
    - df: The DataFrame to be saved.
    - filename: The name of the file (e.g., 'output.xlsx').
    - output_dir: The output directory (Path object) where the file will be saved.
    """
    try:
        # Create the output directory if it does not exist (including any necessary parent directories)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Construct the full path to the output file
        file_path = output_dir / filename
        
        # Save the DataFrame to an Excel file without the index column
        df.to_excel(file_path, index=False)
        
        print(f"DataFrame successfully saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving Excel file: {e}")