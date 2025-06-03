import pandas as pd
import numpy as np
from pathlib import Path
from Utils.lable import annotate_event_in_dataframe, select_event_column_name
from Utils.preprocessing import process_dataframe 
from File_Handler.reader import read_file
from File_Handler.standar import standardize_dataframe
from File_Handler.saver import save_dataframe_to_excel
from pandasgui import show

from Plotter import plot_column
from Models.window_processing import process_data_by_windows, process_data_full_signal
from tests.test_window_processing import test_all_combinations

from Utils.config import *  

# Define directory structure for organized file management
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Data" / "Output_Files"
PROCESSED_DIR = BASE_DIR / "Data" / "Processed_Files"
TEST_DIR = BASE_DIR / "Data" / "Test_Files"

# Step 1: Read input file
# Load the standardized bathroom sensor data for processing
df = read_file("standardized_Bathroom_Domenec.xlsx")
if df is None:
    print("Failed to read the file. Please check the file path and format.")
    exit()

# Step 2: Standardize the dataframe structure
# Ensure consistent column names and data formats across different input files
final_df = standardize_dataframe(df)

# Step 3: Select or detect the event annotation column
# Automatically find or let user choose which column will store event labels
username = select_event_column_name(final_df)

# Main interactive menu loop
# Provides a comprehensive interface for data analysis and event detection workflow
while True:
    print("\nChoose an option:")
    print("1. Modify dataframe (annotate an event)")
    print("2. Plot a signal")
    print("3. Preprocess data")
    print("4. Detect events (PCA + CUSUM + DBSCAN) by windows")
    print("5. Exit and save the dataframe")
    print("6. Detect events (PCA + CUSUM + DBSCAN) full signal")
    print("7. Run parameter test (PCA + CUSUM + DBSCAN grid search)")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        # Manual event annotation functionality
        # Allows users to interactively label events in the time series data
        try:
            final_df = annotate_event_in_dataframe(final_df, username)
        except Exception as e:
            print(f"An error occurred during event annotation: {e}")
            continue

    elif choice == "2":
        # Data visualization functionality
        # Provides interactive plotting capabilities for different sensor channels
        try:
            plot_column(final_df)
        except Exception as e:
            print(f"Error while plotting: {e}")

    elif choice == "3":
        # Data preprocessing pipeline
        # Applies filtering, normalization, and cleaning to prepare data for analysis
        try:
            final_df = process_dataframe(final_df, window_length=21, polyorder=3)
            print("Dataframe preprocessed successfully.")
        except Exception as e:
            print(f"Error during preprocessing: {e}")

    elif choice == "4":
        # Window-based event detection
        # Processes data in sliding windows using PCA dimensionality reduction,
        # CUSUM change detection, and DBSCAN clustering for event identification
        try:
            print("\n=== Starting Window-Based Event Detection ===")
            final_events = process_data_by_windows(final_df, WINDOW_SIZE, WINDOW_OVERLAP, 
                                                 PCA_COMPONENTS, CUSUM_THRESHOLD, DBSCAN_EPS)
            
            # Initialize detection result columns
            final_df["detected_events"] = pd.Series([np.nan] * len(final_df), dtype=object)
            final_df["confidence"] = np.nan

            # Apply detected events to the dataframe with boundary checking
            if not final_events.empty:
                for _, event in final_events.iterrows():
                    start = max(event["start"], 0)
                    end = min(event["end"], len(final_df)-1)
                    final_df.loc[start:end, "detected_events"] = event["event_type"]
                    final_df.loc[start:end, "confidence"] = event["confidence"]

            # Launch interactive GUI for result visualization
            gui = show(final_df)
        except Exception as e:
            print(f"Error during event detection: {str(e)}")

    elif choice == "6":
        # Full-signal event detection
        # Applies the same detection pipeline to the entire dataset without windowing
        # This approach may capture longer-term patterns but uses more memory
        try:
            print("\n=== Starting Full-Signal Event Detection ===")
            final_events = process_data_full_signal(final_df, 
                                                    PCA_COMPONENTS, CUSUM_THRESHOLD, DBSCAN_EPS)

            # Initialize detection result columns
            final_df["detected_events"] = pd.Series([np.nan] * len(final_df), dtype=object)
            final_df["confidence"] = np.nan

            # Apply detected events to the dataframe with boundary checking
            if not final_events.empty:
                for _, event in final_events.iterrows():
                    start = max(event["start"], 0)
                    end = min(event["end"], len(final_df)-1)
                    final_df.loc[start:end, "detected_events"] = event["event_type"]
                    final_df.loc[start:end, "confidence"] = event["confidence"]

            # Launch interactive GUI for result visualization
            gui = show(final_df)
        except Exception as e:
            print(f"Error during full-signal event detection: {str(e)}")

    elif choice == "5":
        # Save and exit functionality
        # Allows users to save their processed data with annotations and detected events
        filename = input("Enter a name for the output Excel file: ").strip()
        if not filename:
            print("Invalid filename. DataFrame not saved.")
            print("Exiting the program.")
            break

        # Directory selection for organized output management
        print("\nWhere would you like to save the file?")
        print("1. Output_Files")
        print("2. Processed_Files")
        dir_choice = input("Enter 1 or 2: ").strip()

        if dir_choice == "1":
            save_path = OUTPUT_DIR
        elif dir_choice == "2":
            save_path = PROCESSED_DIR
        else:
            print("Invalid directory choice. DataFrame not saved.")
            print("Exiting the program.")
            break

        # Execute save operation and exit
        save_dataframe_to_excel(final_df, filename, save_path)
        print(f"DataFrame saved successfully as {filename}.xlsx in '{save_path.name}'.")
        print("Exiting the program.")
        break

    elif choice == "7":
        # Parameter optimization functionality
        # Runs grid search over different parameter combinations to find optimal settings
        # for the event detection pipeline on the current dataset
        try:
            print("\n=== Running Grid Search Over Parameters ===")
            test_all_combinations(final_df, save_path=TEST_DIR)
        except Exception as e:
            print(f"Error during parameter testing: {str(e)}")

    else:
        # Handle invalid menu selections
        print("Invalid choice. Please enter a number from 1 to 7.")