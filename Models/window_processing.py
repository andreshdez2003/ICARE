import pandas as pd
from Models.change_detection import multivariate_cusum
from Models.clustering import detect_events_with_dbscan
from Utils.config import WINDOW_SIZE, WINDOW_OVERLAP, PCA_COMPONENTS, DBSCAN_EPS
from Models.feature_engineering import apply_pca
import numpy as np

def process_data_by_windows(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa datos en ventanas aplicando PCA, detección de cambios y clustering DBSCAN.
    Devuelve eventos detectados con timestamps globales.
    """
    all_events = []
    step = WINDOW_SIZE - WINDOW_OVERLAP

    try:
        for start_idx in range(0, len(raw_data), step):
            end_idx = start_idx + WINDOW_SIZE
            window = raw_data.iloc[start_idx:end_idx]

            # 1. Aplicar PCA
            window_pca = apply_pca(window, n_components=PCA_COMPONENTS)
            if window_pca.empty or len(window_pca) < 10:
                continue

            # 2. Detección de cambios
            change_indices = multivariate_cusum(window_pca)

            if change_indices.size > 0:
                # 3. Obtener datos y sus índices locales
                change_data = window_pca.iloc[change_indices].reset_index(drop=True)

                # 4. Clustering en los datos (no en índices)
                events = detect_events_with_dbscan(change_data.values)

                # 5. Validación robusta
                expected_cols = {"start", "end"}
                if isinstance(events, pd.DataFrame) and not events.empty and expected_cols.issubset(events.columns):

                    # 6. Mapeo seguro a índices globales
                    events["start_window"] = change_indices[events["start"]]
                    events["end_window"] = change_indices[events["end"]]

                    events["start"] = events["start_window"] + start_idx
                    events["end"] = events["end_window"] + start_idx

                    # 7. Limpieza y duración
                    events = events.drop(["start_window", "end_window"], axis=1)
                    events["duration"] = events["end"] - events["start"] + 1

                    if "duration" in events.columns:
                        events = events[events["duration"] >= 5]

                    all_events.append(events)

        # 8. Consolidar resultados
        final_events = pd.concat(all_events, ignore_index=True) if all_events else pd.DataFrame()

        if not final_events.empty:
            final_events = final_events.sort_values("confidence", ascending=False)
            final_events = final_events.drop_duplicates(subset=["start", "end"], keep="first")

        return final_events

    except Exception as e:
        print(f"❌ Error en procesamiento por ventanas: {str(e)}")
        return pd.DataFrame()
