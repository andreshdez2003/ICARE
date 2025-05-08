
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

