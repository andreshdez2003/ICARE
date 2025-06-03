import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

def detect_events_with_dbscan(data: np.ndarray, eps) -> pd.DataFrame:
    """
    Applies DBSCAN clustering to 2D data to detect event segments.

    Parameters:
    - data: A 2D NumPy array (shape: [n_samples, n_features]) representing the input data.
    - eps: The epsilon parameter for DBSCAN, which defines the neighborhood radius.

    Returns:
    - A pandas DataFrame with the following columns:
        - start: Start index of the cluster in the input data (local index).
        - end: End index of the cluster in the input data (local index).
        - event_type: A label for the cluster (e.g., 'Event_0').
        - confidence: Proportion of data points that belong to the cluster (len(cluster) / len(data)).
    """
    # Run DBSCAN clustering
    db = DBSCAN(eps=eps, min_samples=2).fit(data)
    labels = db.labels_

    events = []

    # Iterate over all unique cluster labels
    for cluster_id in np.unique(labels):
        if cluster_id == -1:
            continue  # Skip noise points

        # Get indices of points in this cluster
        cluster_mask = (labels == cluster_id)
        cluster_indices = np.where(cluster_mask)[0]

        # Record the event segment and confidence
        events.append({
            "start": cluster_indices.min(),
            "end": cluster_indices.max(),
            "event_type": f"Event_{cluster_id}",
            "confidence": len(cluster_indices) / len(data)
        })

    return pd.DataFrame(events, columns=["start", "end", "event_type", "confidence"])
