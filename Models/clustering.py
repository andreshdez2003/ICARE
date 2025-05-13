import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from Utils.config import DBSCAN_EPS

def detect_events_with_dbscan(data: np.ndarray) -> pd.DataFrame:
    """
    Versión corregida para datos 2D.
    Retorna DataFrame con:
    - start: Índice inicial en data (no global)
    - end: Índice final en data (no global)
    - event_type: Cluster ID
    - confidence: Confianza calculada
    """
    db = DBSCAN(eps=DBSCAN_EPS, min_samples=2).fit(data)
    labels = db.labels_
    
    events = []
    for cluster_id in np.unique(labels):
        if cluster_id == -1:
            continue
            
        cluster_mask = (labels == cluster_id)
        cluster_indices = np.where(cluster_mask)[0]
        
        events.append({
            "start": cluster_indices.min(),
            "end": cluster_indices.max(),
            "event_type": f"Event_{cluster_id}",
            "confidence": len(cluster_indices)/len(data)
        })
    
        return pd.DataFrame(events, columns=["start", "end", "event_type", "confidence"])