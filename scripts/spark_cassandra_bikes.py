from cassandra.cluster import Cluster
import requests
import uuid

# Conectar a Cassandra
cluster = Cluster(["database"])  # usa el nombre del servicio del contenedor
session = cluster.connect()

# Crear keyspace y tabla si no existen
session.execute("""
CREATE KEYSPACE IF NOT EXISTS bike_data
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

session.set_keyspace("bike_data")

session.execute("""
CREATE TABLE IF NOT EXISTS bike_stations (
    id UUID PRIMARY KEY,
    station_id TEXT,
    name TEXT,
    free_bikes INT,
    timestamp TIMESTAMP
)
""")

# Obtener datos de la API
url = "https://api.citybik.es/v2/networks/alsa-nextbike-leon"
response = requests.get(url)
data = response.json()

stations = data["network"]["stations"]

# Insertar datos en Cassandra
for station in stations:
    station_id = station.get("id", "unknown")
    name = station.get("name", "unknown")
    free_bikes = station.get("free_bikes", 0)

    session.execute(
        "INSERT INTO bike_stations (id, station_id, name, free_bikes, timestamp) VALUES (%s, %s, %s, %s, toTimestamp(now()))",
        (uuid.uuid4(), station_id, name, free_bikes)
    )

print("Datos insertados correctamente.")
cluster.shutdown()
