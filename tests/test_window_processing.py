import itertools
from copy import deepcopy
import pandas as pd
import traceback

from Models.window_processing import process_data_by_windows
from Utils.compare_events import compare_event_detection
from File_Handler.saver import save_dataframe_to_excel

def get_pca_components_options():
    """
    Returns a list of PCA component options to test.
    """
    return [2, 3]

def get_cusum_thresholds():
    """
    Returns a list of threshold values for the CUSUM algorithm.
    """
    return [20, 50, 100, 300, 400, 500]

def get_dbscan_eps_options():
    """
    Returns a list of epsilon values for DBSCAN clustering.
    """
    return [5, 10]

def get_window_size_options():
    """
    Returns a list of window sizes (in samples) to apply during processing.
    """
    return [36, 60, 120, 240, 480]  # 36 = 3 min, 60 = 5 min, etc.

def get_window_overlap_options(window_size):
    """
    Returns a list of overlap sizes based on proportions of the given window size.
    """
    proportions = [0, 0.25, 0.5, 0.75]
    return [int(window_size * p) for p in proportions]

def run_event_detection_with_params(df: pd.DataFrame, pca, cusum, eps, win_size, overlap) -> float:
    """
    Runs the full detection pipeline with the given parameters.
    It modifies the DataFrame to include detected events and confidence scores,
    then returns the accuracy score from event comparison.

    Args:
        df (pd.DataFrame): Input signal data.
        pca (int): Number of PCA components.
        cusum (float): CUSUM detection threshold.
        eps (float): DBSCAN epsilon value.
        win_size (int): Size of the processing window.
        overlap (int): Size of overlap between windows.

    Returns:
        float: Accuracy score of the detection.
    """
    detected = process_data_by_windows(df, win_size, overlap, pca, cusum, eps)

    # Initialize detection columns
    df["detected_events"] = pd.Series([None] * len(df), dtype=object)
    df["confidence"] = None

    # Fill detection columns with event data
    for _, e in detected.iterrows():
        df.loc[e["start"]:e["end"], "detected_events"] = e["event_type"]
        df.loc[e["start"]:e["end"], "confidence"] = e["confidence"]

    return compare_event_detection(df)

def test_all_combinations(df: pd.DataFrame, save_path="tests/results_summary.csv"):
    """
    Tests all combinations of parameters using a given DataFrame and saves the results.

    Args:
        df (pd.DataFrame): Input data with ground truth labels.
        save_path (str): Path where the results file will be saved.
    """
    pca_options = get_pca_components_options()
    cusum_options = get_cusum_thresholds()
    eps_options = get_dbscan_eps_options()
    win_size_options = get_window_size_options()

    results = []

    # Iterate over all combinations of PCA, CUSUM, DBSCAN, and window size
    for pca, cusum, eps, win_size in itertools.product(
        pca_options, cusum_options, eps_options, win_size_options
    ):
        overlap_options = get_window_overlap_options(win_size)
        for overlap in overlap_options:
            print(f"Testing combination PCA={pca}, CUSUM={cusum}, EPS={eps}, WIN={win_size}, OV={overlap}")
            try:
                score = run_event_detection_with_params(df.copy(), pca, cusum, eps, win_size, overlap)

                results.append({
                    "PCA": pca,
                    "CUSUM": cusum,
                    "EPS": eps,
                    "WinSize": win_size,
                    "Overlap": overlap,
                    "Accuracy": score
                })
            except Exception as e:
                print(f"Error for combination PCA={pca}, CUSUM={cusum}, EPS={eps}, WIN={win_size}, OV={overlap}: {str(e)}")
                traceback.print_exc()

    # Save results to Excel
    results_df = pd.DataFrame(results)
    save_dataframe_to_excel(results_df, "test_window_processing_results.xlsx", save_path)
    print(f"Results saved to {save_path}")
