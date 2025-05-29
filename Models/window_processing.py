import pandas as pd
import numpy as np
from Models.change_detection import multivariate_cusum
from Models.clustering import detect_events_with_dbscan
from Models.feature_engineering import apply_pca
import traceback


def process_data_by_windows(raw_data: pd.DataFrame,window_size: int,window_overlap: int,pca_components: int,cusum_threshold: float,dbscan_eps: float) -> pd.DataFrame:
    """
    Procesa datos en ventanas aplicando PCA, detección de cambios y clustering DBSCAN.
    Devuelve eventos detectados con timestamps globales.
    """
    all_events = []
    step = window_size - window_overlap

    try:
        for start_idx in range(0, len(raw_data), step):
            end_idx = start_idx + window_size
            window = raw_data.iloc[start_idx:end_idx]
            if len(window) < 10:
                continue

            # 1. Aplicar PCA
            window_pca = apply_pca(window, n_components=pca_components)
            if window_pca.empty:
                continue

            # 2. Detección de cambios
            change_indices = multivariate_cusum(window_pca, threshold=cusum_threshold)

            if change_indices.size > 0:
                # 3. Obtener datos y sus índices locales
                change_data = window_pca.iloc[change_indices].reset_index(drop=True)

                # 4. Clustering en los datos (no en índices)
                events = detect_events_with_dbscan(change_data.values, eps=dbscan_eps)

                # ✅ Solo procesar si 'events' es un DataFrame válido
                expected_cols = {"start", "end"}
                if isinstance(events, pd.DataFrame) and not events.empty and expected_cols.issubset(events.columns):
                    
                    # 5. Mapeo seguro a índices globales
                    events["start_window"] = change_indices[events["start"]]
                    events["end_window"] = change_indices[events["end"]]

                    events["start"] = events["start_window"] + start_idx
                    events["end"] = events["end_window"] + start_idx

                    # 6. Limpieza y duración
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


def process_data_full_signal(raw_data: pd.DataFrame,window_size: int,window_overlap: int,pca_components: int,cusum_threshold: float,dbscan_eps: float) -> pd.DataFrame:
    """
    Procesa toda la señal completa (sin ventanas) aplicando PCA, CUSUM y DBSCAN.
    Devuelve eventos detectados en coordenadas globales.
    """
    try:
        # 1. PCA sobre toda la señal
        full_pca = apply_pca(raw_data, n_components=pca_components)
        if full_pca.empty or len(full_pca) < 10:
            return pd.DataFrame()

        # 2. Detección de cambios
        change_indices = multivariate_cusum(full_pca, threshold=cusum_threshold)
        if change_indices.size == 0:
            return pd.DataFrame()

        # 3. DBSCAN sobre los puntos de cambio
        change_data = full_pca.iloc[change_indices].reset_index(drop=True)
        events = detect_events_with_dbscan(change_data.values, eps=dbscan_eps)

        expected_cols = {"start", "end"}
        if isinstance(events, pd.DataFrame) and not events.empty and expected_cols.issubset(events.columns):
            # Mapeo de índices locales a índices originales
            events["start"] = change_indices[events["start"]]
            events["end"] = change_indices[events["end"]]
            events["duration"] = events["end"] - events["start"] + 1

            if "duration" in events.columns:
                events = events[events["duration"] >= 5]

            events = events.sort_values("confidence", ascending=False)
            events = events.drop_duplicates(subset=["start", "end"], keep="first")

            return events

        return pd.DataFrame()

    except Exception as e:
        print("❌ Error en procesamiento completo:")
        traceback.print_exc()
        return pd.DataFrame()
