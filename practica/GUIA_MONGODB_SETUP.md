# 🗄️ GUÍA COMPLETA: Instalación y Configuración de MongoDB

## OPCIÓN A: MongoDB Community Edition (Local en Windows)

### 1. Descargar MongoDB
1. Ir a: https://www.mongodb.com/try/download/community
2. Seleccionar:
   - Version: 7.0.x (latest)
   - Platform: Windows
   - Package: MSI
3. Click "Download"

### 2. Instalar MongoDB
1. Ejecutar el instalador .msi descargado
2. Elegir "Complete" installation
3. IMPORTANTE: Marcar "Install MongoDB as a Service"
   - Service Name: MongoDB
   - Data Directory: C:\Program Files\MongoDB\Server\7.0\data
   - Log Directory: C:\Program Files\MongoDB\Server\7.0\log
4. IMPORTANTE: Marcar "Install MongoDB Compass" (GUI opcional pero útil)
5. Click "Next" y "Install"

### 3. Verificar Instalación
Abrir PowerShell como Administrador y ejecutar:

```powershell
# Verificar que MongoDB está corriendo
Get-Service MongoDB

# Debería mostrar:
# Status   Name               DisplayName
# ------   ----               -----------
# Running  MongoDB            MongoDB Server
```

### 4. Probar Conexión
```powershell
# Abrir MongoDB Shell
mongosh

# Deberías ver:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
# Using MongoDB: 7.0.x
```

### 5. Comandos Básicos para Probar

```javascript
// Ver bases de datos existentes
show dbs

// Crear/usar la base de datos del proyecto
use nyc_hvfhv_db

// Ver colecciones (debería estar vacío inicialmente)
show collections

// Salir
exit
```

---

## OPCIÓN B: MongoDB Atlas (Cloud - Gratis)

### 1. Crear Cuenta
1. Ir a: https://www.mongodb.com/cloud/atlas/register
2. Registrarse (gratis - no requiere tarjeta)

### 2. Crear Cluster
1. Click "Build a Database"
2. Elegir "FREE" (M0 Sandbox)
3. Provider: AWS
4. Region: Elegir más cercana a ti
5. Cluster Name: "hvfhv-cluster"
6. Click "Create"

### 3. Configurar Acceso

**A. Database User:**
1. Security → Database Access → Add New Database User
2. Username: `hvfhv_user`
3. Password: `TuPassword123` (guárdala)
4. Database User Privileges: "Read and write to any database"
5. Click "Add User"

**B. Network Access:**
1. Security → Network Access → Add IP Address
2. Click "Allow Access from Anywhere" (0.0.0.0/0)
3. Click "Confirm"

### 4. Obtener URI de Conexión
1. Database → Connect → Drivers
2. Driver: Python / Version: 3.12 or later
3. Copiar la URI:
```
mongodb+srv://hvfhv_user:<password>@hvfhv-cluster.xxxxx.mongodb.net/
```
4. Reemplazar `<password>` con tu password real

---

## PASO 2: Configurar la Conexión en el Proyecto

### Para MongoDB Local:
```python
MONGO_URI = "mongodb://localhost:27017/"
```

### Para MongoDB Atlas:
```python
MONGO_URI = "mongodb+srv://hvfhv_user:TuPassword123@hvfhv-cluster.xxxxx.mongodb.net/"
```

---

## PASO 3: Verificar Conexión desde Python

Ejecutar en PowerShell:

```powershell
# Instalar pymongo
pip install pymongo

# Probar conexión
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017/'); print('✅ Conexión exitosa:', client.server_info()['version'])"
```

Si ves la versión de MongoDB, ¡está funcionando! ✅

---

## Troubleshooting Común

### Error: "MongoServerSelectionTimeoutError"
**Causa:** MongoDB no está corriendo

**Solución (Windows):**
```powershell
# Iniciar servicio MongoDB
Start-Service MongoDB

# Verificar estado
Get-Service MongoDB
```

### Error: "Authentication failed"
**Causa:** Credenciales incorrectas en Atlas

**Solución:**
1. Verificar username y password
2. Asegurar que la IP esté en whitelist
3. Reemplazar `<password>` en la URI con la password real

### Error: "No module named 'pymongo'"
```powershell
pip install pymongo
```

---

## MongoDB Compass (GUI Opcional)

Si instalaste Compass:
1. Abrir MongoDB Compass
2. New Connection
3. URI: `mongodb://localhost:27017/` (local) o tu URI de Atlas
4. Click "Connect"
5. Podrás ver bases de datos, colecciones y documentos visualmente

---

## Siguiente Paso: Ejecutar el Notebook

Una vez MongoDB esté corriendo, abre el notebook y ejecuta las celdas de la Sección 4 para crear la base de datos automáticamente.
