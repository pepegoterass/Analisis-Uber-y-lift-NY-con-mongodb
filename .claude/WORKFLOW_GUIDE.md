# Guía de workflow para Claude Sonnet 4.5

Claude debe seguir este flujo siempre que el usuario solicite generar código,
analizar datos, preparar pipelines o documentación.

---

## 1. Preparación del entorno
- Crear/validar entorno Python
- Configurar conexión a MongoDB
- Verificar que los archivos Parquet existen

## 2. Importación de Parquet → DataFrame
- Usar pandas + pyarrow
- Validar columnas, dtypes, nulls
- Reportar tamaños de memoria

## 3. Limpieza
- Normalizar timestamps
- Convertir coordenadas a números
- Filtrar outliers extremos (duración, distancia)
- Validar que las filas son consistentes

## 4. Insertar datos en MongoDB
- Lote (batch insert)
- Indexar: pickup_datetime, dropoff_datetime, PULocationID, DOLocationID

## 5. Consultas de ejemplo obligatorias
- Viajes por hora del día
- Duración promedio
- Distancia media
- Tarifas si aplican
- Viajes por borough (con lookup hacia NYC Taxi Zones)
- Heatmap de actividad con agregación por lat/lon binning (opcional)

## 6. Visualización
- Gráficos limpios (matplotlib o seaborn)
- Guardar en carpeta /outputs

## 7. Informe final
- Introducción
- Dataset description
- Pipeline de procesamiento
- Consultas + resultados
- Gráficos
- Conclusiones

---

Claude debe:
- Recordar el estado del proyecto
- Mantener modularidad
- Usar nombres de archivo claros
- Ofrecer siempre alternativas más eficientes
