# -*- coding: utf-8 -*-
"""
Parámetros centralizados para el proyecto de detección de eventos.
"""

# Configuración general
TIMESTAMP_COL = "Timestamp"  # Nombre de la columna de timestamps
EVENT_COL = "Event"          # Nombre de la columna de eventos anotados

# Parámetros para PCA
PCA_COMPONENTS = 3           # Número de componentes principales

# Parámetros para CUSUM
CUSUM_THRESHOLD = 400 
#CUSUM_THRESHOLD_FACTOR = 1000      # Umbral de detección de cambios (ajustar según escala de datos)
CUSUM_TRAIN_SIZE = 0.1       # Porcentaje de datos iniciales para calcular media/covarianza

# Parámetros para DBSCAN
DBSCAN_EPS = 5            # Radio de búsqueda (en unidades de timesteps)
DBSCAN_MIN_SAMPLES = 5       # Mínimo de puntos para formar cluster

# Parámetros de validación
VALIDATION_WINDOW = 5        # Ventana temporal (en timesteps) para coincidencia de eventos
MIN_OVERLAP = 0.3            # Solapamiento mínimo requerido para considerar detección válida

#Parametros de ventana
WINDOW_SIZE = 36       # Tamaño de ventana en muestras
WINDOW_OVERLAP = 0   # Solapamiento entre ventanas

# Rutas predeterminadas
OUTPUT_DIR = "Data/Output_Files"
PROCESSED_DIR = "Data/Processed_Files"
TEST_DIR = "Data/Test_Files"