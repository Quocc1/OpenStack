help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up                Bring up containers to run"
	@echo "  down              Shut down containers created from the docker-compose file"
	@echo "  run               Shut down then bring up containers"
	@echo "  master-ui         Open Spark master UI"
	@echo "  worker-ui         Open Spark worker UI"
	@echo "  history-ui        Open Spark history UI"
	@echo "  notebook-ui       Open Spark Notebook UI"
	@echo "  minio-ui          Open Minio UI"
	@echo "  dagster-ui        Open Dagster UI"
	@echo "  metabase-ui       Open Metabase UI"


####################################################################################################################
# Setup containers to run Airflow
up:
	docker compose up -d --build

down:
	docker compose down

run: down up

####################################################################################################################
# Monitoring
master-ui:
	explorer.exe http://localhost:8061

worker-ui:
	explorer.exe http://localhost:8062

history-ui:
	explorer.exe http://localhost:18080

notebook-ui:
	explorer.exe http://localhost:8888

minio-ui:
	explorer.exe http://localhost:9001

dagster-ui:
	explorer.exe http://localhost:3070

metabase-ui:
	explorer.exe http://localhost:3030

# If you are using Linux, you may use this command instead
master-ui-linux:
	open http://localhost:8061

worker-ui-linux:
	open http://localhost:8062

history-ui-linux:
	open http://localhost:18080

notebook-ui-linux:
	open http://localhost:8888

minio-ui-linux:
	open http://localhost:9001

dagster-ui-linux:
	open http://localhost:3070

metabase-ui-linux:
	open http://localhost:3030