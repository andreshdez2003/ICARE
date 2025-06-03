import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
from Utils import plot_menu

def select_column(df, keyword):
    """
    Selects the first column that matches the provided keyword (case-insensitive).
    """
    column_matches = [col for col in df.columns if keyword.lower() in col.lower()]
    return column_matches[0] if column_matches else None

def get_date_range():
    """
    Prompts the user to input a valid date range.
    Returns:
        A tuple of (start_date, end_date) as pandas Timestamps.
        Returns (None, None) if the input is invalid.
    """
    try:
        start_input = input("Enter the start date (YYYY-MM-DD HH:MM:SS): ")
        end_input = input("Enter the end date (YYYY-MM-DD HH:MM:SS): ")
        return pd.to_datetime(start_input), pd.to_datetime(end_input)
    except Exception as e:
        print(f"X Invalid date format. Error: {e}")
        return None, None

def filter_by_date(df, start_date, end_date):
    """
    Filters the DataFrame by a date range.
    Assumes the column is named 'Date'.
    """
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask]

def setup_plot_style(ax, column_name, start_date, end_date):
    """
    Configures plot formatting and appearance.
    """
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d %H:%M"))
    plt.xticks(rotation=45)
    ax.set_title(f"{column_name} from {start_date} to {end_date}")
    ax.set_xlabel("Date")
    ax.set_ylabel(column_name)
    ax.legend()
    ax.grid(True)

def plot_data(filtered_df, column_name, start_date, end_date, event_column=None):
    """
    Creates and shows the plot.
    If event_column is present, overlays detected event points.
    """
    fig, ax = plt.subplots(figsize=(16, 6), dpi=100)
    ax.plot(filtered_df['Date'], filtered_df[column_name], label=column_name, color='blue')

    # Overlay event markers if available
    if event_column and event_column in filtered_df.columns:
        event_mask = filtered_df[event_column].notna()
        events = filtered_df[event_mask]
        ax.scatter(events['Date'], events[column_name], color='red', label='Detected Events', zorder=5)

    setup_plot_style(ax, column_name, start_date, end_date)
    plt.tight_layout()
    plt.show(block=False)

def plot_column(df, event_column='detected_events'):
    """
    Main function to handle full plot workflow:
    - Select column
    - Select date range
    - Filter and plot with optional event markers
    """
    keyword = plot_menu()
    if not keyword:
        return

    column_name = select_column(df, keyword)
    if not column_name:
        print(f"X No column containing '{keyword}' found.")
        return

    start_date, end_date = get_date_range()
    if None in [start_date, end_date]:
        return

    filtered_df = filter_by_date(df, start_date, end_date)
    if filtered_df.empty:
        print("X No data found in the specified date range.")
        return

    plot_data(filtered_df, column_name, start_date, end_date, event_column)
