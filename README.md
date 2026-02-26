# Analisis en Tiempo Real de Bicicletas con Spark, Airflow, Cassandra y Flask

## Objetivo

El objetivo de este proyecto es **capturar datos en tiempo real de la API pública de bicicletas**, almacenarlos en **Apache Cassandra**, procesarlos con **Apache Spark** y visualizarlos mediante una aplicación web desarrollada en **Flask**.  

La infraestructura se despliega con **Docker Compose**, integrando además **Apache Airflow** para la planificación de la ingesta de datos en tiempo real.  

En resumen, el proyecto permite:
- Ingesta periodica de datos de bicicletas publicas desde API externa (CityBikes).
- Guardar los datos en Cassandra.
- Procesamiento distribuido con Spark para generar métricas y visualizaciones.
- Mostrar los resultados en gráficos interactivos vía Flask + Plotly.


## Arquitectura

```text
CityBikes API
    |
    v
Airflow DAG (cada 2 min) ----> Script de ingesta  ----> Cassandra
                                                               |
                                                               v
Flask /bicishora ----> Spark Session ----> lectura Cassandra + agregacion ----> Plotly
```

Componentes principales:

-   **API de Bicicletas:** Proporciona datos en tiempo real sobre las estaciones de bicicletas (ej., bicicletas disponibles, estado de la estación). El proyecto utiliza la API de CityBikes como ejemplo.

-   **Apache Airflow:** Orquesta el proceso de ingesta de datos. Se define un DAG (Directed Acyclic Graph) para programar la ejecución de un trabajo de Spark que extrae datos de la API y los almacena en Cassandra. Ver [`dags/spark_cassandra_bikes_dag.py`](dags/spark_cassandra_bikes_dag.py).

-   **Apache Cassandra:** Una base de datos NoSQL escalable utilizada para almacenar los datos brutos de las estaciones de bicicletas.

-   **Apache Spark:** Procesa los datos almacenados en Cassandra para generar métricas agregadas, como el número de bicicletas disponibles por hora.

-   **Aplicación Flask:** Una aplicación web que consulta Cassandra y utiliza Plotly para crear gráficos interactivos para visualizar los datos.




## Instalacion

1. Clonar repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

2. Requisito principal:

- Docker Desktop (o Docker Engine + Compose plugin).

3. Entorno local opcional (solo para scripts fuera de Docker):

```bash
conda create -y -n pyspark python=3.10
conda activate pyspark
pip install -r requirements.txt
```

## Despliegue

1. Levantar todo el stack:

```bash
docker-compose up -d --build
```

2. Verificar interfaces:

- Spark Master UI: [http://localhost:8080](http://localhost:8080)
- Airflow Webserver: [http://localhost:8084](http://localhost:8084)  (usuario/password por defecto: `airflow` / `airflow`)
- Flask App: [http://localhost:5000](http://localhost:5000)

## Uso

1. Configurar y activar el DAG en Airflow::

-   Accede a la interfaz de Airflow en [http://localhost:8084](http://localhost:8084).
-   Localiza el DAG `spark_cassandra_bikes_dag` y actívalo.
-   Monitoriza la ejecución del DAG para verificar la correcta ingesta de datos, este corre cada 2 mins.

2. Consultar datos y analitica:

-   Accede a la aplicación Flask en [http://localhost:5000](http://localhost:5000).
-   Visualiza los datos de las estaciones de bicicletas en la página principal.
-   Explora las gráficas generadas con Spark en la ruta `/bicishora`.


## License

MIT

