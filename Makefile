help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up            Bring up containers to run Airflow"
	@echo "  down          Shut down containers created from the docker-compose file"
	@echo "  run           Shut down then bring up Airflow containers"
	@echo "  az-login      Log into Azure from inside the container"
	@echo "  infra-init    Initialize Terraform configuration"
	@echo "  infra-up      Build the Azure Cloud infrastructure using Terraform"
	@echo "  infra-down    Destroy the Azure Cloud infrastructure created using Terraform"
	@echo "  infra-config  Generate the configuration.env file from Terraform output.tf"


####################################################################################################################
# Setup containers to run Airflow
up:
	docker compose up -d --build

down:
	docker compose down

run: down up

####################################################################################################################
# Set up cloud infrastructure
infra-init:
	cd ./terraform && terraform init

infra-up:
	cd ./terraform && terraform apply --auto-approve

infra-down:
	cd ./terraform && terraform destroy --auto-approve

infra-config:
	cd ./terraform && terraform output > ../airflow/config/configuration.env

####################################################################################################################
# Login Azure
az-login:
	sh az_login.sh