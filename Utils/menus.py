def plot_menu():
    """
    Interactive menu for selecting which sensor data column to plot.
    
    This function presents a user-friendly menu interface for selecting from
    available sensor measurements, making it easy to visualize different data
    streams in a sensor monitoring or IoT application.
    
    Returns:
        str or None: The name of the selected column to plot, or None if invalid choice
    """
    # Define available plotting options with their display names
    # This dictionary maps menu numbers to actual column names expected in the DataFrame
    plot_choices = {
        "1": "Temperature",     # Environmental temperature sensor
        "2": "Humidity",        # Environmental humidity sensor  
        "3": "Resistance 1",    # First resistance measurement (possibly gas sensor)
        "4": "Resistance 2",    # Second resistance measurement
        "5": "Resistance 3",    # Third resistance measurement
        "6": "Resistance 4"     # Fourth resistance measurement
    }

    # Display the menu with clear formatting
    print("\n What would you like to plot?")
    for key, value in plot_choices.items():
        print(f"{key}. {value}")

    # Get user input with whitespace trimming for robustness
    option = input("Enter a number (1-6): ").strip()

    # Validate user selection and return the corresponding column name
    if option in plot_choices:
        return plot_choices[option]  # Return the column name for plotting
    else:
        print("Invalid choice.")
        return None  # Signal that no valid selection was made
