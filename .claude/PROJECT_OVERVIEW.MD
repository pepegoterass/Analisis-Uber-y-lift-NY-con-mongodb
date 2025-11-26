# Proyecto: Análisis de datos de movilidad (Uber/Lyft HVFHV – NYC TLC 2025)

## Objetivo académico:
Construir una base de datos MongoDB desde archivos Parquet de viajes HVFHV
analizar los datos, generar resultados estadísticos avanzados y producir un
informe técnico de calidad máxima para obtener una calificación de 10/10.

## Dataset:
- High Volume For-Hire Vehicle (HVFHV) – NYC TLC
- Archivos mensuales en formato Parquet (ej: fhvhv_tripdata_2025-01.parquet)
- Contienen datos de Uber, Lyft y otras plataformas FHV de alto volumen

## Infraestructura:
- Python 3.11+
- MongoDB Community o Atlas
- Librerías: pandas, pyarrow, pymongo, fastparquet, matplotlib, seaborn
- VS Code + Claude Sonnet 4.5 (extensión oficial) + Copilot Agent

## Requisitos de la práctica:
1. Cargar dataset de Parquet → Python → MongoDB
2. Crear colecciones adecuadas y limpieza mínima de datos
3. Diseñar consultas en MongoDB (aggregation pipeline)
4. Obtener insights sobre movilidad:
    - horas pico
    - zonas más activas
    - duración y distancia promedio
    - ingresos aproximados
    - mapas o heatmaps (si aplica)
5. Crear un informe final bien estructurado

## Estándares:
- Código modular y profesional
- Consultas en MongoDB optimizadas
- Documentación clara para cada paso
- Resultados visuales interpretables
- Respuestas de Claude deben ser concretas y siempre en contexto del proyecto

## Claude: estilo de colaboración
- Proponer siempre mejoras y optimización
- Aportar análisis experto
- No repetir contenido innecesario
- Mantener el contexto técnico del proyecto
