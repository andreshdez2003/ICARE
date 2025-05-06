from Utils.menus import file_menu,plot_preprocesing_menu
from Utils.lable import annotate_event_in_dataframe, select_event_column_name
from File_Handler.reader import read_file
from File_Handler.standar import standardize_dataframe, add_events_columns
from File_Handler.saver import save_dataframe_to_excel
from Plotter import plot_column, plot_processed

# Step 1: Read and prepare the dataframe
option = file_menu()
df = read_file(option, "standardized_Kitchen_Andres2.xlsx")

if df is None:
    print("Failed to read the file. Please check the file path and format.")
    exit()

print("\nIs the first time you open this file?:")
choice = input("Enter your choice (1(yes) or 2(no)): ")
if choice == "1":
    final_df = standardize_dataframe(df)
    final_df = add_events_columns(final_df)
elif choice == "2":
    final_df = df.copy()
# Step 3: Main loop to modify or exit
username = select_event_column_name(final_df)

while True:
    print("\nChoose an option:")
    print("1. Modify dataframe (annotate an event)")
    print("2. Plot a signal")
    print("3. Exit and save the dataframe")

    choice = input("Enter your choice (1, 2 or 3): ")

    if choice == "1":
        try:
            final_df = annotate_event_in_dataframe(final_df, username)
        except Exception as e:
            print(f"An error occurred during event annotation: {e}")
            print("Returning to the main menu.")
            continue  # Vuelve al inicio del bucle while

    elif choice == "2":
        try:
            # Submenú para elegir tipo de gráfico
            plot_choice = plot_preprocesing_menu()
            if plot_choice == "1":
                plot_column(final_df)
            elif plot_choice == "2":
                plot_processed(final_df)
            else:
                print("⚠️ Opción inválida. Volviendo al menú principal.")
        except Exception as e:
            print(f"❌ Error al graficar: {e}")
            print("Returning to the main menu.")

    elif choice == "3":
        save_dataframe_to_excel(final_df, "standardized_Kitchen_Andres2.xlsx")
        print("✅ DataFrame saved successfully. Exiting the program.")
        break

    else:
        print("⚠️ Invalid choice. Please enter 1, 2 or 3.")