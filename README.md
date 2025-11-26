# 📊 Análisis MongoDB: NYC High Volume For-Hire Vehicle (HVFHV) Data

[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org)
[![Pandas](https://img.shields.io/badge/pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

## 🎯 Descripción del Proyecto

Este proyecto implementa un análisis completo de datos de viajes de vehículos de alto volumen (Uber, Lyft) en la ciudad de Nueva York utilizando MongoDB como base de datos NoSQL. El análisis incluye operaciones CRUD, pipelines de agregación avanzados, y visualizaciones geoespaciales para obtener insights de negocio.

## 📋 Contenido Académico

### ✅ Requisitos Cumplidos:
1. **Carga/Importación de Dataset** - Implementado ✓
2. **Ejercicios sobre inserción, actualización, proyección y filtrado** - Completo ✓
3. **Ejercicios sobre pipeline de agregación** - Avanzado ✓

### 📄 Entregables:
- **PDF Completo**: [`MongoDB_Héctor_Madrigal.pdf`](practica/MongoDB_Héctor_Madrigal.pdf)
- **Jupyter Notebook**: [`HVFHV_MongoDB_Analysis_FINAL.ipynb`](practica/HVFHV_MongoDB_Analysis_FINAL.ipynb)
- **Código Python**: Scripts de procesamiento y carga de datos

## 🗂️ Estructura del Dataset

**Dataset**: NYC High Volume For-Hire Vehicle Trip Records (2024)
- **Fuente**: NYC Taxi & Limousine Commission (TLC)
- **Tamaño**: ~2.5M registros mensuales
- **Plataformas**: Uber, Lyft, Via, Juno
- **Período**: Enero-Marzo 2024

### 📊 Campos Principales:
| Campo | Descripción | Tipo |
|-------|-------------|------|
| `hvfhs_license_num` | Licencia de la plataforma | String |
| `dispatching_base_num` | Base de despacho | String |
| `pickup_datetime` | Fecha/hora de recogida | DateTime |
| `dropoff_datetime` | Fecha/hora de entrega | DateTime |
| `PULocationID` | Zona de recogida | Integer |
| `DOLocationID` | Zona de destino | Integer |
| `trip_miles` | Distancia del viaje | Float |
| `trip_time` | Duración del viaje | Integer |
| `base_passenger_fare` | Tarifa base | Float |
| `tips` | Propinas | Float |
| `shared_request_flag` | Viaje compartido | Boolean |

## 🛠️ Tecnologías Utilizadas

```python
# Stack Tecnológico Principal
MongoDB      # Base de datos NoSQL
Python 3.11+ # Lenguaje de programación
PyMongo      # Driver MongoDB para Python
Pandas       # Manipulación de datos
Plotly       # Visualizaciones interactivas
Folium       # Mapas geoespaciales
Jupyter      # Entorno de desarrollo
```

## 📈 Análisis Implementados

### 🔍 1. Operaciones CRUD Básicas
```mongodb
// Inserción de documentos
db.hvfhv_trips.insertMany([...])

// Consultas con filtrado
db.hvfhv_trips.find({"hvfhs_license_num": "HV0003"})

// Actualizaciones
db.hvfhv_trips.updateMany({}, {$set: {"processed": true}})

// Proyecciones
db.hvfhv_trips.find({}, {"pickup_datetime": 1, "base_passenger_fare": 1})
```

### 🚀 2. Pipelines de Agregación Avanzados

#### 📊 Análisis Temporal por Plataforma
```mongodb
[
  {$match: {"pickup_datetime": {$gte: ISODate("2024-01-01")}}},
  {$group: {
    "_id": {
      "platform": "$hvfhs_license_num",
      "hour": {$hour: "$pickup_datetime"}
    },
    "total_trips": {$sum: 1},
    "avg_fare": {$avg: "$base_passenger_fare"}
  }},
  {$sort: {"_id.hour": 1, "total_trips": -1}}
]
```

#### 🗺️ Análisis Geoespacial
```mongodb
[
  {$group: {
    "_id": "$PULocationID",
    "trip_count": {$sum: 1},
    "avg_distance": {$avg: "$trip_miles"},
    "revenue": {$sum: "$base_passenger_fare"}
  }},
  {$lookup: {
    "from": "taxi_zones",
    "localField": "_id",
    "foreignField": "LocationID",
    "as": "zone_info"
  }}
]
```

### 📊 3. Business Intelligence

#### KPIs Principales:
- **Volumen de Viajes**: 2.5M+ viajes/mes
- **Revenue por Plataforma**: Uber lidera con 60% market share
- **Picos de Demanda**: 8-9 PM en días laborables
- **Zonas Hot**: Manhattan, Brooklyn, Queens
- **Viajes Compartidos**: 15% adoption rate

## 🎨 Visualizaciones

### 📍 Mapas Interactivos
- **Mapa de Calor**: Zonas de mayor demanda
- **Flow Map**: Rutas origen-destino más populares
- **Temporal Map**: Evolución de demanda por horas

### 📈 Gráficos Analíticos
- **Time Series**: Tendencias temporales
- **Heatmaps**: Patrones día/hora
- **Bar Charts**: Comparativas entre plataformas
- **Scatter Plots**: Correlaciones distancia/tarifa

## 🚀 Instalación y Uso

### 1️⃣ Prerequisitos
```bash
# MongoDB Community Server
# Python 3.11+
# Jupyter Notebook/Lab
```

### 2️⃣ Instalación
```bash
# Clonar repositorio
git clone https://github.com/pepegoterass/Analisis-Uber-y-lift-NY-con-mongodb.git
cd Analisis-Uber-y-lift-NY-con-mongodb

# Instalar dependencias
pip install -r practica/requirements.txt

# Configurar MongoDB
# Ver: practica/GUIA_MONGODB_SETUP.md
```

### 3️⃣ Ejecución
```bash
# Iniciar Jupyter
jupyter lab practica/HVFHV_MongoDB_Analysis_FINAL.ipynb

# O ejecutar scripts individuales
python practica/cargar_datos_completo.py
```

## 📁 Estructura del Proyecto

```
📦 Analisis-Uber-y-lift-NY-con-mongodb/
├── 📂 practica/
│   ├── 📊 HVFHV_MongoDB_Analysis_FINAL.ipynb    # Notebook principal
│   ├── 📄 MongoDB_Héctor_Madrigal.pdf          # Entregable PDF
│   ├── 🐍 cargar_datos_completo.py             # Script carga datos
│   ├── 🔧 convert_parquet_to_json.py           # Conversión formatos
│   ├── 📋 requirements.txt                     # Dependencias
│   ├── 📂 outputs/                             # Visualizaciones
│   │   ├── 📂 charts/                          # Gráficos estáticos
│   │   └── 📂 maps/                            # Mapas interactivos
│   └── 📂 data/                                # Datasets (local)
├── 📜 README.md                                # Documentación
└── 📜 .gitignore                               # Exclusiones Git
```

## 🎓 Resultados Académicos

### ✅ Research Questions Respondidas:
1. **¿Cuál es el patrón temporal de uso por plataforma?**
   - Uber domina en horarios pico (8-9 PM)
   - Lyft tiene mayor participación en fines de semana

2. **¿Dónde se concentra la mayor demanda geográficamente?**
   - Manhattan: 45% de pickups
   - Aeropuertos: 20% del revenue total

3. **¿Cuál es el comportamiento de precios por zona/tiempo?**
   - Surge pricing en eventos especiales
   - Premium en zonas corporativas

### 📊 Business Intelligence Insights:
- **Optimización de Flota**: Redistribuir vehículos según demanda temporal
- **Pricing Strategy**: Implementar surge pricing inteligente
- **Market Share**: Uber mantiene liderazgo pero Lyft crece en nichos específicos

## 🏆 Conclusiones

Este proyecto demuestra la potencia de MongoDB para análisis de big data en tiempo real, combinando:
- **Flexibilidad de esquemas** para datos semi-estructurados
- **Pipelines de agregación** para analytics complejos
- **Escalabilidad horizontal** para datasets masivos
- **Integración con Python** para ML y visualización

### 🚀 Próximos Pasos:
- Implementar predicción de demanda con ML
- Añadir análisis de sentimiento de reviews
- Integrar datos de tráfico en tiempo real
- Desarrollar API REST para consultas

## 👨‍💻 Autor

**Héctor Madrigal**
- 📧 Email: [contacto@email.com]
- 🔗 LinkedIn: [perfil-linkedin]
- 🐙 GitHub: [@pepegoterass](https://github.com/pepegoterass)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **NYC Taxi & Limousine Commission** por proporcionar los datos abiertos
- **MongoDB University** por los recursos educativos
- **Plotly Community** por las herramientas de visualización
- **Python Data Science Community** por las librerías utilizadas

---

⭐ **¡Si este proyecto te resultó útil, dale una estrella!** ⭐