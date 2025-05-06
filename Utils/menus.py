def file_menu():
    while True:
        print("What type of file would you like to read?")
        print("1. Excel file (.xls or .xlsx)")
        print("2. CSV file (.csv)")
        option = input("Choose an option (1 or 2): ")

        if option in ["1", "2"]:
            return option
        else:
            print("Invalid option. Please try again.\n")

def plot_menu():
    plot_choices = {
        "1": "Temperature",
        "2": "Humidity",
        "3": "Resistance 1",
        "4": "Resistance 2",
        "5": "Resistance 3",
        "6": "Resistance 4"
    }

    print("\n📊 What would you like to plot?")
    for key, value in plot_choices.items():
        print(f"{key}. {value}")

    option = input("Enter a number (1-6): ").strip()

    if option in plot_choices:
        return plot_choices[option]
    else:
        print("❌ Invalid choice.")
        return None

def plot_preprocesing_menu():
    print("\nSeleccione el tipo de gráfico:")
    print("1. Señal original")
    print("2. Señal procesada (sin tendencia/normalizada)")
    choice = input("Opción (1 o 2): ")
    return choice