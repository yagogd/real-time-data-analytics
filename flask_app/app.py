from flask import Flask, render_template
from cassandra.cluster import Cluster

import pandas as pd
import plotly.express as px
import plotly.io as pio

from pyspark.sql.functions import to_timestamp, hour, minute, concat_ws, sum

from pyspark.sql import SparkSession

app = Flask(__name__)

def get_bike_data():
    cluster = Cluster(['database'])  # o 'cassandra' si renombraste el servicio
    session = cluster.connect('bike_data')

    rows = session.execute('SELECT * FROM bike_stations')
    data = [dict(row._asdict()) for row in rows]

    return data

def get_spark_session():
    return SparkSession.builder \
        .appName("Bicis por hora") \
        .config("spark.jars", "/app/jars/spark-cassandra-connector_2.12-3.4.1.jar") \
        .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
        .config("spark.sql.catalog.cassandracatalog", "com.datastax.spark.connector.CassandraCatalog") \
        .config("spark.cassandra.connection.host", "database") \
        .getOrCreate()

@app.route('/')
def index():
    data = get_bike_data()
    return render_template('index.html', data=data)

@app.route('/test')
def test():
    # Datos de prueba
    df = pd.DataFrame({
        "categoria": ["A", "B", "C", "D"],
        "valor": [10, 15, 7, 20]
    })

    # Crear gráfica
    fig = px.bar(df, x="categoria", y="valor", title="Gráfica de prueba")
    chart_html = pio.to_html(fig, full_html=False)

    return render_template("test.html", chart_html=chart_html)


@app.route('/bicishora')
def bicis_por_hora():
    spark = get_spark_session()

    df = spark.read \
        .format("org.apache.spark.sql.cassandra") \
        .option("keyspace", "bike_data") \
        .option("table", "bike_stations") \
        .load()

    df_filtered = df.filter(df.timestamp.isNotNull())
    df_filtered = df_filtered.withColumn("timestamp", to_timestamp(df_filtered.timestamp))

    df_hora_minuto = df_filtered.withColumn(
        "hora_minuto", 
        concat_ws(":", hour(df_filtered.timestamp), minute(df_filtered.timestamp))
    ).groupBy("hora_minuto") \
     .agg(sum("free_bikes").alias("total_bicis_libres")) \
     .orderBy("hora_minuto")

    pandas_df = df_hora_minuto.toPandas()
    spark.stop()

    chart = px.line(pandas_df, x="hora_minuto", y="total_bicis_libres", title="Bicis Libres por minuto")
    chart_html = pio.to_html(chart, full_html=False)

    return render_template("bicishora.html", chart_html=chart_html, data=pandas_df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
