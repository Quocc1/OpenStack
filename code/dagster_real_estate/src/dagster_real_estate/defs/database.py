import dagster as dg

from .resources import TrinoResource


def drop_all_tables_in_schema(
    context: dg.AssetExecutionContext, trino: TrinoResource, schema: str
):
    """Drop all tables in a Trino schema (for analytics/warehouse schemas)"""
    try:
        context.log.info(f"Schema: {schema}")

        tables = trino.query(f"SHOW TABLES FROM {schema}")

        for table in tables:
            table_name = table[0]
            sql = f"DROP TABLE IF EXISTS {schema}.{table_name}"
            context.log.info(sql)
            trino.execute(sql)
    except Exception as e:
        context.log.warning(f"Failed to drop tables in {schema}: {e}. Skipping...")


@dg.asset
def create_schemas(context: dg.AssetExecutionContext, trino: TrinoResource):
    context.log.info("Creating schemas default")
    trino.execute(
        "CREATE SCHEMA IF NOT EXISTS warehouse.default "
        "WITH (location = 's3a://warehouse/default')"
    )

    context.log.info("Creating schemas bronze")
    trino.execute(
        "CREATE SCHEMA IF NOT EXISTS warehouse.bronze "
        "WITH (location = 's3a://warehouse/bronze')"
    )

    context.log.info("Creating schemas silver")
    trino.execute(
        "CREATE SCHEMA IF NOT EXISTS warehouse.silver "
        "WITH (location = 's3a://warehouse/silver')"
    )

    context.log.info("Creating schemas gold")
    trino.execute("CREATE SCHEMA IF NOT EXISTS analytics.gold")


@dg.asset(deps=[create_schemas])
def drop_tables(context: dg.AssetExecutionContext, trino: TrinoResource):
    context.log.info("Dropping old tables...")
    drop_all_tables_in_schema(context, trino, "warehouse.bronze")
    drop_all_tables_in_schema(context, trino, "warehouse.silver")
    drop_all_tables_in_schema(context, trino, "analytics.gold")
    context.log.info("Drop tables completed")
