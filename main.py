from pathlib import Path
import pandas as pd
import numpy as np
from Utils.lable import annotate_event_in_dataframe, select_event_column_name
from Utils.preprocessing import process_dataframe  # Corregido el nombre del módulo
from File_Handler.reader import read_file
from File_Handler.standar import standardize_dataframe
from File_Handler.saver import save_dataframe_to_excel
from Plotter import plot_column
from Models.window_processing import process_data_by_windows
from pandasgui import show


# Definir directorios 
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Data" / "Output_Files"
PROCESSED_DIR = BASE_DIR / "Data" / "Processed_Files"

# Paso 1: Leer archivo
df = read_file("standardized_Bathroom_Domenec.xlsx")
if df is None:
    print("❌ Failed to read the file. Please check the file path and format.")
    exit()

# Paso 2: Estandarizar el archivo
final_df = standardize_dataframe(df)

# Paso 3: Obtener nombre de columna para anotación de eventos
username = select_event_column_name(final_df)

# Menú principal actualizado
while True:
    print("\nChoose an option:")
    print("1. Modify dataframe (annotate an event)")
    print("2. Plot a signal")
    print("3. Preprocess data")
    print("4. Detect events (PCA + CUSUM + DBSCAN)")
    print("5. Exit and save the dataframe")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        try:
            final_df = annotate_event_in_dataframe(final_df, username)
        except Exception as e:
            print(f"❌ An error occurred during event annotation: {e}")
            continue

    elif choice == "2":
        try:
            plot_column(final_df)
        except Exception as e:
            print(f"❌ Error while plotting: {e}")

    elif choice == "3":
        try:
            final_df = process_dataframe(final_df, window_length=21, polyorder=3)
            print("✅ Dataframe preprocessed successfully.")
        except Exception as e:
            print(f"❌ Error during preprocessing: {e}")

    elif choice == "4":
        try:
            print("\n=== Starting Window-Based Event Detection ===")
            # Procesamiento principal

            final_events = process_data_by_windows(final_df)  # Usar datos crudos
            
            # Crear columnas con los tipos adecuados
            final_df["detected_events"] = pd.Series([np.nan] * len(final_df), dtype=object)
            final_df["confidence"] = np.nan  # está bien como float

            # Mapeo de eventos al dataframe original
            if not final_events.empty:
                for _, event in final_events.iterrows():
                    start = event["start"]
                    end = event["end"]
                    
                    # Validar límites del dataframe
                    start = max(start, 0)
                    end = min(end, len(final_df)-1)
                    
                    # Asignar valores con overwrite controlado
                    final_df.loc[start:end, "detected_events"] = event["event_type"]
                    final_df.loc[start:end, "confidence"] = event["confidence"]

            gui = show(final_df)
        except Exception as e:
            print(f"❌ Error durante detección de eventos: {str(e)}")

    elif choice == "5":
        filename = input("Enter a name for the output Excel file: ").strip()
        if not filename:
            print("⚠️ Invalid filename. DataFrame not saved.")
            print("Exiting the program.")
            break

        print("\nWhere would you like to save the file?")
        print("1. Output_Files")
        print("2. Processed_Files")
        dir_choice = input("Enter 1 or 2: ").strip()

        if dir_choice == "1":
            save_path = OUTPUT_DIR
        elif dir_choice == "2":
            save_path = PROCESSED_DIR
        else:
            print("⚠️ Invalid directory choice. DataFrame not saved.")
            print("Exiting the program.")
            break

        save_dataframe_to_excel(final_df, filename, save_path)
        print(f"✅ DataFrame saved successfully as {filename}.xlsx in '{save_path.name}'.")
        print("Exiting the program.")
        break

    else:
        print("⚠️ Invalid choice. Please enter 1-5.")