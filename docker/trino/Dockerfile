FROM python:3.11-bullseye

ENV TRINO_VERSION=406
ENV TRINO_HOME=/opt/trino
ENV BIN_DIR=/usr/bin
ENV DATA_STAGE_DIR=/var/lib/app/stage
ENV TRINO_DATA_DIR=/var/lib/trino/data
ENV INSTALL_DIR=/tmp/install
ENV CERT_DIR=/usr/local/certs

RUN mkdir -p ${TRINO_HOME} ${TRINO_DATA_DIR} ${DATA_STAGE_DIR} ${INSTALL_DIR} ${CERT_DIR}

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      unzip \
      make \
      openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${INSTALL_DIR}

# Install python deps
RUN pip3 install --no-cache-dir trino

# Install Trino
RUN curl https://repo1.maven.org/maven2/io/trino/trino-server/${TRINO_VERSION}/trino-server-${TRINO_VERSION}.tar.gz -Lo trino-server-${TRINO_VERSION}.tar.gz \
    && tar xvzf trino-server-${TRINO_VERSION}.tar.gz --directory ${TRINO_HOME} --strip-components 1 \
    && rm trino-server-${TRINO_VERSION}.tar.gz 

WORKDIR ${TRINO_HOME}

COPY ./conf ${TRINO_HOME}/etc

RUN chmod u+x ${TRINO_HOME}/bin/* 

EXPOSE 8060

CMD ["/opt/trino/bin/launcher", "run"]