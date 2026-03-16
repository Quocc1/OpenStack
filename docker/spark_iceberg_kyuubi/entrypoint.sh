#!/bin/bash

export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"
export SPARK_BIN=/opt/spark/sbin
export KYUUBI_BIN=/opt/kyuubi/bin
export KYUUBI_CONF_DIR=/opt/kyuubi/conf
export BIN_DIR=/usr/bin

mkdir -p /tmp/spark-events

echo "Starting Spark Master..."
${SPARK_BIN}/start-master.sh -p 7077 --webui-port 8061

echo "Starting Spark Worker..."
${SPARK_BIN}/start-worker.sh spark://localhost:7077 --webui-port 8062

echo "Starting Spark History Server..."
${SPARK_BIN}/start-history-server.sh

echo "Starting Kyuubi Server..."
${KYUUBI_BIN}/kyuubi start

echo "Services started. Launching Jupyter notebook..."
${BIN_DIR}/notebook

if [[ $# -gt 0 ]] ; then
    eval "$1"
fi
