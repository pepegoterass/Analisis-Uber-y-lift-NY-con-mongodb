# -*- coding: utf-8 -*-
"""
SCRIPT COMPLETO: Carga de datos HVFHV a MongoDB
EJECUTAR DIRECTAMENTE CON: python cargar_datos_completo.py

Soluciona el error: NaTType does not support utcoffset
"""

import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import datetime as dt
from glob import glob
import os

# ==================== CONFIGURACIÓN ====================
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "nyc_hvfhv"
COLLECTION_NAME = "trips_2025"
BATCH_SIZE = 20000
SAMPLE_FRACTION = 0.025  # 2.5% de cada archivo

# Directorio con archivos Parquet
DATA_DIR = r"c:\Users\Usuario\Documents\master\mongodb\practica\data"

print("=" * 80)
print("🚀 CARGA DE DATOS NYC HVFHV A MONGODB")
print("=" * 80)

# ==================== FUNCIONES CORREGIDAS ====================

def normalize_datetimes(df, datetime_cols):
    """Normaliza columnas datetime para MongoDB: UTC naive sin NaT."""
    for col in datetime_cols:
        if col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                s = df[col]
                if hasattr(s.dtype, 'tz') and s.dtype.tz is not None:
                    s = s.dt.tz_convert('UTC').dt.tz_localize(None)
            else:
                s = pd.to_datetime(df[col], errors='coerce')
            df[col] = s.where(s.notna(), None)
    return df


def sanitize_for_mongo(df):
    """Sanitiza DataFrame para MongoDB - SOLUCIÓN BRUTAL."""
    df_clean = df.copy()
    
    numeric_time_fields = ['pickup_hour', 'pickup_day_of_week', 'pickup_month']
    
    # Normalizar columnas datetime
    datetime_cols = ['pickup_datetime', 'dropoff_datetime', 'request_datetime', 'on_scene_datetime']
    df_clean = normalize_datetimes(df_clean, datetime_cols)
    
    # Convertir datetime.date a STRING
    for col in df_clean.columns:
        if col not in numeric_time_fields and len(df_clean) > 0:
            first_valid = df_clean[col].dropna().iloc[0] if len(df_clean[col].dropna()) > 0 else None
            if first_valid is not None and isinstance(first_valid, dt.date) and not isinstance(first_valid, dt.datetime):
                df_clean[col] = df_clean[col].astype(str)
    
    # Convertir Int64 a int
    for col in df_clean.select_dtypes(include=['Int64']).columns:
        df_clean[col] = df_clean[col].fillna(0).astype(int)
    
    # BRUTAL: Convertir a diccionarios y limpiar NaT manualmente
    records = df_clean.to_dict('records')
    clean_records = []
    
    for record in records:
        clean_record = {}
        for key, value in record.items():
            if pd.isna(value):
                clean_record[key] = None
            elif isinstance(value, (np.integer, np.floating)):
                clean_record[key] = value.item()
            else:
                clean_record[key] = value
        clean_records.append(clean_record)
    
    return clean_records


def insert_data_to_mongodb(df, collection, batch_size=20000):
    """Inserta DataFrame a MongoDB en lotes."""
    try:
        records = sanitize_for_mongo(df)
        total_inserted = 0
        
        print(f"📦 Preparando {len(records):,} documentos para inserción...")
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            try:
                result = collection.insert_many(batch, ordered=False)
                total_inserted += len(result.inserted_ids)
                print(f"   ✓ Lote {i//batch_size + 1}: {len(result.inserted_ids)} documentos insertados")
            except BulkWriteError as e:
                inserted_count = e.details.get('nInserted', 0)
                total_inserted += inserted_count
                print(f"   ⚠️  Lote {i//batch_size + 1}: {inserted_count} insertados, {len(e.details.get('writeErrors', []))} errores")
            except Exception as e:
                print(f"   ❌ Lote {i//batch_size + 1}: Error - {str(e)[:100]}")
        
        print(f"✅ Total insertado: {total_inserted:,} documentos")
        return total_inserted
    
    except Exception as e:
        print(f"❌ Error en inserción: {str(e)}")
        raise


def clean_hvfhv_data(df):
    """Limpia y prepara datos HVFHV."""
    print("🧹 Limpiando datos...")
    
    # Convertir columnas datetime
    datetime_cols = ['pickup_datetime', 'dropoff_datetime', 'request_datetime', 'on_scene_datetime']
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Calcular duración del viaje
    df['trip_duration_minutes'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds() / 60
    
    # Filtrar valores extremos
    df = df[
        (df['trip_duration_minutes'] > 0) & 
        (df['trip_duration_minutes'] <= 300) &  # Menos de 5 horas
        (df['trip_miles'] > 0) & 
        (df['trip_miles'] <= 100)
    ]
    
    # Crear columnas temporales
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['pickup_day_name'] = df['pickup_datetime'].dt.day_name()
    df['pickup_month'] = df['pickup_datetime'].dt.month
    df['pickup_date'] = df['pickup_datetime'].dt.date
    
    print(f"✅ Datos limpios: {len(df):,} filas")
    return df


# ==================== CONEXIÓN A MONGODB ====================
print("\n🔌 Conectando a MongoDB...")
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    print("✅ Conexión exitosa a MongoDB")
    
    mongo_db = mongo_client[DATABASE_NAME]
    collection = mongo_db[COLLECTION_NAME]
    
    # Limpiar colección
    doc_count = collection.count_documents({})
    if doc_count > 0:
        print(f"\n🗑️  Limpiando colección existente ({doc_count:,} documentos)...")
        collection.delete_many({})
        print("✅ Colección limpiada")
    
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    exit(1)

# ==================== BUSCAR ARCHIVOS PARQUET ====================
print(f"\n📂 Buscando archivos en: {DATA_DIR}")
parquet_files = sorted(glob(os.path.join(DATA_DIR, "fhvhv_tripdata_2025-*.parquet")))

if not parquet_files:
    print(f"❌ No se encontraron archivos Parquet en {DATA_DIR}")
    exit(1)

print(f"✅ Encontrados {len(parquet_files)} archivos:")
for f in parquet_files:
    print(f"   - {os.path.basename(f)}")

# ==================== CARGAR ARCHIVOS ====================
print("\n" + "=" * 80)
print("📥 INICIANDO CARGA DE ARCHIVOS")
print("=" * 80)

total_docs_inserted = 0

for idx, file_path in enumerate(parquet_files, 1):
    filename = os.path.basename(file_path)
    print(f"\n{'=' * 80}")
    print(f"📄 [{idx}/{len(parquet_files)}] Procesando: {filename}")
    print(f"{'=' * 80}")
    
    try:
        # Leer archivo con muestreo
        print(f"📖 Leyendo archivo (muestra: {SAMPLE_FRACTION*100}%)...")
        parquet_file = pq.ParquetFile(file_path)
        total_rows = parquet_file.metadata.num_rows
        
        # Muestreo sistemático
        skip = int(1 / SAMPLE_FRACTION)
        row_indices = list(range(0, total_rows, skip))
        
        df = parquet_file.read(columns=None).to_pandas()
        df_sampled = df.iloc[row_indices].reset_index(drop=True)
        
        print(f"   Total filas: {total_rows:,}")
        print(f"   Filas muestreadas: {len(df_sampled):,}")
        
        # Limpiar datos
        df_clean = clean_hvfhv_data(df_sampled)
        
        # Insertar a MongoDB
        print(f"💾 Insertando a MongoDB...")
        inserted = insert_data_to_mongodb(df_clean, collection, BATCH_SIZE)
        total_docs_inserted += inserted
        
        print(f"✅ Archivo completado: {inserted:,} documentos insertados")
        
    except Exception as e:
        print(f"❌ ERROR procesando {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        continue

# ==================== RESUMEN FINAL ====================
print("\n" + "=" * 80)
print("🎉 PROCESO COMPLETADO")
print("=" * 80)
print(f"Total documentos insertados: {total_docs_inserted:,}")
print(f"Total documentos en MongoDB: {collection.count_documents({}):,}")
print("\n✅ Datos listos para análisis en MongoDB Compass o agregaciones")
