FROM eclipse-temurin:17-jdk

ENV SPARK_VERSION=4.1.1
ENV ICEBERG_VERSION=4.0_2.13-1.10.1
ENV AWSSDK_VERSION=2.42.13
ENV AWSCLI_VERSION=2.42.13
ENV KYUUBI_VERSION=1.11.0
ENV POSTGRES_VERSION=42.7.10
ENV HADOOP_AWS_VERSION=3.4.3
ENV AWS_SDK_BUNDLE_VERSION=1.12.797
ENV ANALYTICS_ACCELERATOR_VERSION=1.3.1

ENV SPARK_HOME=/opt/spark
ENV KYUUBI_HOME=/opt/kyuubi
ENV BIN_DIR=/usr/bin
ENV INSTALL_DIR=/tmp/install
ENV NOTEBOOK_DIR=/var/lib/app/notebooks
ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"

RUN mkdir -p ${SPARK_HOME} ${KYUUBI_HOME} ${INSTALL_DIR} ${NOTEBOOK_DIR}

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    sudo \
    curl \
    unzip \
    make \
    dos2unix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR ${INSTALL_DIR}

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt && \
    rm requirements.txt

RUN curl -fsSL https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark.tgz && \
    tar xzf spark.tgz --directory /opt/spark --strip-components 1 && \
    rm spark.tgz && \
    cd /opt/spark/jars && \
    curl -fsSL https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.0_2.13/1.10.1/iceberg-spark-runtime-4.0_2.13-1.10.1.jar -O && \
    curl -fsSL https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWSSDK_VERSION}/bundle-${AWSSDK_VERSION}.jar -O && \
    curl -fsSL https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/${AWSCLI_VERSION}/url-connection-client-${AWSCLI_VERSION}.jar -O && \
    curl -fsSL https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar -O && \
    curl -fsSL https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_BUNDLE_VERSION}/aws-java-sdk-bundle-${AWS_SDK_BUNDLE_VERSION}.jar -O && \
    curl -fsSL https://repo1.maven.org/maven2/software/amazon/s3/analyticsaccelerator/analyticsaccelerator-s3/${ANALYTICS_ACCELERATOR_VERSION}/analyticsaccelerator-s3-${ANALYTICS_ACCELERATOR_VERSION}.jar -O && \
    curl -fsSL https://repo1.maven.org/maven2/org/postgresql/postgresql/${POSTGRES_VERSION}/postgresql-${POSTGRES_VERSION}.jar -O

RUN curl -fsSL https://dlcdn.apache.org/kyuubi/kyuubi-${KYUUBI_VERSION}/apache-kyuubi-${KYUUBI_VERSION}-bin.tgz -o kyuubi.tgz && \
    tar xzf kyuubi.tgz --directory ${KYUUBI_HOME} --strip-components 1 && \
    rm kyuubi.tgz

WORKDIR ${SPARK_HOME}

COPY spark-defaults.conf ${SPARK_HOME}/conf
COPY notebook ${BIN_DIR}/notebook
COPY entrypoint.sh ${BIN_DIR}

RUN dos2unix ${BIN_DIR}/notebook ${BIN_DIR}/entrypoint.sh && \
    chmod +x ${SPARK_HOME}/bin/* ${BIN_DIR}/notebook ${BIN_DIR}/entrypoint.sh && \
    chmod +x ${BIN_DIR}/entrypoint.sh

EXPOSE 8888 7077 8061 8062 10000 10009 18080

WORKDIR ${BIN_DIR}

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
CMD ["notebook"]
