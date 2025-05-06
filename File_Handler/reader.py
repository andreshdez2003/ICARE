from pathlib import Path
import pandas as pd


def read_file(option,filename):
    # Define folder paths
    BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up to '2TratamientoGases'
    INPUT_DIR = BASE_DIR / "Data" / "Input_Files" # Direct acces to the Input_Files folder
    OUTPUT_DIR = BASE_DIR / "Data" / "Output_Files"

    # Search first in OUTPUT_DIR
    output_path = OUTPUT_DIR / filename
    input_path = INPUT_DIR / filename

    if output_path.exists():
        file_path = output_path
        print(f"Found file in Output_Files: {file_path.name}")
    elif input_path.exists():
        file_path = input_path
        print(f"Found file in Input_Files: {file_path.name}")
    else:
        print("File not found in either Input_Files or Output_Files.")
        return None
  
    if option == "1":
        try:
            df = pd.read_excel(file_path)
            print("Excel file read successfully.\n")
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

    elif option == "2":
        try:
            df = pd.read_csv(file_path, sep=";")
            print("CSV file read successfully.\n")
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None