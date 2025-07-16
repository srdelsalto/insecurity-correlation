# scripts/limpieza.py

import pandas as pd
import os
import unicodedata

# Obtiene la ruta absoluta del directorio raíz del proyecto
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')
PREPROCESSED_PATH = os.path.join(PROJECT_ROOT, 'data', 'preprocessed')
PROCESSED_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed')

def cargar_dataset(nombre_archivo, hoja=None):
    ruta = os.path.join(RAW_PATH, nombre_archivo)
    if nombre_archivo.endswith('.xlsx'):
        return pd.read_excel(ruta, sheet_name=hoja)
    elif nombre_archivo.endswith('.csv'):
        return pd.read_csv(ruta)
    else:
        raise ValueError("Formato no soportado")

def cargar_dataset_preprocessed(nombre_archivo, hoja=None):
    ruta = os.path.join(PREPROCESSED_PATH, nombre_archivo)
    if nombre_archivo.endswith('.xlsx'):
        return pd.read_excel(ruta, sheet_name=hoja)
    elif nombre_archivo.endswith('.csv'):
        return pd.read_csv(ruta)
    else:
        raise ValueError("Formato no soportado")

def limpiar_nombres_columnas(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '').str.replace('-', '_')
    return df

def limpiar_datos_vacios(df):
    # Reemplaza valores vacíos o NaN en columnas numéricas por 0
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(0)
    return df

def estandarizar_provincias(df, col='provincia'):
    df[col] = (
        df[col].astype(str)
        .str.strip()
        .str.upper()
        .apply(lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8'))
    )
    return df

def eliminar_totales(df, col='provincia'):
    return df[~df[col].str.contains('total', case=False, na=False)]

def calcular_tasa(df, eventos_col, poblacion_col, nueva_col='tasa_100mil'):
    df[nueva_col] = (df[eventos_col] / df[poblacion_col]) * 100000
    return df

def guardar_dataset(df, nombre_archivo):
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    df.to_csv(os.path.join(PROCESSED_PATH, nombre_archivo), index=False)
