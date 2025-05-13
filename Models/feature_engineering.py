from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

def apply_pca(processed_data: pd.DataFrame, n_components: int = 3) -> pd.DataFrame:
    """
    Aplica PCA a las columnas filtradas con '(y)' en los nombres.

    Retorna un DataFrame con componentes principales.
    Si hay menos muestras o columnas que n_components, se omite la ventana.
    """
    try:
        # Filtrar columnas con '(y)'
        features = processed_data.filter(like='(y)')
        
        # Validación de dimensiones mínimas para PCA
        if features.shape[0] < n_components or features.shape[1] < n_components:
            print(f"⚠️ Ventana descartada para PCA: shape {features.shape}, index: {processed_data.index[0]}–{processed_data.index[-1]}")
            return pd.DataFrame()

        # Aplicar PCA
        pca = PCA(n_components=n_components)
        pca_components = pca.fit_transform(features)

        # Crear DataFrame con los componentes
        pca_df = pd.DataFrame(
            pca_components,
            columns=[f"PCA_{i+1}" for i in range(n_components)],
            index=processed_data.index
        )
        return pca_df

    except Exception as e:
        print(f"❌ Error en PCA: {str(e)}")
        return pd.DataFrame()
