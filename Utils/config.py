"""
Centralized configuration parameters for the event detection project.

This module contains all tunable parameters and settings used across different
components of the event detection pipeline, including preprocessing, feature
extraction, anomaly detection algorithms, and validation metrics.
"""

# =============================================================================
# GENERAL CONFIGURATION
# =============================================================================
TIMESTAMP_COL = "Timestamp"  # Column name for timestamp data
EVENT_COL = "Event"          # Column name for annotated ground truth events

# =============================================================================
# FEATURE EXTRACTION PARAMETERS
# =============================================================================
# Principal Component Analysis (PCA) settings
PCA_COMPONENTS = 3           # Number of principal components to retain
                            # Controls dimensionality reduction - fewer components
                            # reduce noise but may lose important signal information

# =============================================================================
# ANOMALY DETECTION ALGORITHM PARAMETERS
# =============================================================================
# CUSUM (Cumulative Sum) change detection parameters
CUSUM_THRESHOLD = 400       # Detection threshold for cumulative sum
                           # Higher values reduce false positives but may miss subtle changes
                           # Should be adjusted based on your data's typical variance

# CUSUM_THRESHOLD_FACTOR = 1000  # Alternative threshold scaling factor (currently disabled)
                                # Can be used for automatic threshold calculation

CUSUM_TRAIN_SIZE = 0.1      # Fraction of initial data used for baseline statistics
                           # Determines how much historical data is used to establish
                           # normal behavior patterns (mean and covariance)

# DBSCAN clustering parameters for spatial-temporal event grouping
DBSCAN_EPS = 5              # Maximum distance between samples in the same neighborhood
                           # Measured in timesteps - controls how close points must be
                           # to be considered part of the same event cluster

DBSCAN_MIN_SAMPLES = 5      # Minimum number of samples required to form a dense region
                           # Higher values create more conservative clustering,
                           # requiring stronger evidence for event detection

# =============================================================================
# VALIDATION AND EVALUATION PARAMETERS
# =============================================================================
VALIDATION_WINDOW = 5       # Temporal window size (in timesteps) for event matching
                           # Allows some tolerance when comparing detected events
                           # with ground truth annotations

MIN_OVERLAP = 0.3           # Minimum overlap ratio required for valid detection
                           # Range: 0.0 to 1.0, where 1.0 requires perfect overlap
                           # Lower values are more permissive for event boundaries

# =============================================================================
# SLIDING WINDOW PROCESSING PARAMETERS
# =============================================================================
WINDOW_SIZE = 36            # Size of sliding window in samples
                           # Determines how much data is processed at once
                           # Larger windows capture longer-term patterns but use more memory

WINDOW_OVERLAP = 0          # Overlap between consecutive windows (in samples)
                           # Zero overlap means non-overlapping windows
                           # Positive values create smoother transitions but increase computation

# =============================================================================
# FILE SYSTEM PATHS
# =============================================================================
# Directory structure for organized data management
OUTPUT_DIR = "Data/Output_Files"        # Directory for algorithm results and reports
PROCESSED_DIR = "Data/Processed_Files"  # Directory for preprocessed/cleaned data
TEST_DIR = "Data/Test_Files"           # Directory for test datasets and validation data