import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "Data" /"Output_Files"


def save_dataframe_to_csv(df, filename):
    """
    Saves a DataFrame to a CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame to save.
    - filename (str): The full path or name of the output CSV file (e.g. 'output.csv').
    """
    try:
        file_path = OUTPUT_DIR / filename
        df.to_csv(file_path, index=False)
        print(f"DataFrame saved successfully to '{file_path}'")
    except Exception as e:
        print(f"Error saving DataFrame to CSV: {e}")

def save_dataframe_to_excel(df, filename):
    try:
        file_path = OUTPUT_DIR / filename
        df.to_excel(file_path, index=False)
        print(f"DataFrame saved successfully to '{file_path}'")
    except Exception as e:
        print(f"Error saving DataFrame to xlsx: {e}")


