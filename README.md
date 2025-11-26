# 📊 MongoDB Analysis: NYC High Volume For-Hire Vehicle (HVFHV) Data

[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)](https://jupyter.org)
[![Pandas](https://img.shields.io/badge/pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

## 🎯 Project Description

This project implements a comprehensive analysis of high-volume vehicle trip data (Uber, Lyft) in New York City using MongoDB as a NoSQL database. The analysis includes CRUD operations, advanced aggregation pipelines, and geospatial visualizations to derive business insights.

## 📋 Academic Content

### ✅ Requirements Fulfilled:
1. **Dataset Loading/Import** - Implemented ✓
2. **Insertion, Update, Projection and Filtering Exercises** - Complete ✓
3. **Aggregation Pipeline Exercises** - Advanced ✓

### 📄 Deliverables:
- **Complete PDF**: [`MongoDB_Héctor_Madrigal.pdf`](practica/MongoDB_Héctor_Madrigal.pdf)
- **Jupyter Notebook**: [`HVFHV_MongoDB_Analysis_FINAL.ipynb`](practica/HVFHV_MongoDB_Analysis_FINAL.ipynb)
- **Python Code**: Data processing and loading scripts

## 🗂️ Dataset Structure

**Dataset**: NYC High Volume For-Hire Vehicle Trip Records (2024)
- **Source**: NYC Taxi & Limousine Commission (TLC)
- **Size**: ~2.5M monthly records
- **Platforms**: Uber, Lyft, Via, Juno
- **Period**: January-March 2024

### 📊 Main Fields:
| Field | Description | Type |
|-------|-------------|------|
| `hvfhs_license_num` | Platform license | String |
| `dispatching_base_num` | Dispatching base | String |
| `pickup_datetime` | Pickup date/time | DateTime |
| `dropoff_datetime` | Dropoff date/time | DateTime |
| `PULocationID` | Pickup location zone | Integer |
| `DOLocationID` | Dropoff location zone | Integer |
| `trip_miles` | Trip distance | Float |
| `trip_time` | Trip duration | Integer |
| `base_passenger_fare` | Base fare | Float |
| `tips` | Tips amount | Float |
| `shared_request_flag` | Shared ride flag | Boolean |

## 🛠️ Technologies Used

```python
# Main Technology Stack
MongoDB      # NoSQL Database
Python 3.11+ # Programming Language
PyMongo      # MongoDB Driver for Python
Pandas       # Data Manipulation
Plotly       # Interactive Visualizations
Folium       # Geospatial Maps
Jupyter      # Development Environment
```

## 📈 Implemented Analysis

### 🔍 1. Basic CRUD Operations
```mongodb
// Document insertion
db.hvfhv_trips.insertMany([...])

// Queries with filtering
db.hvfhv_trips.find({"hvfhs_license_num": "HV0003"})

// Updates
db.hvfhv_trips.updateMany({}, {$set: {"processed": true}})

// Projections
db.hvfhv_trips.find({}, {"pickup_datetime": 1, "base_passenger_fare": 1})
```

### 🚀 2. Advanced Aggregation Pipelines

#### 📊 Temporal Analysis by Platform
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

#### 🗺️ Geospatial Analysis
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

#### Key KPIs:
- **Trip Volume**: 2.5M+ trips/month
- **Revenue by Platform**: Uber leads with 60% market share
- **Demand Peaks**: 8-9 PM on weekdays
- **Hot Zones**: Manhattan, Brooklyn, Queens
- **Shared Rides**: 15% adoption rate

## 🎨 Visualizations

### 📍 Interactive Maps
- **Heat Map**: High-demand zones
- **Flow Map**: Most popular origin-destination routes
- **Temporal Map**: Demand evolution by hours

### 📈 Analytical Charts
- **Time Series**: Temporal trends
- **Heatmaps**: Day/hour patterns
- **Bar Charts**: Platform comparisons
- **Scatter Plots**: Distance/fare correlations

## 🚀 Installation and Usage

### 1️⃣ Prerequisites
```bash
# MongoDB Community Server
# Python 3.11+
# Jupyter Notebook/Lab
```

### 2️⃣ Installation
```bash
# Clone repository
git clone https://github.com/pepegoterass/Analisis-Uber-y-lift-NY-con-mongodb.git
cd Analisis-Uber-y-lift-NY-con-mongodb

# Install dependencies
pip install -r practica/requirements.txt

# Configure MongoDB
# See: practica/GUIA_MONGODB_SETUP.md
```

### 3️⃣ Execution
```bash
# Start Jupyter
jupyter lab practica/HVFHV_MongoDB_Analysis_FINAL.ipynb

# Or run individual scripts
python practica/cargar_datos_completo.py
```

## 📁 Project Structure

```
📦 Analisis-Uber-y-lift-NY-con-mongodb/
├── 📂 practica/
│   ├── 📊 HVFHV_MongoDB_Analysis_FINAL.ipynb    # Main notebook
│   ├── 📄 MongoDB_Héctor_Madrigal.pdf          # PDF deliverable
│   ├── 🐍 cargar_datos_completo.py             # Data loading script
│   ├── 🔧 convert_parquet_to_json.py           # Format conversion
│   ├── 📋 requirements.txt                     # Dependencies
│   ├── 📂 outputs/                             # Visualizations
│   │   ├── 📂 charts/                          # Static charts
│   │   └── 📂 maps/                            # Interactive maps
│   └── 📂 data/                                # Datasets (local)
├── 📜 README.md                                # Documentation
└── 📜 .gitignore                               # Git exclusions
```

## 🎓 Academic Results

### ✅ Research Questions Answered:
1. **What is the temporal usage pattern by platform?**
   - Uber dominates during peak hours (8-9 PM)
   - Lyft has higher participation on weekends

2. **Where is the highest demand geographically concentrated?**
   - Manhattan: 45% of pickups
   - Airports: 20% of total revenue

3. **What is the pricing behavior by zone/time?**
   - Surge pricing during special events
   - Premium rates in corporate zones

### 📊 Business Intelligence Insights:
- **Fleet Optimization**: Redistribute vehicles according to temporal demand
- **Pricing Strategy**: Implement intelligent surge pricing
- **Market Share**: Uber maintains leadership but Lyft grows in specific niches

## 🏆 Conclusions

This project demonstrates MongoDB's power for real-time big data analysis, combining:
- **Schema flexibility** for semi-structured data
- **Aggregation pipelines** for complex analytics
- **Horizontal scalability** for massive datasets
- **Python integration** for ML and visualization

### 🚀 Next Steps:
- Implement demand prediction with ML
- Add sentiment analysis of reviews
- Integrate real-time traffic data
- Develop REST API for queries

## 👨‍💻 Author

**Héctor Madrigal**
- 📧 Email: [hector.madrigal.contacto@gmail.com]
- 🔗 LinkedIn: [www.linkedin.com/in/héctor-madrigal-4286ba330]
- 🐙 GitHub: [@pepegoterass](https://github.com/pepegoterass)

## 📄 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NYC Taxi & Limousine Commission** for providing open data
- **MongoDB University** for educational resources
- **Plotly Community** for visualization tools
- **Python Data Science Community** for the libraries used

---

⭐ **¡Si este proyecto te resultó útil, dale una estrella!** ⭐