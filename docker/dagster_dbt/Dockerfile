FROM python:3.13.12-slim-trixie

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

RUN mkdir -p $DAGSTER_HOME

COPY dagster.yaml $DAGSTER_HOME
COPY profiles.yml /root/.dbt/profiles.yml


WORKDIR $DAGSTER_HOME
