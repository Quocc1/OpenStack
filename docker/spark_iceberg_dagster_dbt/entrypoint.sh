#!/bin/bash

export JAVA_HOME="$(jrunscript -e 'java.lang.System.out.println(java.lang.System.getProperty("java.home"));')"
export DAGSTER_DIR=/var/lib/app/dagster
export SPARK_BIN=/opt/spark/sbin
export KYUUBI_BIN=/opt/kyuubi/bin

mkdir -p /tmp/spark-events
start-master.sh -p 7077 --webui-port 8061
start-worker.sh spark://spark:7077 --webui-port 8062
start-history-server.sh
${KYUUBI_BIN}/kyuubi start

cd ${DAGSTER_DIR} && dagster-webserver -h 0.0.0.0 -p 3070 &


if [[ $# -gt 0 ]] ; then
    eval "$1"
fi