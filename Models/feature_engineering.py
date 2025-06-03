from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

def apply_pca(processed_data: pd.DataFrame, n_components: int = 3) -> pd.DataFrame:
    """
    Applies Principal Component Analysis (PCA) to columns containing '(y)' in their names.

    Parameters:
    - processed_data: A DataFrame containing the data to transform.
    - n_components: Number of principal components to compute.

    Returns:
    - A new DataFrame containing the PCA-transformed data with columns named 'PCA_1', 'PCA_2', etc.
      If the number of samples or features is less than n_components, an empty DataFrame is returned.
    """
    try:
        # Select columns that contain '(y)' in their names
        features = processed_data.filter(like='(y)')
        
        # Validate dimensions: need at least n_components rows and columns
        if features.shape[0] < n_components or features.shape[1] < n_components:
            print(f"Window skipped for PCA: shape {features.shape}, index: {processed_data.index[0]}–{processed_data.index[-1]}")
            return pd.DataFrame()

        # Apply PCA
        pca = PCA(n_components=n_components)
        pca_components = pca.fit_transform(features)

        # Create DataFrame for PCA components with same index as input
        pca_df = pd.DataFrame(
            pca_components,
            columns=[f"PCA_{i+1}" for i in range(n_components)],
            index=processed_data.index
        )
        return pca_df

    except Exception as e:
        print(f"Error during PCA: {str(e)}")
        return pd.DataFrame()