import dagster as dg

create_schemas_job = dg.define_asset_job(
    name="create_schemas_job", selection="create_schemas"
)

drop_tables_job = dg.define_asset_job(name="drop_tables_job", selection="drop_tables")

crawl_real_estate_website_job = dg.define_asset_job(
    name="crawl_real_estate_website_job", selection="crawl_real_estate_website"
)

dbt_bronze_job = dg.define_asset_job(name="dbt_bronze_job", selection="bronze_raw_data")
dbt_silver_job = dg.define_asset_job(
    name="dbt_silver_job", selection="silver_refined_data"
)
dbt_gold_job = dg.define_asset_job(name="dbt_gold_job", selection="gold_analytics_data")
dbt_all_jobs = dg.define_asset_job(
    name="dbt_all_jobs",
    selection=[
        "bronze_raw_data",
        "silver_refined_data",
        "gold_analytics_data",
    ],
)

end_to_end_job = dg.define_asset_job(
    name="end_to_end_job",
    description="Complete real estate data pipeline from crawling to gold layer",
)
