from dagster import job
from dagster_dbt import dbt_cli_resource
from dagster_pyspark import pyspark_resource

from .database import drop_tables_op, create_schemas_op, trino_resource
from .crawl import crawl_real_estate_website_op
from .dbt import dbt_bronze_run_op, dbt_bronze_test_doc_sources_op, dbt_silver_run_op, \
    dbt_silver_test_doc_sources_op, dbt_gold_run_op, dbt_gold_test_doc_sources_op
# from .predict import predict_op


@job(resource_defs={'dbt': dbt_cli_resource, 'trino': trino_resource, 'pyspark': pyspark_resource})
def end_to_end():
    dbt_gold_test_doc_sources_op(
        dbt_gold_run_op(
            dbt_silver_test_doc_sources_op(
                dbt_silver_run_op(
                    dbt_bronze_test_doc_sources_op(
                        dbt_bronze_run_op(
                            crawl_real_estate_website_op(
                                drop_tables_op(
                                    create_schemas_op()
                                )
                            )
                        )
                    )
                )
            )
        )
    )
