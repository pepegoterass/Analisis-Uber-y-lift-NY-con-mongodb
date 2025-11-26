**Prompt 1**
Actúa como Senior Data Analyst especializado en Big Data y MongoDB.

Quiero que configures este proyecto desde cero.
Usa las reglas de los archivos .claude del proyecto.

Necesito:
1. estructura de carpetas
2. dependencias
3. scripts base (ingestión, limpieza, carga a MongoDB)
4. configuración de logging
5. archivos .env para la conexión a MongoDB

Responde generando los archivos completos con código listo para usar.

**Prompt 2**
Quiero que implementes la ingesta completa de archivos Parquet HVFHV (NYC TLC).
El objetivo es leerlos, validarlos y preparar DataFrames limpios.

Requisitos:
- Usar pandas + pyarrow
- Validar schema
- Detectar nulls
- Estimar memoria
- Reportar número de filas cargadas

Genera el archivo scripts/ingest.py siguiendo las reglas del proyecto.

**Prompt 3**
Actúa como Data Engineer senior.
Necesito un script clean.py que realice:

- normalización de datetime
- eliminación de viajes con duración <=0 o >4h
- distancias erróneas
- columnas obligatorias garantizadas
- conversión de tipos

Quiero el script completo, comentado y optimizado.

**Prompt 4**
Genera el archivo scripts/load_mongo.py.

Necesito:
- conexión a MongoDB (URI desde .env)
- inserciones por lotes (batch size 20k)
- índices optimizados:
    - pickup_datetime
    - dropoff_datetime
    - PULocationID
    - DOLocationID

Debes generar también un script opcional load_all.py que cargue todos los meses automáticamente.

**Prompt 5**
Crea el archivo queries.py con al menos 8 consultas MongoDB en aggregation pipeline:

1. Viajes por hora del día
2. Duración media del viaje
3. Distancia media del viaje
4. Actividad por borough (con NYC Taxi Zones)
5. Top 10 zonas con más demanda
6. Distribución de duraciones (histograma)
7. Viajes por día de la semana
8. Mapa de calor (lat/lon agregados por bins)

Incluye gráficos generados con matplotlib y guarda todo en /outputs.

**Prompt 6**
Quiero un informe final completo en Markdown que documente:

- Introducción
- Descripción del dataset HVFHV
- Arquitectura del proyecto
- Pipeline Parquet → Python → MongoDB
- Limpieza de datos
- Consultas realizadas
- Visualizaciones
- Conclusiones analíticas

El informe debe tener calidad de 10/10.

Guárdalo como /report/Informe_Final.md
