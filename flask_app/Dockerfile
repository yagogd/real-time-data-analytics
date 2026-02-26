FROM python:3.10-slim

WORKDIR /app

# Instala Java 17 y curl
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Variables de entorno para Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Copia la aplicación
COPY . /app

# Copia los archivos .jar del conector
COPY jars/* /app/jars/
ENV PYSPARK_SUBMIT_ARGS="--packages com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions --conf spark.cassandra.connection.host=database pyspark-shell"


# Instala paquetes de Python
RUN pip install flask cassandra-driver pandas plotly pyspark==3.4.1

EXPOSE 5000

CMD ["python", "app.py"]
