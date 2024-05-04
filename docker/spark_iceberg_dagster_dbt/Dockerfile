FROM python:3.11-bullseye

ENV SPARK_VERSION=3.3.1
ENV KYUUBI_VERSION=1.6.1
ENV AWSCLI_VERSION=2.17.247
ENV AWSSDK_VERSION=2.17.247
ENV POSTGRES_VERSION=42.7.3
ENV ICEBERG_VERSION=3.3_2.12-1.1.0
ENV SPARK_HOME=/opt/spark
ENV KYUUBI_HOME=/opt/kyuubi
ENV DAGSTER_HOME=/opt/dagster

ENV BIN_DIR=/usr/bin
ENV DBT_DIR=/var/lib/app/dbt
ENV INSTALL_DIR=/tmp/install
ENV DAGSTER_DIR=/var/lib/app/dagster
ENV DATA_STAGE_DIR=/var/lib/app/stage
ENV NOTEBOOKS_DIR=/var/lib/app/notebooks

ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"

RUN mkdir -p ${SPARK_HOME} ${DAGSTER_HOME} ${NOTEBOOKS_DIR} ${KYUUBI_HOME} ${INSTALL_DIR} ${BIN_DIR} \
            ${DAGSTER_DIR} ${DBT_DIR} ${DATA_STAGE_DIR}

RUN apt-get update && apt-get upgrade -y  && \
  apt-get install -y --no-install-recommends \
  sudo \
  curl \
  unzip \
  make \
  openjdk-11-jdk \
  dos2unix \
  && rm -rf /var/lib/apt/lists/*

WORKDIR ${INSTALL_DIR}

# Install python deps
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

# Download and Spark
RUN curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 \
    && rm spark-${SPARK_VERSION}-bin-hadoop3.tgz 

# Download iceberg spark runtime
RUN curl https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.3_2.12/1.1.0/iceberg-spark-runtime-${ICEBERG_VERSION}.jar -Lo iceberg-spark-runtime-${ICEBERG_VERSION}.jar  \
    && mv iceberg-spark-runtime-${ICEBERG_VERSION}.jar /opt/spark/jars 

# Download Java AWS SDK
RUN curl https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWSSDK_VERSION}/bundle-${AWSSDK_VERSION}.jar -Lo bundle-${AWSSDK_VERSION}.jar \
    && mv bundle-${AWSSDK_VERSION}.jar /opt/spark/jars 

# Download URL connection client required for S3FileIO
RUN curl https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/${AWSCLI_VERSION}/url-connection-client-${AWSCLI_VERSION}.jar -Lo url-connection-client-${AWSCLI_VERSION}.jar \
     && mv url-connection-client-${AWSCLI_VERSION}.jar /opt/spark/jars 

# Download and install Kyuubi JDBC
RUN curl https://archive.apache.org/dist/incubator/kyuubi/kyuubi-${KYUUBI_VERSION}-incubating/apache-kyuubi-${KYUUBI_VERSION}-incubating-bin.tgz -Lo kyuubi.tgz \ 
    && tar xvzf kyuubi.tgz --directory ${KYUUBI_HOME} --strip-components 1 \
    && rm kyuubi.tgz 

# Download and install Postgres driver for Hive metastore
RUN curl https://repo1.maven.org/maven2/org/postgresql/postgresql/${POSTGRES_VERSION}/postgresql-${POSTGRES_VERSION}.jar -Lo pgsql.jar \ 
    && mv pgsql.jar /opt/spark/jars 

WORKDIR ${SPARK_HOME}

COPY conf/spark-defaults.conf ${SPARK_HOME}/conf
COPY conf/dagster.yaml ${DAGSTER_HOME}
COPY conf/profiles.yml /root/.dbt/
COPY conf/notebook ${BIN_DIR}/notebook
COPY entrypoint.sh ${BIN_DIR}

RUN dos2unix ${BIN_DIR}/notebook

RUN chmod u+x ${SPARK_HOME}/* \
  && chmod u+x ${SPARK_HOME}/bin/* \
  && chmod u+x ${BIN_DIR}/notebook 

# Spark notebook port
EXPOSE 8888 

# Spark port
EXPOSE 7077 

# Spark master web ui port
EXPOSE 8061 

# Spark worker web ui port
EXPOSE 8062 

# Thrift ODBC/JDBC port
EXPOSE 10000 

# Kyuubi JDBC port
EXPOSE 10009 

# Spark history web ui port
EXPOSE 18080 

WORKDIR ${BIN_DIR}

ENTRYPOINT ["entrypoint.sh"]
CMD ["notebook"]