# -*- coding: utf-8 -*-
"""
SOLUCIÓN DEFINITIVA AL ERROR: NaTType does not support utcoffset
Ejecuta este script en el notebook con: %run fix_nat_error.py
"""

import pandas as pd
import numpy as np
import datetime as dt

print("🔧 Cargando funciones corregidas...")

def normalize_datetimes(df, datetime_cols):
    """
    Normaliza columnas datetime para MongoDB: UTC naive sin NaT.
    """
    for col in datetime_cols:
        if col in df.columns:
            # Si ya es datetime, trabajar directamente
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                s = df[col]
                # Si tiene timezone, convertir a UTC naive
                if hasattr(s.dtype, 'tz') and s.dtype.tz is not None:
                    s = s.dt.tz_convert('UTC').dt.tz_localize(None)
            else:
                # Convertir a datetime si no lo es
                s = pd.to_datetime(df[col], errors='coerce')
            
            # Reemplazar NaT por None
            df[col] = s.where(s.notna(), None)
    
    return df


def sanitize_for_mongo(df):
    """
    Sanitiza DataFrame para MongoDB - SOLUCIÓN BRUTAL.
    Convierte a diccionarios y elimina NaT manualmente.
    """
    df_clean = df.copy()
    
    # Campos numéricos que NO tocar
    numeric_time_fields = ['pickup_hour', 'pickup_day_of_week', 'pickup_month']
    
    # 1) Normalizar columnas datetime principales
    datetime_cols = ['pickup_datetime', 'dropoff_datetime', 'request_datetime', 'on_scene_datetime']
    df_clean = normalize_datetimes(df_clean, datetime_cols)
    
    # 2) Convertir datetime.date a STRING
    for col in df_clean.columns:
        if col not in numeric_time_fields and len(df_clean) > 0:
            first_valid = df_clean[col].dropna().iloc[0] if len(df_clean[col].dropna()) > 0 else None
            if first_valid is not None and isinstance(first_valid, dt.date) and not isinstance(first_valid, dt.datetime):
                df_clean[col] = df_clean[col].astype(str)
    
    # 3) Convertir Int64 a int
    for col in df_clean.select_dtypes(include=['Int64']).columns:
        df_clean[col] = df_clean[col].fillna(0).astype(int)
    
    # 4) BRUTAL: Convertir a diccionarios y limpiar NaT manualmente
    records = df_clean.to_dict('records')
    clean_records = []
    
    for record in records:
        clean_record = {}
        for key, value in record.items():
            # Eliminar NaT/NaN de cualquier tipo
            if pd.isna(value):
                clean_record[key] = None
            # Convertir numpy types a Python types
            elif isinstance(value, (np.integer, np.floating)):
                clean_record[key] = value.item()
            else:
                clean_record[key] = value
        clean_records.append(clean_record)
    
    return clean_records  # Retorna lista de diccionarios


def insert_data_to_mongodb(df, collection, batch_size=20000):
    """
    Inserta DataFrame a MongoDB en lotes.
    Trabaja con lista de diccionarios de sanitize_for_mongo().
    """
    from pymongo.errors import BulkWriteError
    
    try:
        # Sanitizar datos (retorna lista de diccionarios)
        records = sanitize_for_mongo(df)
        total_inserted = 0
        
        print(f"📦 Preparando {len(records):,} documentos para inserción...")
        
        # Insertar en lotes
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


print("✅ Funciones cargadas exitosamente:")
print("   - normalize_datetimes()")
print("   - sanitize_for_mongo()")
print("   - insert_data_to_mongodb()")
print("\n🚀 Ahora ejecuta la celda de carga de archivos (celda 24)")
