# === Configuración ===
$year   = 2024
$types  = @('yellow_tripdata','green_tripdata','fhv_tripdata','fhvhv_tripdata')  # cambia si quieres menos tipos
$months = 1..12
$baseUrl = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
$outDir  = "NYC_TLC_$year"

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

function Download-TripFile {
    param(
        [string]$type,
        [int]$year,
        [string]$month
    )
    $fileName = '{0}_{1}-{2}.parquet' -f $type, $year, $month
    $url  = "$baseUrl/$fileName"
    $dest = Join-Path $outDir $fileName

    if (Test-Path $dest) { Write-Host "✅ Ya existe: $fileName (saltando)"; return }

    $maxRetries = 3
    for ($i=1; $i -le $maxRetries; $i++) {
        try {
            Write-Host "⬇️  Descargando ($i/$maxRetries): $fileName"
            Invoke-WebRequest -Uri $url -OutFile $dest -TimeoutSec 600

            if ((Test-Path $dest) -and ((Get-Item $dest).Length -gt 0)) {
                Write-Host "✅ OK: $fileName"
                return
            } else {
                throw "Archivo vacío o no creado"
            }
        } catch {
            Write-Warning ("Intento {0} falló para {1}: {2}" -f $i, $fileName, $_.Exception.Message)
            Start-Sleep -Seconds (5 * $i)
        }
    }
    Write-Error ("❌ No se pudo descargar {0}. ¿Mes no publicado o URL distinta?" -f $fileName)
}

# === Bucle principal: 12 meses x tipos seleccionados ===
foreach ($t in $types) {
    foreach ($m in $months) {
        $mm = "{0:d2}" -f $m
        Download-TripFile -type $t -year $year -month $mm
    }
}

# Tabla de zonas (para $lookup en Mongo)
Invoke-WebRequest -Uri "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv" -OutFile (Join-Path $outDir "taxi_zone_lookup.csv")

Write-Host "`n🚀 Terminado. Archivos en: $(Resolve-Path $outDir)"
