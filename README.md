# Real-Time Bike Analytics with Spark, Airflow, Cassandra, and Flask

Language: [Español](README.es.md)

## Objective

The goal of this project is to **capture real-time data from a public bike API**, store it in **Apache Cassandra**, process it with **Apache Spark**, and visualize it through a **Flask** web application.

The infrastructure is deployed with **Docker Compose**, and includes **Apache Airflow** to schedule the real-time ingestion workflow.

In short, this project allows you to:
- Periodically ingest public bike data from an external API (CityBikes).
- Store the data in Cassandra.
- Run distributed processing with Spark to generate metrics and visualizations.
- Display results in interactive charts using Flask + Plotly.

## Architecture

```text
CityBikes API
    |
    v
Airflow DAG (every 2 min) ----> Ingestion script ----> Cassandra
                                                              |
                                                              v
Flask /bicishora ----> Spark Session ----> read Cassandra + aggregation ----> Plotly
```

Main components:

- **Bike API:** Provides real-time station data (for example, available bikes and station status). This project uses the CityBikes API as an example.
- **Apache Airflow:** Orchestrates data ingestion. A DAG (Directed Acyclic Graph) schedules a Spark job that extracts data from the API and stores it in Cassandra. See [`dags/spark_cassandra_bikes_dag.py`](dags/spark_cassandra_bikes_dag.py).
- **Apache Cassandra:** A scalable NoSQL database used to store raw bike-station data.
- **Apache Spark:** Processes data from Cassandra to generate aggregated metrics, such as available bikes per hour.
- **Flask Application:** Web app that queries Cassandra and uses Plotly for interactive charts.

## Installation

1. Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_NAME>
```

2. Main prerequisite:

- Docker Desktop (or Docker Engine + Compose plugin).

3. Optional local environment (only for scripts outside Docker):

```bash
conda create -y -n pyspark python=3.10
conda activate pyspark
pip install -r requirements.txt
```

## Deployment

1. Start the full stack:

```bash
docker-compose up -d --build
```

2. Verify interfaces:

- Spark Master UI: [http://localhost:8080](http://localhost:8080)
- Airflow Webserver: [http://localhost:8084](http://localhost:8084) (default user/password: `airflow` / `airflow`)
- Flask App: [http://localhost:5000](http://localhost:5000)

## Usage

1. Configure and enable the Airflow DAG:

- Open Airflow at [http://localhost:8084](http://localhost:8084).
- Find DAG `spark_cassandra_bikes_dag` and enable it.
- Monitor DAG runs to verify ingestion is working correctly (runs every 2 minutes).

2. Query data and analytics:

- Open the Flask app at [http://localhost:5000](http://localhost:5000).
- View bike station data on the main page.
- Explore Spark-generated charts at `/bicishora`.

## Credits

The Spark infrastructure is based on the [`easy_spark`](https://github.com/Napuh/easy_spark) repository, used to simplify cluster setup and deployment with Docker.
