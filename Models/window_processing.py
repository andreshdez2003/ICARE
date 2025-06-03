import pandas as pd
import numpy as np
from Models.change_detection import multivariate_cusum
from Models.clustering import detect_events_with_dbscan
from Models.feature_engineering import apply_pca
import traceback


def process_data_by_windows(raw_data: pd.DataFrame,
                            window_size: int,
                            window_overlap: int,
                            pca_components: int,
                            cusum_threshold: float,
                            dbscan_eps: float) -> pd.DataFrame:
    """
    Processes data in overlapping windows by applying PCA, change detection (CUSUM),
    and clustering (DBSCAN) to detect events.

    Parameters:
    - raw_data: The full input DataFrame to process.
    - window_size: Number of rows per window.
    - window_overlap: Overlap between consecutive windows.
    - pca_components: Number of PCA components to compute.
    - cusum_threshold: Threshold for the multivariate CUSUM algorithm.
    - dbscan_eps: Epsilon parameter for DBSCAN clustering.

    Returns:
    - A DataFrame of detected events with global start and end indices and event confidence.
    """
    all_events = []
    step = window_size - window_overlap

    try:
        for start_idx in range(0, len(raw_data), step):
            end_idx = start_idx + window_size
            window = raw_data.iloc[start_idx:end_idx]

            if len(window) < 10:
                continue

            # 1. Apply PCA to the window
            window_pca = apply_pca(window, n_components=pca_components)
            if window_pca.empty:
                continue

            # 2. Change point detection with CUSUM
            change_indices = multivariate_cusum(window_pca, threshold=cusum_threshold)

            if change_indices.size > 0:
                # 3. Extract the points where changes occurred
                change_data = window_pca.iloc[change_indices].reset_index(drop=True)

                # 4. Apply DBSCAN clustering to change data
                events = detect_events_with_dbscan(change_data.values, eps=dbscan_eps)

                # 5. Map local indices to global indices
                expected_cols = {"start", "end"}
                if isinstance(events, pd.DataFrame) and not events.empty and expected_cols.issubset(events.columns):
                    events["start_window"] = change_indices[events["start"]]
                    events["end_window"] = change_indices[events["end"]]

                    events["start"] = events["start_window"] + start_idx
                    events["end"] = events["end_window"] + start_idx

                    # 6. Add duration and filter out very short events
                    events = events.drop(["start_window", "end_window"], axis=1)
                    events["duration"] = events["end"] - events["start"] + 1
                    events = events[events["duration"] >= 5]

                    all_events.append(events)

        # 7. Combine all events into a single DataFrame
        final_events = pd.concat(all_events, ignore_index=True) if all_events else pd.DataFrame()

        # 8. Post-processing: remove duplicates and sort by confidence
        if not final_events.empty:
            final_events = final_events.sort_values("confidence", ascending=False)
            final_events = final_events.drop_duplicates(subset=["start", "end"], keep="first")

        return final_events

    except Exception as e:
        print(f"Error during windowed processing: {str(e)}")
        return pd.DataFrame()


def process_data_full_signal(raw_data: pd.DataFrame,
                             pca_components: int,
                             cusum_threshold: float,
                             dbscan_eps: float) -> pd.DataFrame:
    """
    Processes the entire signal as a whole (no windows) by applying PCA,
    change detection (CUSUM), and clustering (DBSCAN).

    Parameters:
    - raw_data: The full input DataFrame to process.
    - pca_components: Number of PCA components to compute.
    - cusum_threshold: Threshold for the multivariate CUSUM algorithm.
    - dbscan_eps: Epsilon parameter for DBSCAN clustering.

    Returns:
    - A DataFrame of detected events with global start and end indices and event confidence.
    """
    try:
        # 1. Apply PCA to the entire dataset
        full_pca = apply_pca(raw_data, n_components=pca_components)
        if full_pca.empty or len(full_pca) < 10:
            return pd.DataFrame()

        # 2. Apply CUSUM to detect changes
        change_indices = multivariate_cusum(full_pca, threshold=cusum_threshold)
        if change_indices.size == 0:
            return pd.DataFrame()

        # 3. Apply DBSCAN clustering to the change points
        change_data = full_pca.iloc[change_indices].reset_index(drop=True)
        events = detect_events_with_dbscan(change_data.values, eps=dbscan_eps)

        expected_cols = {"start", "end"}
        if isinstance(events, pd.DataFrame) and not events.empty and expected_cols.issubset(events.columns):
            # Map local indices to original indices
            events["start"] = change_indices[events["start"]]
            events["end"] = change_indices[events["end"]]
            events["duration"] = events["end"] - events["start"] + 1
            events = events[events["duration"] >= 5]

            events = events.sort_values("confidence", ascending=False)
            events = events.drop_duplicates(subset=["start", "end"], keep="first")

            return events

        return pd.DataFrame()

    except Exception:
        print("Error during full signal processing:")
        traceback.print_exc()
        return pd.DataFrame()
