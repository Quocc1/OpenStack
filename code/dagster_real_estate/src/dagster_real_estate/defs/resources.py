from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject
from dagster_aws.s3 import S3Resource
from trino.dbapi import connect


class TrinoResource(dg.ConfigurableResource):
    """Resource for connecting to Trino database."""

    host: str
    port: int
    user: str

    @contextmanager
    def get_connection(self) -> Iterator:
        conn = connect(
            host=self.host,
            port=self.port,
            user=self.user,
        )
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, sql: str) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

    def query(self, sql: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()


dbt_project_directory_bronze = Path(__file__).absolute().parent / "bronze"
dbt_project_directory_silver = Path(__file__).absolute().parent / "silver"
dbt_project_directory_gold = Path(__file__).absolute().parent / "gold"

dbt_project_bronze = DbtProject(project_dir=dbt_project_directory_bronze)
dbt_project_silver = DbtProject(project_dir=dbt_project_directory_silver)
dbt_project_gold = DbtProject(project_dir=dbt_project_directory_gold)

dbt_resource_bronze = DbtCliResource(project_dir=dbt_project_bronze)
dbt_resource_silver = DbtCliResource(project_dir=dbt_project_silver)
dbt_resource_gold = DbtCliResource(project_dir=dbt_project_gold)


@dg.definitions
def resources() -> dg.Definitions:
    return dg.Definitions(
        resources={
            "trino": TrinoResource(host="trino", port=8080, user="trino"),
            "dbt_bronze": dbt_resource_bronze,
            "dbt_silver": dbt_resource_silver,
            "dbt_gold": dbt_resource_gold,
            "s3": S3Resource(
                endpoint_url="http://rustfs:9000",
                aws_access_key_id="admin",
                aws_secret_access_key="password",
                region_name="us-east-1",
            ),
        }
    )
