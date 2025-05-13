import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal
from Utils.config import CUSUM_THRESHOLD

def multivariate_cusum(pca_components: pd.DataFrame, threshold: float = CUSUM_THRESHOLD) -> np.ndarray:
    """
    Versión corregida con manejo de matrices singulares y regularización.
    """
    try:
        data = pca_components.values
        n_samples, n_features = data.shape
        
        # Tamaño mínimo de entrenamiento = 2 * n_features
        train_size = max(int(0.1 * n_samples), 2 * n_features)
        if train_size >= n_samples:
            return np.array([])
        
        # Inicializar parámetros con regularización
        mu = np.mean(data[:train_size], axis=0)
        cov = np.cov(data[:train_size], rowvar=False)
        cov += 1e-6 * np.eye(n_features)  # Regularización Tikhonov
        
        # Verificar definición positiva
        if np.any(np.linalg.eigvals(cov)) <= 0:
            cov = np.diag(np.diag(cov)) + 1e-6 * np.eye(n_features)
        
        S = np.zeros(n_samples)
        change_points = []
        
        for t in range(1, n_samples):
            try:
                # Usar pseudo-inversa para estabilidad numérica
                inv_cov = np.linalg.pinv(cov)
                log_prob = multivariate_normal.logpdf(data[t], mean=mu, cov=cov, allow_singular=True)
                log_prob_prev = multivariate_normal.logpdf(data[t-1], mean=mu, cov=cov, allow_singular=True)
                
                S[t] = max(0, S[t-1] + log_prob - log_prob_prev)
                
                if S[t] > threshold:
                    change_points.append(t)
                    # Actualizar parámetros con nueva venta
                    new_start = t
                    new_end = min(t + train_size, n_samples)
                    if new_end - new_start < n_features:
                        break  # Evitar ventanas demasiado pequeñas
                        
                    mu = np.mean(data[new_start:new_end], axis=0)
                    cov = np.cov(data[new_start:new_end], rowvar=False)
                    cov += 1e-6 * np.eye(n_features)  # Regularizar siempre
                    
            except Exception as e:
                print(f"Warning en t={t}: {str(e)}")
                continue
        
        return np.unique(change_points)  # Eliminar duplicados

    except Exception as e:
        print(f"Error en CUSUM: {str(e)}")
        return np.array([])