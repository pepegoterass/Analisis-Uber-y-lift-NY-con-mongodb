# 🚕 Análisis de Movilidad Urbana NYC - HVFHV Data 2025

Proyecto académico de análisis de datos de viajes HVFHV (High Volume For-Hire Vehicle) de Nueva York utilizando MongoDB como base de datos NoSQL.

## 📋 Descripción del Proyecto

Este proyecto implementa un pipeline completo ETL (Extract, Transform, Load) para analizar millones de viajes de plataformas como Uber y Lyft en Nueva York durante el primer semestre de 2025. El análisis se realiza utilizando **MongoDB** para almacenamiento y consultas, y **Python** para procesamiento y visualización.

### 🎯 Objetivos

1. Construir un pipeline ETL robusto: Parquet → Python → MongoDB
2. Diseñar una base de datos NoSQL optimizada con índices
3. Realizar análisis exploratorio de datos (EDA) de movilidad urbana
4. Generar insights accionables mediante aggregation pipelines
5. Crear visualizaciones profesionales para comunicar resultados

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **MongoDB Community Edition / Atlas**
- **Pandas** - Manipulación de datos
- **PyArrow** - Lectura de archivos Parquet
- **PyMongo** - Conexión con MongoDB
- **Matplotlib & Seaborn** - Visualización de datos
- **Jupyter Notebook** - Análisis interactivo

## 📁 Estructura del Proyecto

```
practica/
│
├── data/                           # Archivos Parquet HVFHV (no incluidos en repo)
│   ├── fhvhv_tripdata_2025-01.parquet
│   ├── fhvhv_tripdata_2025-02.parquet
│   └── ...
│
├── outputs/                        # Visualizaciones generadas
│   ├── trips_by_hour.png
│   ├── top_pickup_zones.png
│   ├── trips_by_weekday.png
│   └── dashboard_metricas.png
│
├── report/                         # Informe técnico final
│
├── HVFHV_MongoDB_Analysis.ipynb    # Notebook principal del análisis
├── requirements.txt                # Dependencias Python
├── README.md                       # Este archivo
└── practica_mongodb.log            # Log de ejecución
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio o crear carpeta del proyecto

```bash
cd practica
```

### 2. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 3. Instalar MongoDB

**Opción A: MongoDB Community Edition (Local)**
- Descargar desde: https://www.mongodb.com/try/download/community
- Seguir instrucciones de instalación según tu sistema operativo

**Opción B: MongoDB Atlas (Cloud - Gratis)**
- Crear cuenta en: https://www.mongodb.com/cloud/atlas
- Crear un cluster gratuito
- Obtener URI de conexión

### 4. Descargar datos HVFHV

1. Ir a [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
2. Descargar archivos Parquet de **High Volume For-Hire Vehicle (HVFHV)** para 2025:
   - `fhvhv_tripdata_2025-01.parquet`
   - `fhvhv_tripdata_2025-02.parquet`
   - `fhvhv_tripdata_2025-03.parquet`
   - `fhvhv_tripdata_2025-04.parquet`
   - `fhvhv_tripdata_2025-05.parquet`
   - `fhvhv_tripdata_2025-06.parquet`
3. Colocar archivos en la carpeta `./data/`

### 5. Configurar conexión a MongoDB

Abrir el notebook `HVFHV_MongoDB_Analysis.ipynb` y ajustar:

```python
# MongoDB Local
MONGO_URI = "mongodb://localhost:27017/"

# MongoDB Atlas (ejemplo)
# MONGO_URI = "mongodb+srv://usuario:password@cluster.mongodb.net/"
```

## 📊 Uso del Notebook

### Ejecución paso a paso

1. **Abrir Jupyter Notebook:**
   ```bash
   jupyter notebook HVFHV_MongoDB_Analysis.ipynb
   ```

2. **Ejecutar celdas secuencialmente:**
   - Sección 1: Configuración del entorno
   - Sección 2: Ingesta de datos Parquet
   - Sección 3: Limpieza y transformación
   - Sección 4: Carga a MongoDB
   - Sección 5: Consultas y análisis
   - Sección 6: Dashboard de métricas
   - Sección 7: Conclusiones

3. **Opciones de carga de datos:**
   - **Muestra rápida:** Insertar solo 50K filas para pruebas
   - **Carga completa:** Insertar todos los archivos Parquet (6 meses)

## 🔍 Consultas Implementadas

El notebook incluye las siguientes consultas con **MongoDB Aggregation Pipelines**:

1. 🕐 **Viajes por hora del día** - Identificar horas pico
2. 📍 **Top 10 zonas de recogida** - Zonas más activas
3. 📅 **Viajes por día de la semana** - Patrones semanales
4. ⏱️ **Estadísticas de duración** - Promedio, mín, máx
5. 📈 **Distribución de duraciones** - Histograma
6. 🚖 **Análisis por plataforma** - Market share Uber vs Lyft
7. 📊 **Dashboard de métricas clave** - Resumen visual

## 📈 Visualizaciones Generadas

Todas las visualizaciones se guardan automáticamente en `./outputs/`:

- `trips_by_hour.png` - Distribución horaria de viajes
- `top_pickup_zones.png` - Top 10 zonas de demanda
- `trips_by_weekday.png` - Patrón semanal
- `duration_distribution.png` - Histograma de duraciones
- `platform_analysis.png` - Comparativa Uber/Lyft
- `dashboard_metricas.png` - Dashboard completo

## 🎓 Criterios de Evaluación Cumplidos

- ✅ **Código modular y profesional** con funciones reutilizables
- ✅ **Logging estructurado** para debugging y monitoreo
- ✅ **Rutas relativas** (no absolutas)
- ✅ **Manejo de errores** con try/except
- ✅ **Consultas optimizadas** con aggregation pipelines
- ✅ **Índices en MongoDB** para rendimiento
- ✅ **Visualizaciones claras** e interpretables
- ✅ **Documentación completa** paso a paso

## 🧹 Limpieza de Datos Aplicada

1. Conversión de timestamps a formato datetime
2. Filtrado de viajes con duración <= 0 o > 4 horas
3. Eliminación de distancias negativas o extremas (>200 mi)
4. Remoción de valores nulos en campos críticos
5. Feature engineering: hora del día, día de semana

## 💡 Insights Principales

### Patrones Temporales
- Horas pico: 7-9 AM y 5-7 PM (horarios laborales)
- Mayor actividad en días laborales vs fines de semana
- Duración promedio: 10-20 minutos

### Patrones Geográficos
- Manhattan concentra >50% de recogidas
- Aeropuertos (JFK, LGA, EWR) son zonas críticas
- Flujos desde zonas residenciales hacia centros de negocio

### Comportamiento por Plataforma
- Uber domina con >60% market share
- Lyft con ~30-35% de participación
- Pequeñas diferencias en duración/distancia promedio

## 🔧 Troubleshooting

### Error: "No module named 'pymongo'"
```bash
pip install pymongo
```

### Error: "Connection refused to MongoDB"
- Verificar que MongoDB esté ejecutándose: `mongod`
- Revisar URI de conexión en el notebook

### Error: "FileNotFoundError: [Errno 2] No such file"
- Asegurar que los archivos Parquet estén en `./data/`
- Verificar nombres de archivos correctos

### Notebook muy lento
- Reducir muestra de datos: `sample_rows=10000`
- Insertar solo 1-2 archivos para pruebas

## 📚 Referencias

- [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [MongoDB Aggregation Pipeline](https://docs.mongodb.com/manual/core/aggregation-pipeline/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)

## 👨‍💻 Autor

**Proyecto Académico:** Bases de Datos NoSQL  
**Universidad:** Master en Big Data  
**Fecha:** Noviembre 2025  

## 📄 Licencia

Proyecto académico con fines educativos.

---

**🎉 ¡Proyecto completado exitosamente!**
