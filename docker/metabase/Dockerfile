ARG metabase_repo=metabase
ARG metabase_version=v0.49.8
FROM metabase/${metabase_repo}:${metabase_version} as metabase

FROM openjdk:19-slim-bullseye

ENV FC_LANG en-US LC_CTYPE en_US.UTF-8

ENV MB_DB_FILE="/conf/metabase.db" 
ENV MB_DB_HOST="0.0.0.0" 
ENV MB_JETTY_PORT="3030" 
ENV MB_DB_TYPE="h2" 
ENV MB_PLUGINS_DIR="/plugins"

# dependencies
RUN mkdir -p ${MB_PLUGINS_DIR} && chmod a+rwx ${MB_PLUGINS_DIR} && \
    mkdir -p $(dirname ${MB_DB_FILE}) && chmod a+rwx $(dirname ${MB_DB_FILE}) && \
    apt-get update -yq && apt-get install -yq bash fonts-dejavu-core fonts-dejavu-extra fontconfig curl openjdk-11-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/{apt,dpkg,cache,log}
RUN mkdir -p /app/certs && \
    curl https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -o /app/certs/rds-combined-ca-bundle.pem  && \
    keytool -noprompt -import -trustcacerts -alias aws-rds -file /app/certs/rds-combined-ca-bundle.pem -keystore /etc/ssl/certs/java/cacerts -keypass changeit -storepass changeit && \
    curl https://cacerts.digicert.com/DigiCertGlobalRootG2.crt.pem -o /app/certs/DigiCertGlobalRootG2.crt.pem  && \
    keytool -noprompt -import -trustcacerts -alias azure-cert -file /app/certs/DigiCertGlobalRootG2.crt.pem -keystore /etc/ssl/certs/java/cacerts -keypass changeit -storepass changeit && \
    useradd --shell /bin/bash metabase


WORKDIR /app
USER metabase

# copy app from the offical image
COPY --from=metabase --chown=metabase /app /app

# expose our default runtime port
EXPOSE 3030

# run it
ENTRYPOINT ["/app/run_metabase.sh"]