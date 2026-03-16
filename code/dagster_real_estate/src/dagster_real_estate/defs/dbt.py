import dagster as dg
from dagster_dbt import DbtCliResource

from .crawl import crawl_real_estate_website
from .resources import (
    dbt_project_directory_bronze,
    dbt_project_directory_gold,
    dbt_project_directory_silver,
)


@dg.asset(deps=[crawl_real_estate_website])
def bronze_raw_data(
    context: dg.AssetExecutionContext, dbt_bronze: DbtCliResource
) -> None:
    """Execute bronze layer dbt commands"""
    context.log.info(f"Executing bronze dbt run: {dbt_project_directory_bronze}")
    dbt_bronze.cli(
        ["build", "--project-dir", str(dbt_project_directory_bronze)]
    ).stream()


@dg.asset(deps=[bronze_raw_data])
def silver_refined_data(
    context: dg.AssetExecutionContext, dbt_silver: DbtCliResource
) -> None:
    """Execute silver layer dbt commands"""
    context.log.info(f"Executing silver dbt run: {dbt_project_directory_silver}")
    dbt_silver.cli(
        ["build", "--project-dir", str(dbt_project_directory_silver)]
    ).stream()


@dg.asset(deps=[silver_refined_data])
def gold_analytics_data(
    context: dg.AssetExecutionContext, dbt_gold: DbtCliResource
) -> None:
    """Execute gold layer dbt commands"""
    context.log.info(f"Executing gold dbt run: {dbt_project_directory_gold}")
    dbt_gold.cli(["build", "--project-dir", str(dbt_project_directory_gold)]).stream()
