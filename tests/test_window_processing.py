import itertools
from copy import deepcopy
import pandas as pd
import traceback


from Models.window_processing import process_data_by_windows
from Utils.compare_events import compare_event_detection

from File_Handler.saver import save_dataframe_to_excel


def get_pca_components_options():
    return [2, 3]


def get_cusum_thresholds():
    return [20, 50, 100, 300, 400, 500]


def get_dbscan_eps_options():
    return [5, 10 ]


def get_window_size_options():
    return [36, 60, 120 , 240 , 480] # 36 = 3mins, 60 = 5 mins, 120 = 10 mins


def get_window_overlap_options(window_size):
    proportions = [0, 0.25, 0.5, 0.75]
    return [int(window_size * p) for p in proportions]


def run_event_detection_with_params(df: pd.DataFrame, pca, cusum, eps, win_size, overlap) -> float:
    """
    Ejecuta el pipeline con parámetros específicos y devuelve el score de detección.
    """

    detected = process_data_by_windows(df, win_size, overlap, pca, cusum, eps)

    df["detected_events"] = pd.Series([None] * len(df), dtype=object)
    df["confidence"] = None

    for _, e in detected.iterrows():
        df.loc[e["start"]:e["end"], "detected_events"] = e["event_type"]
        df.loc[e["start"]:e["end"], "confidence"] = e["confidence"]

    return compare_event_detection(df)




def test_all_combinations(df: pd.DataFrame, save_path="tests/results_summary.csv"):
    """
    Ejecuta todas las combinaciones de parámetros utilizando un DataFrame proporcionado
    y guarda los resultados.
    """
    pca_options = get_pca_components_options()
    cusum_options = get_cusum_thresholds()
    eps_options = get_dbscan_eps_options()
    win_size_options = get_window_size_options()

    results = []

    for pca, cusum, eps, win_size in itertools.product(
        pca_options, cusum_options, eps_options, win_size_options
    ):
        overlap_options = get_window_overlap_options(win_size)  # Aquí genero solapamientos dependientes del tamaño ventana
        for overlap in overlap_options:
            print(f"Probando combinación PCA={pca}, CUSUM={cusum}, EPS={eps}, WIN={win_size}, OV={overlap}")  
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
                print(f"❌ Error en combinación PCA={pca}, CUSUM={cusum}, EPS={eps}, WIN={win_size}, OV={overlap}: {str(e)}")
                traceback.print_exc()

    results_df = pd.DataFrame(results)
    save_dataframe_to_excel(results_df, "test_window_processing_results.xlsx", save_path)
    print(f"✅ Resultados guardados en {save_path}")
