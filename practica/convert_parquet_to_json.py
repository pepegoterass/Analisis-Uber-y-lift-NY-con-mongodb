#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para convertir archivos Parquet a JSON (OPCIONAL)
NO ES NECESARIO para el proyecto - el notebook ya hace la conversión directa.

Uso:
    python convert_parquet_to_json.py
"""

import pandas as pd
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_parquet_to_json(parquet_file, output_dir='./data', sample_rows=None):
    """
    Convierte un archivo Parquet a JSON (NDJSON format).
    
    Args:
        parquet_file (Path): Ruta al archivo Parquet
        output_dir (str): Directorio de salida
        sample_rows (int, optional): Número de filas a exportar (None = todas)
    
    Returns:
        Path: Ruta al archivo JSON generado
    """
    try:
        logger.info(f"🔄 Procesando: {parquet_file.name}")
        
        # Leer Parquet
        df = pd.read_parquet(parquet_file, engine='pyarrow')
        total_rows = len(df)
        logger.info(f"   📊 Total de filas en Parquet: {total_rows:,}")
        
        # Limitar filas si se especifica
        if sample_rows and sample_rows < total_rows:
            df = df.head(sample_rows)
            logger.info(f"   ✂️  Exportando solo {sample_rows:,} filas")
        
        # Convertir columnas datetime a string (requerido para JSON)
        datetime_cols = df.select_dtypes(include=['datetime64']).columns
        for col in datetime_cols:
            df[col] = df[col].astype(str)
            logger.info(f"   ✓ Convertido {col} a string")
        
        # Definir archivo de salida
        output_file = Path(output_dir) / f"{parquet_file.stem}.json"
        
        # Exportar a JSON (NDJSON - newline delimited JSON)
        # orient='records' → Cada fila es un objeto JSON
        # lines=True → Cada objeto en una línea (formato para mongoimport)
        df.to_json(output_file, orient='records', lines=True, date_format='iso')
        
        # Información del archivo generado
        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        logger.info(f"✅ JSON generado: {output_file.name}")
        logger.info(f"   💾 Tamaño: {file_size_mb:.2f} MB")
        logger.info(f"   📄 Registros: {len(df):,}")
        
        return output_file
    
    except Exception as e:
        logger.error(f"❌ Error al convertir {parquet_file.name}: {str(e)}")
        raise


def convert_all_parquet_files(data_dir='./data', sample_rows=None):
    """
    Convierte todos los archivos Parquet en un directorio a JSON.
    
    Args:
        data_dir (str): Directorio que contiene archivos Parquet
        sample_rows (int, optional): Número de filas por archivo
    
    Returns:
        list: Lista de archivos JSON generados
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.error(f"❌ El directorio {data_dir} no existe")
        return []
    
    # Buscar archivos Parquet
    parquet_files = list(data_path.glob('*.parquet'))
    
    if not parquet_files:
        logger.warning(f"⚠️  No se encontraron archivos .parquet en {data_dir}")
        return []
    
    logger.info(f"📂 Encontrados {len(parquet_files)} archivos Parquet")
    logger.info("="*80)
    
    json_files = []
    
    for idx, parquet_file in enumerate(parquet_files, 1):
        logger.info(f"\n[{idx}/{len(parquet_files)}] Procesando archivo...")
        
        try:
            json_file = convert_parquet_to_json(parquet_file, data_dir, sample_rows)
            json_files.append(json_file)
        except Exception as e:
            logger.error(f"⚠️  Saltando {parquet_file.name} debido a error")
            continue
    
    logger.info("\n" + "="*80)
    logger.info(f"🎉 Conversión completada: {len(json_files)}/{len(parquet_files)} archivos")
    
    return json_files


def import_to_mongodb_instructions(json_files, db_name='nyc_hvfhv_db', collection_name='trips'):
    """
    Muestra las instrucciones para importar JSON a MongoDB usando mongoimport.
    
    Args:
        json_files (list): Lista de archivos JSON
        db_name (str): Nombre de la base de datos
        collection_name (str): Nombre de la colección
    """
    if not json_files:
        return
    
    print("\n" + "="*80)
    print("📋 INSTRUCCIONES PARA IMPORTAR A MONGODB")
    print("="*80)
    print("\nEjecutar estos comandos en PowerShell:\n")
    
    for json_file in json_files:
        print(f"# Importar {json_file.name}")
        print(f'mongoimport --uri "mongodb://localhost:27017/" `')
        print(f'            --db {db_name} `')
        print(f'            --collection {collection_name} `')
        print(f'            --file "{json_file}" `')
        print(f'            --jsonArray')
        print()
    
    print("="*80)
    print("⚠️  NOTA: Este método es MENOS EFICIENTE que usar el notebook.")
    print("💡 RECOMENDACIÓN: Usa el notebook HVFHV_MongoDB_Analysis.ipynb")
    print("="*80)


if __name__ == "__main__":
    print("🔄 CONVERTIDOR PARQUET → JSON PARA MONGODB")
    print("="*80)
    print("⚠️  ADVERTENCIA: Este script NO es necesario para el proyecto.")
    print("💡 El notebook ya convierte Parquet → MongoDB directamente.")
    print("="*80)
    print()
    
    # Configuración
    DATA_DIR = './data'
    SAMPLE_ROWS = None  # None = exportar todas las filas
    # SAMPLE_ROWS = 10000  # Descomentar para exportar solo 10K filas
    
    # Convertir archivos
    json_files = convert_all_parquet_files(DATA_DIR, sample_rows=SAMPLE_ROWS)
    
    # Mostrar instrucciones de importación
    if json_files:
        import_to_mongodb_instructions(json_files)
