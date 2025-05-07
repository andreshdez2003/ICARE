from pathlib import Path
import pandas as pd

def get_file_path(filename):
    """Busca el archivo en los directorios de entrada y salida."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / "Data" / "Input_Files"
    OUTPUT_DIR = BASE_DIR / "Data" / "Output_Files"

    output_path = OUTPUT_DIR / filename
    input_path = INPUT_DIR / filename

    if output_path.exists():
        print(f"Found file in Output_Files: {filename}")
        return output_path
    if input_path.exists():
        print(f"Found file in Input_Files: {filename}")
        return input_path
    
    print("File not found in Input_Files or Output_Files.")
    return None

def detect_file_type(file_path):
    """Detecta el tipo de archivo basado en su extensión."""
    extension = file_path.suffix.lower()
    
    if extension in ('.xls', '.xlsx', '.xlsm'):
        return 'excel'
    if extension == '.csv':
        return 'csv'
    return None

def read_file(filename):
    """Lee automáticamente archivos Excel o CSV desde los directorios designados."""
    file_path = get_file_path(filename)
    
    if not file_path:
        return None

    file_type = detect_file_type(file_path)
    
    if file_type == 'excel':
        try:
            df = pd.read_excel(file_path)
            print("Excel file read successfully.\n")
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None
            
    elif file_type == 'csv':
        try:
            df = pd.read_csv(file_path, sep=";")
            print("CSV file read successfully.\n")
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
            
    else:
        print(f"Unsupported file type: {file_path.suffix}")
        return None