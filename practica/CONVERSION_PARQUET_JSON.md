# 🔄 Conversión Parquet a JSON para MongoDB

## RESPUESTA RÁPIDA: NO ES NECESARIO

El notebook **ya convierte automáticamente** Parquet → MongoDB usando PyMongo.

**Flujo actual:**
```
Parquet → Pandas → dict() → MongoDB (BSON)
```

**NO necesitas** archivos JSON intermedios.

---

## Métodos de Importación a MongoDB

### MÉTODO 1: PyMongo (YA IMPLEMENTADO EN EL NOTEBOOK) ✅

**Ventajas:**
- ✅ Conversión automática Parquet → MongoDB
- ✅ Control total sobre limpieza de datos
- ✅ Inserción por lotes optimizada (20K documentos/batch)
- ✅ Logging y manejo de errores
- ✅ **No requiere archivos intermedios**

**Código (ya está en el notebook):**
```python
# Leer Parquet
df = pd.read_parquet('archivo.parquet')

# Limpiar
df_clean = clean_hvfhv_data(df)

# Convertir a diccionarios e insertar
records = df_clean.to_dict('records')
collection.insert_many(records, ordered=False)
```

---

### MÉTODO 2: mongoimport (Alternativa Manual)

Si prefieres usar la herramienta CLI de MongoDB:

**Paso 1: Convertir Parquet a JSON**

```python
import pandas as pd

# Leer Parquet
df = pd.read_parquet('fhvhv_tripdata_2025-01.parquet')

# Exportar a JSON (formato NDJSON para mongoimport)
df.to_json('output.json', orient='records', lines=True)
```

**Paso 2: Importar con mongoimport**

```powershell
mongoimport --uri "mongodb://localhost:27017/" `
            --db nyc_hvfhv_db `
            --collection trips `
            --file output.json `
            --jsonArray
```

**Desventajas:**
- ❌ Archivos JSON muy grandes (2-3x el tamaño de Parquet)
- ❌ Sin limpieza de datos automática
- ❌ Proceso en 2 pasos (lento)
- ❌ Sin control de errores detallado

---

## MÉTODO RECOMENDADO: Usar el Notebook

**Razones:**

1. **Sin archivos intermedios** → Ahorra espacio en disco
2. **Limpieza automática** → Datos ya validados
3. **Logging detallado** → Sabes qué pasó
4. **Batch insert** → Más rápido que mongoimport
5. **Índices automáticos** → Ya optimizado

---

## Comparación de Rendimiento

| Método | Tiempo (1M docs) | Espacio en Disco | Limpieza | Índices |
|--------|------------------|------------------|----------|---------|
| **PyMongo (Notebook)** | ~5 min | Solo Parquet | ✅ Sí | ✅ Auto |
| mongoimport + JSON | ~15 min | Parquet + JSON (3x) | ❌ No | ❌ Manual |

---

## Si AÚN Quieres Exportar a JSON

**Script standalone:**

```python
# convert_parquet_to_json.py
import pandas as pd
from pathlib import Path

def convert_all_parquet_to_json():
    data_path = Path('./data')
    parquet_files = list(data_path.glob('*.parquet'))
    
    for parquet_file in parquet_files:
        print(f"🔄 Convirtiendo {parquet_file.name}...")
        
        # Leer Parquet
        df = pd.read_parquet(parquet_file)
        
        # Convertir datetime a string
        for col in df.select_dtypes(include=['datetime64']).columns:
            df[col] = df[col].astype(str)
        
        # Exportar a JSON (NDJSON format)
        output_file = data_path / f"{parquet_file.stem}.json"
        df.to_json(output_file, orient='records', lines=True)
        
        print(f"✅ Guardado: {output_file.name}")

if __name__ == "__main__":
    convert_all_parquet_to_json()
```

**Ejecutar:**
```powershell
python convert_parquet_to_json.py
```

---

## Conclusión

**USA EL NOTEBOOK** → Es más eficiente, rápido y profesional.

La conversión Parquet → JSON → MongoDB solo tiene sentido si:
- Quieres archivos JSON para otro propósito
- Estás usando una herramienta que solo acepta JSON
- Necesitas compartir los datos en formato JSON

Para este proyecto académico, **el notebook ya tiene todo optimizado**.
