import json
from datetime import datetime
import pandas as pd
import requests_cache
from retry_requests import retry
import openmeteo_requests

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Definimos los parámetros de la API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 27.5726,
    "longitude": 115.084,
    "hourly": "temperature_2m"
}
responses = openmeteo.weather_api(url, params=params)

# Procesamos los datos de la respuesta
response = responses[0]
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

# Convertir las temperaturas a tipo float estándar de Python
temperaturas = [float(temp) for temp in hourly_temperature_2m]

# Calculamos los valores
temp_max = float(f"{max(temperaturas):.2f}")
temp_min = float(f"{min(temperaturas):.2f}")
temp_mitjana = float(f"{sum(temperaturas) / len(temperaturas):.2f}")

# Crear un diccionario con las estadísticas calculadas
dades = {
    "temperatura_maxima": temp_max,
    "temperatura_minima": temp_min,
    "temperatura_mitjana": temp_mitjana
}

# Generar el nombre del archivo JSON
nom_fitxer = f"temp_{datetime.now().strftime('%Y%m%d')}.json"

# Guardar los resultados en un archivo JSON
with open(nom_fitxer, 'w') as fitxer_json:
    json.dump(dades, fitxer_json, indent=4)

print(f"Dades de temperatura guardades a: {nom_fitxer}")