import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal

def multivariate_cusum(pca_components: pd.DataFrame, threshold: float) -> np.ndarray:
    """
    Applies a multivariate CUSUM algorithm to detect changes in PCA-reduced data.
    Includes regularization and stability measures for singular matrices.

    Parameters:
    - pca_components: DataFrame containing the PCA-transformed data.
    - threshold: CUSUM threshold for detecting a change point.

    Returns:
    - An array of indices where change points were detected.
    """
    try:
        data = pca_components.values
        n_samples, n_features = data.shape
        
        # Define training window size (at least twice the number of features)
        train_size = max(int(0.1 * n_samples), 2 * n_features)
        if train_size >= n_samples:
            return np.array([])  # Not enough data to run CUSUM
        
        # Estimate initial mean and covariance from training window
        mu = np.mean(data[:train_size], axis=0)
        cov = np.cov(data[:train_size], rowvar=False)
        
        # Add Tikhonov regularization to handle near-singular matrices
        cov += 1e-6 * np.eye(n_features)
        
        # If covariance is not positive definite, fall back to diagonal + regularization
        if np.any(np.linalg.eigvals(cov) <= 0):
            cov = np.diag(np.diag(cov)) + 1e-6 * np.eye(n_features)
        
        S = np.zeros(n_samples)        # CUSUM statistic
        change_points = []             # Detected change point indices
        
        # Iterate over each time step
        for t in range(1, n_samples):
            try:
                # Compute log-likelihood ratio using log-pdf differences
                log_prob = multivariate_normal.logpdf(data[t], mean=mu, cov=cov, allow_singular=True)
                log_prob_prev = multivariate_normal.logpdf(data[t-1], mean=mu, cov=cov, allow_singular=True)
                
                S[t] = max(0, S[t-1] + log_prob - log_prob_prev)

                # Detect change point if CUSUM exceeds the threshold
                if S[t] > threshold:
                    change_points.append(t)
                    
                    # Update mean and covariance using new window
                    new_start = t
                    new_end = min(t + train_size, n_samples)
                    if new_end - new_start < n_features:
                        break  # Avoid recalculating with too few points
                    
                    mu = np.mean(data[new_start:new_end], axis=0)
                    cov = np.cov(data[new_start:new_end], rowvar=False)
                    cov += 1e-6 * np.eye(n_features)
            
            except Exception as e:
                print(f"Warning at t={t}: {str(e)}")
                continue  # Continue processing in case of local error
        
        return np.unique(change_points)  # Remove duplicate detections

    except Exception as e:
        print(f"Error in CUSUM: {str(e)}")
        return np.array([])
