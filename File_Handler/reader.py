from pathlib import Path  # Imports Path for easier and safer file path manipulations
import pandas as pd       # Imports pandas for data handling (especially DataFrames)

def get_file_path(filename):
    """
    Searches for the specified filename in three standard project directories:
    - Input_Files
    - Output_Files
    - Processed_Files
    
    Returns the full path to the file if found, or None if not found.
    """
    # BASE_DIR points to the root of the project (two levels above this script)
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / "Data" / "Input_Files"
    OUTPUT_DIR = BASE_DIR / "Data" / "Output_Files"
    PROCESSED_DIR = BASE_DIR / "Data" / "Processed_Files"

    # Build full file paths for each directory
    output_path = OUTPUT_DIR / filename
    input_path = INPUT_DIR / filename
    processed_path = PROCESSED_DIR / filename

    # Check each directory in order of priority and return the path if the file exists
    if output_path.exists():
        print(f"Found file in Output_Files: {filename}")
        return output_path
    if input_path.exists():
        print(f"Found file in Input_Files: {filename}")
        return input_path
    if processed_path.exists():
        print(f"Found file in Processed_Files: {filename}")
        return processed_path

    # If the file wasn't found in any of the folders
    print("File not found in Input_Files, Output_Files, or Processed_Files.")
    return None

def detect_file_type(file_path):
    """
    Determines the type of file based on its extension.
    Returns 'excel' for Excel files, 'csv' for CSV files, or None if unsupported.
    """
    extension = file_path.suffix.lower()  # Get the lowercase file extension

    if extension in ('.xls', '.xlsx', '.xlsm'):
        return 'excel'
    if extension == '.csv':
        return 'csv'
    return None  # Unsupported file type

def read_file(filename):
    """
    Automatically reads Excel or CSV files from the designated directories.
    Uses get_file_path() to locate the file and detect_file_type() to determine how to read it.
    
    Returns a pandas DataFrame if successful, or None otherwise.
    """
    file_path = get_file_path(filename)

    if not file_path:
        return None  # File not found

    file_type = detect_file_type(file_path)

    if file_type == 'excel':
        try:
            # Read Excel file using ',' as the decimal separator
            df = pd.read_excel(file_path, decimal=',')
            print("Excel file read successfully.\n")
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

    elif file_type == 'csv':
        try:
            # Read CSV file using ';' as the field separator
            df = pd.read_csv(file_path, sep=";")
            print("CSV file read successfully.\n")
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    else:
        # Unsupported file type
        print(f"Unsupported file type: {file_path.suffix}")
        return None